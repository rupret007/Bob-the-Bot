#!/usr/bin/env python3
"""Vendored, cleaned OpenClaw fallback CLI for Cursor Cloud Agents APIs.

Native Cursor Cloud Agent tools should be used first. This CLI is a fallback
for operators who need direct endpoint access.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import cursor_api_common  # noqa: E402
import env_loader  # noqa: E402

VERSION = "1.0.0"


def _load_repo_dotenv() -> None:
    repo_root = _SCRIPT_DIR.parent.parent
    env_loader.merge_dotenv_paths([repo_root / ".env", Path.cwd() / ".env"], override=False)


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "y"}:
        return True
    if lowered in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"Invalid boolean value: {value!r}. Use true|false.")


def normalize_base_url(raw: str | None) -> str:
    base = (raw or "https://api.cursor.com").strip()
    if not base:
        base = "https://api.cursor.com"
    lowered = base.lower()
    if not lowered.startswith(("http://", "https://")):
        raise ValueError("Base URL must start with http:// or https://.")
    return base.rstrip("/")


@dataclass
class Config:
    base_url: str
    api_key: str
    auth_mode: str
    timeout_seconds: int
    retries: int
    retry_backoff_seconds: float
    output_json: bool


class CursorApiClient:
    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg

    def _auth_headers(self, mode: str) -> dict[str, str]:
        if mode == "bearer":
            return {"Authorization": f"Bearer {self.cfg.api_key}"}
        if mode == "basic":
            token = base64.b64encode(f"{self.cfg.api_key}:".encode("utf-8")).decode("ascii")
            return {"Authorization": f"Basic {token}"}
        raise ValueError(f"Unsupported auth mode: {mode}")

    def _request_once(
        self,
        method: str,
        path: str,
        query: dict[str, str] | None,
        body: dict[str, Any] | None,
        mode: str,
    ) -> tuple[int, dict[str, Any], str]:
        url = f"{self.cfg.base_url}{path}"
        if query:
            url += "?" + urllib.parse.urlencode(query)
        payload: bytes | None = None
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": cursor_api_common.USER_AGENT_OPENCLAW,
        }
        headers.update(self._auth_headers(mode))
        if body is not None:
            payload = cursor_api_common.encode_request_json(body)

        req = urllib.request.Request(url=url, data=payload, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=self.cfg.timeout_seconds) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                data = cursor_api_common.parse_json_response_body(raw)
                return resp.status, data, raw
        except urllib.error.HTTPError as err:
            try:
                raw = err.read().decode("utf-8", errors="replace")
            except Exception as read_err:  # noqa: BLE001
                raw = f"<unreadable HTTP error body: {read_err}>"
            try:
                data = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                data = {"raw": raw}
            return err.code, data, raw
        except (urllib.error.URLError, TimeoutError, ConnectionError, BrokenPipeError, OSError) as err:
            msg = str(err)
            return cursor_api_common.TRANSIENT_TRANSPORT_STATUS, {"error": msg}, msg

    def request(
        self,
        method: str,
        path: str,
        query: dict[str, str] | None = None,
        body: dict[str, Any] | None = None,
    ) -> tuple[int, dict[str, Any], str, str]:
        auth_order = ["bearer", "basic"] if self.cfg.auth_mode == "auto" else [self.cfg.auth_mode]
        last: tuple[int, dict[str, Any], str, str] = (0, {}, "", auth_order[0])
        for mode in auth_order:
            attempt = 0
            while True:
                status, data, raw = self._request_once(method, path, query, body, mode)
                last = (status, data, raw, mode)
                retryable = status in {429, 500, 502, 503, 504, cursor_api_common.TRANSIENT_TRANSPORT_STATUS}
                if retryable and attempt < self.cfg.retries:
                    time.sleep(self.cfg.retry_backoff_seconds * (2**attempt))
                    attempt += 1
                    continue
                break
            if self.cfg.auth_mode == "auto" and status in {401, 403} and mode != auth_order[-1]:
                continue
            return status, data, raw, mode
        return last


def print_out(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")


def require_one_of(repo: str, pr_url: str) -> None:
    has_r = bool((repo or "").strip())
    has_p = bool((pr_url or "").strip())
    if has_r and has_p:
        raise ValueError("Pass only one of --repository or --pr-url (not both).")
    if not has_r and not has_p:
        raise ValueError("Provide --repository or --pr-url.")


def build_create_payload(args: argparse.Namespace) -> dict[str, Any]:
    source: dict[str, Any]
    if args.pr_url:
        source = {"prUrl": args.pr_url}
    else:
        source = {"repository": args.repository}
        if args.ref:
            source["ref"] = args.ref

    target: dict[str, Any] = {"branchName": args.branch_name, "autoCreatePr": args.auto_create_pr}
    if args.auto_create_pr:
        target["openAsCursorGithubApp"] = args.open_as_cursor_github_app
        if args.open_as_cursor_github_app:
            target["skipReviewerRequest"] = args.skip_reviewer_request

    return {
        "prompt": {"text": args.prompt.strip()},
        "model": args.model,
        "source": source,
        "target": target,
    }


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", default=os.getenv("CURSOR_BASE_URL", "https://api.cursor.com"))
    parser.add_argument("--auth-mode", choices=["auto", "basic", "bearer"], default=os.getenv("CURSOR_AUTH_MODE", "auto"))
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--retry-backoff-seconds", type=float, default=0.5)
    parser.add_argument("--json", action="store_true")


def validate_common_args(args: argparse.Namespace) -> None:
    if args.timeout_seconds <= 0:
        raise ValueError("--timeout-seconds must be > 0")
    if args.retries < 0:
        raise ValueError("--retries must be >= 0")
    if args.retry_backoff_seconds < 0:
        raise ValueError("--retry-backoff-seconds must be >= 0")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_args(parser)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("whoami")
    sub.add_parser("models")

    p_list = sub.add_parser("list-agents")
    p_list.add_argument("--limit", default="20")
    p_list.add_argument("--cursor", default="")
    p_list.add_argument("--pr-url", default="")

    p_status = sub.add_parser("agent-status")
    p_status.add_argument("--id", required=True)

    p_conv = sub.add_parser("conversation")
    p_conv.add_argument("--id", required=True)

    p_art = sub.add_parser("artifacts")
    p_art.add_argument("--id", required=True)

    p_art_dl = sub.add_parser("artifact-download-url")
    p_art_dl.add_argument("--id", required=True)
    p_art_dl.add_argument("--path", required=True)

    p_create = sub.add_parser("create-agent")
    p_create.add_argument("--prompt", default="")
    p_create.add_argument("--repository", default="")
    p_create.add_argument("--ref", default="")
    p_create.add_argument("--pr-url", default="")
    p_create.add_argument("--model", default="default")
    p_create.add_argument("--branch-name", required=True)
    p_create.add_argument("--auto-create-pr", type=parse_bool, default=False)
    p_create.add_argument("--open-as-cursor-github-app", type=parse_bool, default=False)
    p_create.add_argument("--skip-reviewer-request", type=parse_bool, default=False)
    p_create.add_argument("--dry-run", action="store_true")

    p_follow = sub.add_parser("followup")
    p_follow.add_argument("--id", required=True)
    p_follow.add_argument("--prompt", required=True)
    p_follow.add_argument("--dry-run", action="store_true")

    p_stop = sub.add_parser("stop-agent")
    p_stop.add_argument("--id", required=True)

    p_stop_all = sub.add_parser("stop-all-jobs")
    p_stop_all.add_argument("--repo", default=".")
    p_stop_all.add_argument("--limit", default="100")
    p_stop_all.add_argument("--max-pages", type=int, default=10)
    p_stop_all.add_argument("--include-terminal", action="store_true")
    p_stop_all.add_argument("--dry-run", action="store_true")
    p_stop_all.add_argument("--yes", action="store_true")

    p_delete = sub.add_parser("delete-agent")
    p_delete.add_argument("--id", required=True)

    p_diag = sub.add_parser("diagnose")
    p_diag.add_argument("--show-key", action="store_true")
    return parser.parse_args()


def _run_subprocess(args: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(args, cwd=str(cwd), text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def _normalize_github_remote(url: str) -> str:
    value = (url or "").strip()
    if value.startswith("git@github.com:"):
        value = "https://github.com/" + value.split("git@github.com:", 1)[1]
    if value.endswith(".git"):
        value = value[:-4]
    return value.rstrip("/")


def _detect_repo_origin_url(repo_path: Path) -> str:
    code, out, err = _run_subprocess(["git", "remote", "get-url", "origin"], cwd=repo_path)
    if code != 0 or not out.strip():
        raise ValueError(f"Could not determine repo origin URL from {repo_path}. {err.strip()}")
    return _normalize_github_remote(out.strip())


def _agent_page_cursor(data: dict[str, Any]) -> str:
    cursors: list[str] = []
    for key in ("nextCursor", "cursor"):
        if key not in data:
            continue
        raw = data[key]
        if not isinstance(raw, str):
            raise RuntimeError(f"list-agents returned non-string {key}")
        value = raw.strip()
        if value:
            cursors.append(value)
    if len(set(cursors)) > 1:
        raise RuntimeError("list-agents returned conflicting pagination cursors")
    return cursors[0] if cursors else ""


def _iter_agents(client: CursorApiClient, *, limit: int, max_pages: int) -> tuple[list[dict[str, Any]], bool]:
    agents: list[dict[str, Any]] = []
    cursor = ""
    complete = False
    for _ in range(max(1, max_pages)):
        query: dict[str, str] = {"limit": str(limit)}
        if cursor:
            query["cursor"] = cursor
        status, data, raw, _auth_mode = client.request("GET", "/v0/agents", query=query)
        if status >= 400:
            raise RuntimeError(f"list-agents failed (HTTP {status}): {data or raw}")
        page = data.get("agents") if isinstance(data, dict) else None
        if not isinstance(page, list):
            raise RuntimeError("list-agents response omitted the agents list")
        cursor = _agent_page_cursor(data)
        if not page:
            complete = not cursor
            break
        for item in page:
            if isinstance(item, dict):
                agents.append(item)
        if not cursor:
            complete = True
            break
    return agents, complete


def _agent_source_repository(agent: dict[str, Any]) -> str:
    source = agent.get("source") if isinstance(agent.get("source"), dict) else {}
    repo = source.get("repository")
    return _normalize_github_remote(str(repo or ""))


def handle(cfg: Config, args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    client = CursorApiClient(cfg)

    if args.command == "diagnose":
        payload = {
            "ok": True,
            "cli_version": VERSION,
            "base_url": cfg.base_url,
            "auth_mode": cfg.auth_mode,
            "timeout_seconds": cfg.timeout_seconds,
            "retries": cfg.retries,
            "api_key_present": bool(cfg.api_key),
            "api_key_preview": (f"{cfg.api_key[:2]}***{cfg.api_key[-2:]}" if args.show_key and len(cfg.api_key) > 8 else "***"),
            "policy": {
                "native_cloud_agents_preferred": True,
                "cli_fallback_only": True,
                "no_andrea_sync": True,
                "no_gateway_launch_agent_copy": True,
                "no_secret_bootstrapping": True,
                "no_auto_send": True,
            },
        }
        return 0, payload

    if args.command == "whoami":
        status, data, raw, auth_mode = client.request("GET", "/v0/me")
        return status, {"status": status, "auth_mode": auth_mode, "response": data or raw}

    if args.command == "models":
        status, data, raw, auth_mode = client.request("GET", "/v0/models")
        return status, {"status": status, "auth_mode": auth_mode, "response": data or raw}

    if args.command == "list-agents":
        limit = int(str(args.limit))
        if limit < 1 or limit > 100:
            raise ValueError("--limit must be an integer between 1 and 100.")
        query: dict[str, str] = {"limit": str(limit)}
        if args.cursor:
            query["cursor"] = args.cursor
        if args.pr_url:
            query["prUrl"] = args.pr_url
        status, data, raw, auth_mode = client.request("GET", "/v0/agents", query=query)
        return status, {"status": status, "auth_mode": auth_mode, "response": data or raw}

    if args.command == "agent-status":
        cursor_api_common.validate_agent_id(args.id)
        status, data, raw, auth_mode = client.request("GET", f"/v0/agents/{args.id}")
        return status, {"status": status, "auth_mode": auth_mode, "response": data or raw}

    if args.command == "conversation":
        cursor_api_common.validate_agent_id(args.id)
        status, data, raw, auth_mode = client.request("GET", f"/v0/agents/{args.id}/conversation")
        return status, {"status": status, "auth_mode": auth_mode, "response": data or raw}

    if args.command == "artifacts":
        cursor_api_common.validate_agent_id(args.id)
        status, data, raw, auth_mode = client.request("GET", f"/v0/agents/{args.id}/artifacts")
        return status, {"status": status, "auth_mode": auth_mode, "response": data or raw}

    if args.command == "artifact-download-url":
        cursor_api_common.validate_agent_id(args.id)
        status, data, raw, auth_mode = client.request(
            "GET",
            f"/v0/agents/{args.id}/artifacts/download",
            query={"path": args.path},
        )
        return status, {"status": status, "auth_mode": auth_mode, "response": data or raw}

    if args.command == "create-agent":
        require_one_of(args.repository, args.pr_url)
        if not args.prompt.strip():
            raise ValueError("create-agent requires --prompt.")
        payload = build_create_payload(args)
        if args.dry_run:
            return 0, {"status": 0, "dry_run": True, "would_send": False, "payload": payload}
        status, data, raw, auth_mode = client.request("POST", "/v0/agents", body=payload)
        return status, {"status": status, "auth_mode": auth_mode, "response": data or raw}

    if args.command == "followup":
        cursor_api_common.validate_agent_id(args.id)
        body = {"prompt": {"text": args.prompt}}
        if args.dry_run:
            return 0, {
                "status": 0,
                "dry_run": True,
                "would_send": False,
                "agent_id": args.id,
                "payload": body,
            }
        status, data, raw, auth_mode = client.request("POST", f"/v0/agents/{args.id}/followup", body=body)
        return status, {"status": status, "auth_mode": auth_mode, "response": data or raw}

    if args.command == "stop-agent":
        cursor_api_common.validate_agent_id(args.id)
        status, data, raw, auth_mode = client.request("POST", f"/v0/agents/{args.id}/stop")
        return status, {"status": status, "auth_mode": auth_mode, "response": data or raw}

    if args.command == "stop-all-jobs":
        limit = int(str(args.limit))
        if limit < 1 or limit > 100:
            raise ValueError("--limit must be an integer between 1 and 100.")
        if args.max_pages <= 0:
            raise ValueError("--max-pages must be > 0")

        repo_path = Path(str(args.repo or ".")).expanduser().resolve()
        if not repo_path.is_dir():
            raise ValueError(f"--repo must be an existing directory: {repo_path}")
        target_repo = _detect_repo_origin_url(repo_path)
        agents, scan_complete = _iter_agents(client, limit=limit, max_pages=args.max_pages)
        matches = [ag for ag in agents if _agent_source_repository(ag) == target_repo]
        include_terminal = bool(args.include_terminal)
        to_stop: list[dict[str, Any]] = []
        for ag in matches:
            status = str(ag.get("status") or "").strip().upper()
            if status in cursor_api_common.TERMINAL_AGENT_STATUSES and not include_terminal:
                continue
            to_stop.append(ag)

        dry_run = bool(args.dry_run) or not bool(args.yes)
        results: list[dict[str, Any]] = []
        if not dry_run and scan_complete:
            for ag in to_stop:
                agent_id = str(ag.get("id") or "").strip()
                if not agent_id:
                    results.append({"id": "", "ok": False, "error": "missing_agent_id"})
                    continue
                status, data, raw, auth_mode = client.request("POST", f"/v0/agents/{agent_id}/stop")
                results.append({"id": agent_id, "http_status": status, "auth_mode": auth_mode, "ok": status < 400, "response": data or raw})

        if not scan_complete:
            command_status = 409
            note = "Agent scan hit --max-pages before cursor ended; increase --max-pages and retry."
        else:
            command_status = 0 if all(bool(r.get("ok", True)) for r in results) else 502
            note = "Pass --yes to execute stops." if dry_run and not args.dry_run else ""

        return command_status, {
            "status": command_status,
            "ok": command_status == 0,
            "dry_run": dry_run,
            "scan_complete": scan_complete,
            "repo_origin": target_repo,
            "matched": len(matches),
            "eligible_to_stop": len(to_stop),
            "attempted": len(results),
            "stopped": sum(1 for r in results if bool(r.get("ok"))),
            "failed_to_stop": sum(1 for r in results if not bool(r.get("ok"))),
            "note": note,
            "results": results,
        }

    if args.command == "delete-agent":
        cursor_api_common.validate_agent_id(args.id)
        status, data, raw, auth_mode = client.request("DELETE", f"/v0/agents/{args.id}")
        return status, {"status": status, "auth_mode": auth_mode, "response": data or raw}

    raise ValueError(f"Unsupported command: {args.command}")


def main() -> int:
    _load_repo_dotenv()
    if len(sys.argv) == 2 and sys.argv[1] in ("--version", "-V"):
        print(f"cursor_openclaw {VERSION}")
        return 0

    args = parse_args()
    try:
        validate_common_args(args)
        api_key = (os.getenv("CURSOR_API_KEY") or "").strip()
        if args.command != "diagnose" and not api_key:
            raise RuntimeError("CURSOR_API_KEY is required.")
        cfg = Config(
            base_url=normalize_base_url(args.base_url),
            api_key=api_key,
            auth_mode=args.auth_mode,
            timeout_seconds=args.timeout_seconds,
            retries=max(0, args.retries),
            retry_backoff_seconds=max(0.0, args.retry_backoff_seconds),
            output_json=args.json,
        )
        status, payload = handle(cfg, args)
        payload["ok"] = status < 400
        print_out(payload, as_json=cfg.output_json)
        return 0 if status < 400 else 4
    except Exception as err:  # noqa: BLE001
        payload = {"ok": False, "error": str(err)}
        print_out(payload, as_json=cursor_api_common.argv_has_json_flag())
        return 2


if __name__ == "__main__":
    sys.exit(main())
