from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import stat
import ssl
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import urllib.request

from tools.openclaw import cursor_openclaw as cli


def client() -> cli.CursorApiClient:
    return cli.CursorApiClient(cli.Config(
        "https://api.cursor.com", "synthetic-key", "bearer", 5, 0, 0, True,
    ))


def handshake(client_context: ssl.SSLContext, server_context: ssl.SSLContext) -> None:
    """Perform a real TLS handshake in memory, without external traffic."""
    incoming, outgoing = ssl.MemoryBIO(), ssl.MemoryBIO()
    server_in, server_out = ssl.MemoryBIO(), ssl.MemoryBIO()
    peer = client_context.wrap_bio(incoming, outgoing, server_hostname="api.cursor.com")
    server = server_context.wrap_bio(server_in, server_out, server_side=True)
    client_done = server_done = False
    for _ in range(20):
        try:
            peer.do_handshake()
            client_done = True
        except ssl.SSLWantReadError:
            pass
        server_in.write(outgoing.read())
        try:
            server.do_handshake()
            server_done = True
        except ssl.SSLWantReadError:
            pass
        incoming.write(server_out.read())
        if client_done and server_done:
            return
    raise AssertionError("TLS handshake did not complete")


class DotenvSecurityTests(unittest.TestCase):
    def test_only_credentials_are_loaded_even_with_override(self) -> None:
        extra = {
            "HTTPS_PROXY": "http://attacker.invalid:8080",
            "https_proxy": "http://attacker.invalid:8080",
            "SSL_CERT_FILE": "/attacker/ca.pem", "SSL_CERT_DIR": "/attacker/certs",
            "SSLKEYLOGFILE": "/attacker/keys", "CURSOR_BASE_URL": "https://attacker.invalid",
            "PATH": "/attacker/bin", "UNRELATED": "ignored",
        }
        with tempfile.TemporaryDirectory() as tmp:
            dotenv = Path(tmp) / ".env"
            dotenv.write_text(
                'export CURSOR_API_KEY="synthetic credential"\nCURSOR_AUTH_MODE=bearer\n'
                + "".join(f"{key}={value}\n" for key, value in extra.items()),
                encoding="utf-8",
            )
            for override in (False, True):
                with self.subTest(override=override), mock.patch.dict(os.environ, {}, clear=True):
                    self.assertEqual(cli.env_loader.merge_dotenv_paths([dotenv], override=override), [dotenv])
                    self.assertEqual(dict(os.environ), {
                        "CURSOR_API_KEY": "synthetic credential", "CURSOR_AUTH_MODE": "bearer",
                    })
            with mock.patch.dict(os.environ, {"PATH": "original"}, clear=True):
                cli.env_loader.merge_dotenv_paths([dotenv], override=True)
                self.assertEqual(os.environ["PATH"], "original")

    def test_symlinked_dotenv_is_refused_at_lstat_before_open(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            script_dir = root / "tools" / "openclaw"
            script_dir.mkdir(parents=True)
            dotenv = root / ".env"
            target = Path(tmp) / "credentials"
            target.write_text("CURSOR_API_KEY=outside\nCURSOR_AUTH_MODE=bearer\n", encoding="utf-8")
            dotenv.symlink_to(target)
            st = dotenv.lstat()
            self.assertTrue(stat.S_ISLNK(st.st_mode))
            self.assertFalse(stat.S_ISREG(st.st_mode))
            for dangling in (False, True):
                if dangling:
                    target.unlink()
                with (
                    self.subTest(dangling=dangling),
                    mock.patch.object(cli, "_SCRIPT_DIR", script_dir),
                    mock.patch.dict(os.environ, {}, clear=True),
                    mock.patch.object(
                        cli.env_loader.os, "open",
                        side_effect=AssertionError("lstat must refuse symlinks before os.open"),
                    ) as open_file,
                ):
                    self.assertFalse(cli.env_loader._merge_file(dotenv, override=False))
                    cli._load_repo_dotenv()
                    self.assertEqual(dict(os.environ), {})
                    open_file.assert_not_called()
            with (
                mock.patch.dict(os.environ, {}, clear=True),
                mock.patch.object(
                    cli.env_loader.os, "open",
                    side_effect=AssertionError("lstat must refuse symlinks before os.open"),
                ) as open_file,
            ):
                self.assertEqual(cli.env_loader.merge_dotenv_paths([dotenv]), [])
                self.assertEqual(dict(os.environ), {})
                open_file.assert_not_called()

    def test_dotenv_replaced_by_symlink_during_open_is_refused_at_open(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dotenv = Path(tmp) / ".env"
            target = Path(tmp) / "outside"
            dotenv.write_text("CURSOR_API_KEY=initial\n", encoding="utf-8")
            target.write_text("CURSOR_API_KEY=outside\nCURSOR_AUTH_MODE=bearer\n", encoding="utf-8")
            real_open = os.open
            nofollow = getattr(os, "O_NOFOLLOW", 0)
            self.assertNotEqual(nofollow, 0, "O_NOFOLLOW required for symlink refusal during open")
            open_calls: list[tuple[object, int]] = []

            def replace_then_open(path, flags):
                open_calls.append((path, flags))
                self.assertEqual(flags & nofollow, nofollow)
                dotenv.unlink()
                dotenv.symlink_to(target)
                return real_open(path, flags)

            with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(cli.env_loader.os, "open", side_effect=replace_then_open):
                self.assertEqual(cli.env_loader.merge_dotenv_paths([dotenv]), [])
                self.assertNotIn("CURSOR_API_KEY", os.environ)
                self.assertNotIn("CURSOR_AUTH_MODE", os.environ)
            self.assertEqual(len(open_calls), 1)

    def test_dotenv_replaced_by_regular_file_during_open_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dotenv = Path(tmp) / ".env"
            replacement = Path(tmp) / "replacement"
            dotenv.write_text("CURSOR_API_KEY=initial\n", encoding="utf-8")
            replacement.write_text(
                "CURSOR_API_KEY=outside\nCURSOR_AUTH_MODE=bearer\n", encoding="utf-8",
            )
            before = dotenv.lstat()
            self.assertTrue(stat.S_ISREG(before.st_mode))
            self.assertTrue(stat.S_ISREG(replacement.lstat().st_mode))
            self.assertFalse(os.path.samestat(before, replacement.lstat()))
            real_open = os.open

            def replace_then_open(path, flags):
                self.assertEqual(path, dotenv)
                # Rename a separately created file so its inode cannot be reused.
                replacement.replace(dotenv)
                return real_open(path, flags)

            with (
                mock.patch.dict(os.environ, {}, clear=True),
                mock.patch.object(cli.env_loader.os, "open", side_effect=replace_then_open) as open_file,
            ):
                self.assertEqual(cli.env_loader.merge_dotenv_paths([dotenv]), [])
                self.assertEqual(dict(os.environ), {})
                open_file.assert_called_once()
            self.assertFalse(os.path.samestat(before, dotenv.lstat()))

    def test_git_ignores_root_and_nested_dotenv(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        gitignore = (repo / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn(".env", [line.strip() for line in gitignore if line.strip() and not line.strip().startswith("#")])
        result = subprocess.run(
            ["git", "check-ignore", "-v", "--no-index", ".env", "tools/openclaw/.env"],
            cwd=repo, capture_output=True, text=True, check=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        for line in result.stdout.splitlines():
            match, _ = line.split("\t", 1)
            pattern = match.split(":", 2)[2]
            self.assertFalse(pattern.startswith("!"), f"Negated ignore match: {line}")
        ignored_paths = [line.split("\t", 2)[-1] for line in result.stdout.splitlines()]
        self.assertEqual(ignored_paths, [".env", "tools/openclaw/.env"])


class TransportSecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        cls.ca = cls.root / "attacker-ca.pem"
        commands = [
            ["req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1",
             "-subj", "/CN=Test Attacker CA", "-addext", "basicConstraints=critical,CA:TRUE",
             "-keyout", "ca.key", "-out", "attacker-ca.pem"],
            ["req", "-newkey", "rsa:2048", "-nodes", "-subj", "/CN=api.cursor.com",
             "-keyout", "server.key", "-out", "server.csr"],
            ["x509", "-req", "-in", "server.csr", "-CA", "attacker-ca.pem", "-CAkey", "ca.key",
             "-CAcreateserial", "-days", "1", "-extfile", "server.ext", "-out", "server.pem"],
            ["rehash", str(cls.root)],
        ]
        (cls.root / "server.ext").write_text(
            "subjectAltName=DNS:api.cursor.com\nbasicConstraints=critical,CA:FALSE\nextendedKeyUsage=serverAuth\n",
            encoding="ascii",
        )
        for command in commands:
            subprocess.run(["openssl", *command], cwd=cls.root, check=True, capture_output=True)
        cls.server = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        cls.server.load_cert_chain(cls.root / "server.pem", cls.root / "server.key")

    def hostile_environment(self, keylog: Path) -> dict[str, str]:
        return {
            "HTTPS_PROXY": "http://attacker.invalid:8080", "https_proxy": "http://attacker.invalid:8080",
            "HTTP_PROXY": "http://attacker.invalid:8080", "ALL_PROXY": "http://attacker.invalid:8080",
            "NO_PROXY": "", "no_proxy": "", "SSL_CERT_FILE": str(self.ca),
            "SSL_CERT_DIR": str(self.root), "SSLKEYLOGFILE": str(keylog),
        }

    def test_proxy_and_attacker_ca_cannot_intercept_tls(self) -> None:
        keylog = self.root / "mitm-keylog"
        with mock.patch.dict(os.environ, self.hostile_environment(keylog)):
            opener = client().opener
            self.assertFalse(any(isinstance(h, urllib.request.ProxyHandler) for h in opener.handlers))
            tls = next(h._context for h in opener.handlers if isinstance(h, urllib.request.HTTPSHandler))
            self.assertEqual(tls.verify_mode, ssl.CERT_REQUIRED)
            self.assertTrue(tls.check_hostname)
            self.assertIsNone(tls.keylog_filename)
            attacker_der = ssl.PEM_cert_to_DER_cert(self.ca.read_text(encoding="ascii"))
            self.assertNotIn(attacker_der, tls.get_ca_certs(binary_form=True))
            with self.assertRaises(ssl.SSLCertVerificationError):
                handshake(tls, self.server)
            # Positive control: the same hostname and server are accepted if the
            # attacker CA is deliberately trusted, so rejection is due to trust.
            trusted = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            trusted.load_verify_locations(cafile=self.ca)
            handshake(trusted, self.server)
        self.assertFalse(keylog.exists())

    def test_hostile_environment_before_import_is_ignored(self) -> None:
        keylog = self.root / "import-keylog"
        script = """
import ssl
import sys
import urllib.request
from tools.openclaw import cursor_openclaw as cli
cfg = cli.Config('https://api.cursor.com', 'synthetic', 'bearer', 5, 0, 0, True)
opener = cli.CursorApiClient(cfg).opener
assert not any(isinstance(h, urllib.request.ProxyHandler) for h in opener.handlers)
tls = next(h._context for h in opener.handlers if isinstance(h, urllib.request.HTTPSHandler))
with open(sys.argv[1], encoding='ascii') as ca:
    attacker_der = ssl.PEM_cert_to_DER_cert(ca.read())
assert attacker_der not in tls.get_ca_certs(binary_form=True)
assert tls.verify_mode == ssl.CERT_REQUIRED and tls.check_hostname
assert tls.keylog_filename is None
sys.path.insert(0, 'tests')
from test_openclaw_security import handshake
from pathlib import Path
root = Path(sys.argv[1]).parent
server = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
server.load_cert_chain(root / 'server.pem', root / 'server.key')
try:
    handshake(tls, server)
except ssl.SSLCertVerificationError:
    pass
else:
    raise AssertionError('Attacker CA was trusted after import')
"""
        subprocess.run(
            [sys.executable, "-c", script, str(self.ca)],
            cwd=Path(__file__).resolve().parents[1],
            env={**os.environ, **self.hostile_environment(keylog)},
            check=True, capture_output=True, text=True,
        )
        self.assertFalse(keylog.exists())

    def test_missing_system_trust_does_not_fall_back_to_environment(self) -> None:
        with (
            mock.patch.dict(os.environ, self.hostile_environment(self.root / "missing-trust-keylog")),
            mock.patch.object(cli, "_SYSTEM_CA_FILE", None),
            mock.patch.object(cli, "_SYSTEM_CA_DIR", None),
        ):
            with self.assertRaisesRegex(RuntimeError, "System TLS certificate paths are unavailable"):
                client()

    def test_keylog_env_does_not_log_even_successful_handshake(self) -> None:
        keylog = self.root / "successful-keylog"
        with mock.patch.dict(os.environ, self.hostile_environment(keylog)):
            tls = cli._tls_context()
            # Test-only trust permits a completed handshake to exercise logging.
            tls.load_verify_locations(cafile=self.ca)
            handshake(tls, self.server)
            self.assertIsNone(tls.keylog_filename)
        self.assertFalse(keylog.exists())


class DiagnosticSecurityTests(unittest.TestCase):
    def test_show_key_never_outputs_any_credential_characters(self) -> None:
        for key in ("", "~", "~!@$%^&*()_+", "~" * 128):
            for json_output in (False, True):
                for flag in ([], ["--show-key"]):
                    with self.subTest(length=len(key), json=json_output, show_key=bool(flag)):
                        output = io.StringIO()
                        argv = ["cursor_openclaw.py", *(["--json"] if json_output else []), "diagnose", *flag]
                        with (
                            mock.patch.dict(os.environ, {"CURSOR_API_KEY": key}, clear=True),
                            mock.patch.object(cli, "_load_repo_dotenv"),
                            mock.patch.object(sys, "argv", argv),
                            contextlib.redirect_stdout(output),
                            contextlib.redirect_stderr(output),
                        ):
                            self.assertEqual(cli.main(), 0)
                        rendered = output.getvalue()
                        # '_' occurs in field names; compare the key field exactly
                        # and use '~' as a credential-only canary in all nonempty keys.
                        self.assertNotIn("~", rendered)
                        expected = f"set (length {len(key)})" if key else "not set"
                        if json_output:
                            self.assertEqual(json.loads(rendered)["api_key_preview"], expected)
                        else:
                            self.assertIn(f"api_key_preview: {expected}\n", rendered)


if __name__ == "__main__":
    unittest.main()
