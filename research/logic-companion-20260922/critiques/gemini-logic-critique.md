Here are 8 complete bullet points regarding the WebJam desktop app companion to Logic Pro:

*   The WebJam desktop companion app will facilitate the export of individual stems and MIDI data directly to a user-specified folder, ready for seamless import into Logic Pro.
*   A core feature will be the automatic muting of WebJam's local audio output whenever Logic Pro's Record LED is actively engaged.
*   This mute detection will be implemented by monitoring Mackie Control feedback messages transmitted over an IAC MIDI bus from Logic Pro.
*   The highest risk for echo or bleed arises from WebJam's local audio output inadvertently mixing with Logic Pro's input, especially during recording sessions.
*   **Acceptance Test:** With WebJam playing audio, arm a track in Logic Pro and press record; WebJam's local audio must immediately cease playing.
*   This automatic muting is critical to prevent unwanted feedback loops or the recording of WebJam's output directly into Logic Pro, ensuring clean takes.
*   Integration with virtual audio drivers like BlackHole is considered an optional future enhancement for more advanced routing, but not part of the initial release.
*   Development of a phone-based remote control for WebJam is currently parked and will not be included in the initial desktop app release.
