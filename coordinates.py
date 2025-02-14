import pyautogui
import keyboard  # Library to detect keypresses

def get_mouse_position_and_color():
    """Get the mouse position and the color of the pixel at that position."""
    # Get the current mouse position
    mouse_position = pyautogui.position()
    print("Current mouse position:", mouse_position)

    # Take a screenshot and get the color of the pixel at the mouse position
    screenshot = pyautogui.screenshot()
    pixel_color = screenshot.getpixel(mouse_position)  # Returns (R, G, B)

    print("Color at mouse position (RGB):", pixel_color)

# Wait for the "Z" key to be pressed
print("Press 'Z' to get the mouse position and color...")
keyboard.wait("z")  # Wait until the "Z" key is pressed

# Run the function when "Z" is pressed
get_mouse_position_and_color()