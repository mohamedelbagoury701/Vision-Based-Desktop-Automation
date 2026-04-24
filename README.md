# Vision-Based Desktop Automation with Dynamic Icon Grounding 🤖

## Objective
A robust Python RPA application that uses computer vision to dynamically locate, ground, and interact with the Notepad icon on Windows, regardless of its position. It fetches posts from a JSON API and automates text entry and file management.

## Key Features ✨
- **Multimodal AI Grounding:** Uses Gemini 2.5 Flash for intelligent icon detection (returning precise x, y coordinates).
- **Graceful Degradation:** Automatic fallback to traditional computer vision (PyAutoGUI) with retry logic if the AI system is unavailable or fails.
- **Robust State Management:** - Utilizes clipboard injection (`pyperclip`) to prevent keyboard shortcut conflicts (Sticky Keys bug).
  - Uses OS-level termination (`taskkill`) to ensure a clean application state for every loop.
- **Dynamic Pathing:** Auto-detects target directories (seamlessly handles OneDrive vs. Local Desktop environments).

## Requirements & Setup 🚀
1. Ensure you have Python and `uv` installed.
2. Install dependencies:
   ```bash
   uv add pyautogui pillow google-genai pyperclip
   ```
3. Create a `.env` file in the root directory to securely store your API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage 💻
To execute the automation workflow, run:
   ```bash
   uv run vision.py
   ```

## Visual Grounding Proof 📸
As per the requirements, the repository includes 3 screenshots demonstrating the system successfully grounding the Notepad icon in different desktop locations:
1. `center.jpg` - Icon detected in the center of the screen.
2. `top_right.jpg` - Icon detected in the top-right area.
3. `bottom_left.png` - Icon detected in the bottom-left area (demonstrating successful UI interaction and text entry).
```
