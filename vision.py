import os
import json
import pyautogui
import time
from PIL import Image
from google import genai
from google.genai import types
import pyperclip
import task


API_KEY = os.getenv("GEMINI_API_KEY")  # Replace with your actual API key

USE_AI_VISION = False


def locate_icon_ai(max_retries=3):
    print("Waking up AI Vision : Gemini-2.5-flash")
    screen_path = "screenshot.png"
    pyautogui.screenshot(screen_path)

    client = genai.Client(api_key=API_KEY)
    img = Image.open(screen_path)

    prompt = """
    Find the 'Notepad' application icon on the desktop. 
    Calculate its exact center coordinates as percentages of the total screen width and height.
    Return ONLY a valid JSON object in this exact format: {"x_percent": 50.5, "y_percent": 20.1}
    """

    for attempt in range(max_retries):
        try:
            print(f"[*] AI Attempt {attempt + 1}/{max_retries}...")
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[img, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
            )
            data = json.loads(response.text)

            screen_width, screen_height = pyautogui.size()
            x = int((data["x_percent"] / 100) * screen_width)
            y = int((data["y_percent"] / 100) * screen_height)
            return x, y

        except Exception as e:
            if attempt < max_retries - 1:
                print(f"[-] AI Vision Failed Attempt {attempt + 1}: Retrying...")
                time.sleep(2)
    return None, None


def locate_icon_traditional(max_retries=3):
    print("Using Traditional Computer Vision to locate the icon...")
    icon_path = "notepad_icon.png"
    for attempt in range(max_retries):
        try:
            print(f"[*] Traditional Attempt {attempt + 1}/{max_retries}...")
            locationx, locationy = pyautogui.locateCenterOnScreen(
                icon_path, confidence=0.75
            )

            if locationx is not None and locationy is not None:
                print(f"Traditional Vision found icon at: X={locationx}, Y={locationy}")
                return locationx, locationy
            else:
                print(f"[-] Icon not found using traditional method in attempt {attempt + 1}.")
                time.sleep(1)
    
        except Exception as e:
            print(f"[-] Traditional Vision Error: {e}")
            time.sleep(1)
    return None, None

def smart_locate_icon():
    if USE_AI_VISION:
        x, y = locate_icon_ai()
        if x is not None and y is not None:
            return x, y
        else:
            print(
                "[-] AI Vision failed to locate the icon. Falling back to traditional method."
            )

    return locate_icon_traditional()


def type_title_and_body(post_id, title, body):
    print("Validating Notepad launch...")
    launched = False
    for _ in range(5): # Timeout after 5 seconds
        active_window = pyautogui.getActiveWindowTitle()
        if active_window and "Notepad" in active_window:
            launched = True
            break
        time.sleep(1)
        
    if not launched:
        print("[-] Warning: Notepad might not be the active window!")
    time.sleep(1)
    pyautogui.hotkey("ctrl", "n")
    title = f"Title {post_id} : {title}\n\n"
    body = f"Body {post_id} : {body}\n\n"
    pyperclip.copy(title)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    time.sleep(1)
    pyperclip.copy(body)
    pyautogui.hotkey("ctrl", "v")


def next_post(post_id):
    pyautogui.hotkey("ctrl", "s")
    user_profile = os.path.expanduser("~")
    onedrive_desktop = os.path.join(user_profile, "OneDrive", "Desktop")
    local_desktop = os.path.join(user_profile, "Desktop")
    base_desktop = (
        onedrive_desktop if os.path.exists(onedrive_desktop) else local_desktop
    )

    desktop_path = os.path.join(base_desktop, "tjm-project")
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)

    file_path = os.path.join(desktop_path, f"post_{post_id}.txt")

    if os.path.exists(file_path):
        os.remove(file_path)

    pyperclip.copy(file_path)
    time.sleep(1)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(1)
    os.system("taskkill /f /im notepad.exe >nul 2>&1")
    time.sleep(1)


if __name__ == "__main__":
    pyautogui.hotkey("win", "d")
    posts = task.fetching_posts()
    if posts:
        for idx, (title, body) in enumerate(task.get_post_titles_bodies(posts), 1):
            x, y = smart_locate_icon()
            if x is not None and y is not None:
                pyautogui.moveTo(x, y, duration=1)
                pyautogui.doubleClick()
            else:
                print(
                    f"Failed to locate the icon using both methods while starting iteration {idx}."
                )
                break
            time.sleep(0.5)
            type_title_and_body(idx, title, body)
            time.sleep(0.5)
            next_post(idx)
        print("All posts processed successfully.")
        print(f"Total execution time of fetching posts: {task.fetching_posts.last_exec_time:.2f} seconds")
    else:
        print("Failed to fetch posts.")


