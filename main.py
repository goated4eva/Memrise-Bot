import pyautogui
import time
import threading
from tkinter import Tk, Button, Label, StringVar, Entry
import keyboard  # Library to detect keypresses

# Global variables to control the program state
program_active = False
paused = False
wait_time = 1  # Default wait time per click
toggle_key = "z"  # Default toggle key

# Set pyautogui to have no delay between actions
pyautogui.PAUSE = 0

# Path to the image of the "Hint" button
HINT_IMAGE_PATH = "hint_button.PNG"  # Use uppercase .PNG

# Define the RGB color of the "Correct" button
CORRECT_COLOR = (0, 167, 120)  # Cyan-green color
COLOR_TOLERANCE = 7  # Allow slight variations in color

# Define the coordinates to check after the 9th click
CHECK_COORDINATES = (1425, 290)  # (x, y) of the correct! button
FALLBACK_COORDINATES = (584, 948)  # (x, y) of the classic review button 

def take_screenshot():
    """Take a screenshot of the screen."""
    screenshot = pyautogui.screenshot()
    return screenshot

def find_button(image_path):
    """Locate a button on the screen using image recognition. Returns the coordinates of the button if found, otherwise None."""
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
    """Get the color of the pixel at the specified coordinates. Returns the RGB color as a tuple."""
    try:
        screenshot = take_screenshot()
        pixel_color = screenshot.getpixel((x, y))
        return pixel_color
    except Exception as e:
        print(f"Error getting pixel color: {e}")
        return None

def click_target_positions():
    """Click at the predefined positions in the specified order."""
    global paused, wait_time

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
        print(f"Clicked 'Hint' ({i}/9)")
        time.sleep(wait_time)

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
            # If the "Hint" button is not found, wait 1 second and try again up to 4 times
            for attempt in range(4):
                time.sleep(2)
                hint_position = find_button(HINT_IMAGE_PATH)
                if hint_position:
                    pyautogui.moveTo(hint_position.x, hint_position.y)
                    pyautogui.click()
                    print("Clicked the 'Hint' button.")
                    break
                elif attempt == 3:
                    # If the "Hint" button is not found after 4 attempts, press F5 to refresh the page
                    keyboard.press_and_release('f5')
                    print("Pressed F5 to refresh the page.")
                    time.sleep(10)  # Wait for the page to refresh

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

def update_wait_time():
    """Update the wait time per click."""
    global wait_time
    try:
        wait_time = float(wait_time_entry.get())
        print(f"Wait time updated to: {wait_time} seconds")
    except ValueError:
        print("Invalid input for wait time. Please enter a number.")

def update_toggle_key():
    """Update the toggle key."""
    global toggle_key
    new_key = toggle_key_entry.get().lower()
    if new_key:
        toggle_key = new_key
        keyboard.unhook_all()  # Remove previous keybind
        keyboard.on_press_key(toggle_key, on_z_press)  # Set new keybind
        print(f"Toggle key updated to: {toggle_key}")
    else:
        print("Invalid input for toggle key. Please enter a single character.")

def on_z_press(event):
    """Toggle program state when the toggle key is pressed."""
    toggle_program_state()

def run_program_logic():
    """Run the program logic in a loop."""
    while program_active:
        if not paused:
            click_target_positions()

# Create the UI
root = Tk()
root.title("Auto Memrise Bot")
root.geometry("300x200")

# Status label
status_var = StringVar()
status_var.set("Program is OFF")
status_label = Label(root, textvariable=status_var, font=("Arial", 14))
status_label.pack(pady=10)

# Wait time input
wait_time_label = Label(root, text="Wait time per click (seconds):", font=("Arial", 10))
wait_time_label.pack()
wait_time_entry = Entry(root)
wait_time_entry.insert(0, str(wait_time))
wait_time_entry.pack()

# Update wait time button
update_wait_time_button = Button(root, text="Update Wait Time", command=update_wait_time, font=("Arial", 10))
update_wait_time_button.pack(pady=5)

# Toggle key input
toggle_key_label = Label(root, text="Toggle key:", font=("Arial", 10))
toggle_key_label.pack()
toggle_key_entry = Entry(root)
toggle_key_entry.insert(0, toggle_key)
toggle_key_entry.pack()

# Update toggle key button
update_toggle_key_button = Button(root, text="Update Toggle Key", command=update_toggle_key, font=("Arial", 10))
update_toggle_key_button.pack(pady=5)

# Toggle button
toggle_button = Button(root, text="Toggle", command=toggle_program_state, font=("Arial", 12))
toggle_button.pack(pady=10)

# Listen for the initial toggle keypress
keyboard.on_press_key(toggle_key, on_z_press)

# Run the UI
root.mainloop()
