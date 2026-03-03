# Project: EchoPulse (Local STT)
**Status:** MVP Functional (Phase 1 & 2 Complete)
**Hardware:** MacBook Pro M3 Max (64GB Unified Memory)
**Objective:** High-speed, private, local speech-to-text with "Hold-to-Record" global hotkey functionality.

---

## 🏗 Current Architecture
- **Engine:** `mlx-whisper` (optimized for Apple Silicon).
- **Model:** `whisper-large-v3-turbo` (loaded into Unified Memory).
- **Audio Capture:** `sounddevice` + `scipy` (16kHz Mono).
- **Global Control:** `pynput` listening for `Right Command` (cmd_r).
- **Integration:** `pyperclip` + `osascript` (AppleScript) for automated GUI pasting.
- **Data Logging:** Automatic storage of `.wav` and `.txt` pairs in `/training_data` for future fine-tuning.

---

## 🚀 Execution
Single entry point (run via `uv` for dependencies):

```bash
uv run main.py
```

Or after installing the project: `echopulse` (see `pyproject.toml` scripts).

---

## 🛠 Features Implemented
1. **Hold-to-Record:** Logic implemented via `on_press` and `on_release` with a boolean gate (`is_held`) to prevent trigger-spamming.
2. **Audio UI (Earcons):**
   - **Start:** `Tink.aiff` (Subtle bloop).
   - **End:** `Glass.aiff` (High-pitched success bleep).
3. **Automated Pasting:** Copies result to clipboard and triggers `Cmd+V` globally using AppleScript.
4. **Local Privacy:** 0% cloud dependency; data never leaves the M3 chip.

---

## 📈 Next Steps (The "Phase 3" Roadmap)

### 1. Smart Formatting (The "Snake_Case" Problem)
To handle technical speech (e.g., saying "main dot p-y" and getting `main.py` or "process audio function" and getting `process_audio`), we have two paths:
- **Option A (System Prompting):** Use the `initial_prompt` parameter in Whisper to bias the model toward code-friendly formatting. 
  - *Example:* `mlx_whisper.transcribe(path, initial_prompt="Use snake_case for functions and file extensions.")`
- **Option B (The LLM Refiner):** Pass the raw Whisper output to a local **Llama 3** (via Ollama) with a system prompt: *"You are a technical editor. Convert spoken descriptions of functions or files into snake_case and keep the rest as natural speech."*

### 2. Fine-Tuning (Acoustic Optimization)
If the model consistently fails on specific names or jargon:
- Use the collected `training_data/` folder.
- Use **MLX-LoRA** to train a lightweight adapter. This "patches" the model without needing to retrain the whole 1.5GB base.

### 3. Background Persistence (Launch Agent)
To move away from an open Terminal window:
- Create a `com.echopulse.plist` file in `~/Library/LaunchAgents`.
- This will allow the script to run as a "Daemon" (background process) that starts at login.

### 4. System Extension (The Menu Bar)
Consider wrapping the Python script in **Rumps** (a Python library for macOS menu bar apps) to give it a visual "On/Off" indicator in the top right of your screen.

---

## 📝 Developer Notes for Future AI
- **Memory Management:** The M3 Max handles `large-v3` easily. Do not downgrade to `base` or `small` unless latency exceeds 2 seconds.
- **Permissions:** If pasting fails, check **System Settings > Privacy & Security > Accessibility** for both Terminal and `/usr/bin/osascript`.
- **Audio Device:** If an external mic is plugged in, `sounddevice` might need an explicit device ID mapping.
- **Dependencies:** Managed via `uv`. Key libraries: `mlx-whisper`, `sounddevice`, `pynput`, `pyperclip`.
- **Optional scripts:** `archive/record_and_transcribe.py` — interactive record-then-transcribe (Enter to start/stop). Not needed for the main hold-to-record flow.
- **Clipboard preservation (idea):** Current approach overwrites the clipboard with the transcript, so a later Cmd+V can re-paste the transcript instead of what the user copied.
  - **Simple fix (plain text only):** Save current clipboard (`pbpaste`), set transcript, trigger paste, then restore the saved clipboard after a short delay. Downside: restores only plain text (can lose rich formatting/images).
  - **Robust fix (preserve rich clipboard):** Use macOS `NSPasteboard` (via `pyobjc`) to snapshot/restore all available pasteboard types (RTF/HTML/images/etc.) around the paste action.
  - **Alternative:** Avoid clipboard entirely by “typing” the transcript via accessibility/keystroke injection (slower; may behave differently in some apps).