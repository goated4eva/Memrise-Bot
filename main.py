import pyautogui
import time
import threading
from tkinter import Tk, Button, Label, StringVar
import keyboard  # Library to detect keypresses

# Global variables to control the program state
program_active = False
paused = False

# Set pyautogui to have no delay between actions
pyautogui.PAUSE = 0

# Path to the image of the "Hint" button
HINT_IMAGE_PATH = "hint_button.PNG"  # Use uppercase .PNG

# Define the RGB color of the "Correct" button
CORRECT_COLOR = (0, 167, 120)  # Cyan-green color
COLOR_TOLERANCE = 10  # Allow slight variations in color

# Define the coordinates to check after the 9th click
CHECK_COORDINATES = (1411, 341)  # (x, y)
FALLBACK_COORDINATES = (576, 950)  # (x, y)

def take_screenshot():
    """Take a screenshot of the screen."""
    screenshot = pyautogui.screenshot()
    return screenshot

def find_button(image_path):
    """
    Locate a button on the screen using image recognition.
    Returns the coordinates of the button if found, otherwise None.
    """
    try:
        print(f"Looking for button: {image_path}")
        button_location = pyautogui.locateOnScreen(image_path, confidence=0.7)  # Lower confidence
        if button_location:
            print(f"Button found at: {button_location}")
            return pyautogui.center(button_location)
        else:
            print(f"Button not found on the screen: {image_path}")
            return None
    except Exception as e:
        print(f"Error finding button: {e}")
        return None

def get_pixel_color(x, y):
    """
    Get the color of the pixel at the specified coordinates.
    Returns the RGB color as a tuple.
    """
    try:
        screenshot = take_screenshot()
        pixel_color = screenshot.getpixel((x, y))
        return pixel_color
    except Exception as e:
        print(f"Error getting pixel color: {e}")
        return None

def click_target_positions():
    """Click at the predefined positions in the specified order."""
    global paused

    # Find the "Hint" button dynamically
    hint_position = find_button(HINT_IMAGE_PATH)
    if not hint_position:
        print("Skipping cycle because Hint button was not found.")
        # Click the fallback coordinates
        pyautogui.moveTo(FALLBACK_COORDINATES[0], FALLBACK_COORDINATES[1])
        pyautogui.click()
        print(f"Clicked fallback coordinates: {FALLBACK_COORDINATES}")
        return

    # Click Hint 9 times
    for i in range(1, 10):  # Loop from 1 to 9
        if not program_active or paused:  # Stop if program is toggled off or paused
            break
        pyautogui.moveTo(hint_position.x, hint_position.y)
        pyautogui.click()
        print(f"Clicked 'Hint' ({i}/9)...")
        if i == 9:
            time.sleep(0.1)  # Small delay between clicks

    # Move to the coordinates (x=1411, y=341)
    pyautogui.moveTo(CHECK_COORDINATES[0], CHECK_COORDINATES[1])
    print(f"Moved to coordinates: {CHECK_COORDINATES}")

    # Check the color at the coordinates
    pixel_color = get_pixel_color(CHECK_COORDINATES[0], CHECK_COORDINATES[1])
    if pixel_color and all(abs(pixel_color[i] - CORRECT_COLOR[i]) <= COLOR_TOLERANCE for i in range(3)):
        print(f"Color at {CHECK_COORDINATES} matches the target color: {pixel_color}")
        pyautogui.click()  # Click if the color matches
    else:
        print(f"Color at {CHECK_COORDINATES} does not match the target color: {pixel_color}")
        # Search for the "Hint" button again
        hint_position = find_button(HINT_IMAGE_PATH)
        if hint_position:
            pyautogui.moveTo(hint_position.x, hint_position.y)
            pyautogui.click()
            print("Clicked the 'Hint' button.")
        else:
            # Move to fallback coordinates and click
            pyautogui.moveTo(FALLBACK_COORDINATES[0], FALLBACK_COORDINATES[1])
            pyautogui.click()
            print(f"Clicked fallback coordinates: {FALLBACK_COORDINATES}")

def toggle_program_state():
    """Toggle the program state on/off or pause/resume."""
    global program_active, paused

    if not program_active:
        # Start the program if it's not active
        program_active = True
        paused = False
        status_var.set("Program is RUNNING")
        print("Program started.")
        # Start the clicking process in a separate thread
        threading.Thread(target=run_program_logic, daemon=True).start()
    else:
        if paused:
            # Resume the program if it's paused
            paused = False
            status_var.set("Program is RUNNING")
            print("Program resumed.")
        else:
            # Pause the program if it's running
            paused = True
            status_var.set("Program is PAUSED")
            print("Program paused.")

# Function to handle F9 keypress
def on_f9_press(event):
    """Toggle program state when F9 is pressed."""
    toggle_program_state()

def run_program_logic():
    """Run the program logic in a loop."""
    while program_active:
        if not paused:
            click_target_positions()

# Create the UI
root = Tk()
root.title("Auto Memrise Bot")
root.geometry("300x150")

# Status label
status_var = StringVar()
status_var.set("Program is OFF")
status_label = Label(root, textvariable=status_var, font=("Arial", 14))
status_label.pack(pady=10)

# Toggle button
toggle_button = Button(root, text="Toggle", command=toggle_program_state, font=("Arial", 12))
toggle_button.pack(pady=10)

# Listen for F9 keypress
keyboard.on_press_key("Z", on_f9_press)

# Run the UI
root.mainloop()