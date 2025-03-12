HOW IT WORKS
USE AN ADBLOCKER FOR PEACE OF MIND
PRESS IGNORE ALL AND SAVE
PRESS IGNORE NONE
PRESS IGNORE ALL AND UNCHECK ONE WORD
REVIEW THAT WORD AND COUNT HOW MANY TIMES YOU NEED TO CLICK FOR THE LESSON TO END

RUN THIS COMMAND IN CMD OR TERMINAL
pip install opencv-python-headless

Lines 8-11 on main.py:
run coordinates.py and place the mouse cursor over the buttons you want to find the coordinates of
get the coordinates and place them in where they are supposed to be for lines 8-11

line 35 main.py :    for i in range(1, x+1): 
x is how many times it will click the hint button

line 38 main.py:       print(f"Clicking 'Hint' ({i}/x)...")
change x to how many times you want the hint button to be pressed

line 40 main.py       time.sleep(x)  # Short delay between clicks
set x to the delay in seconds you want it to have between clicks on the hint button

main.py lines 42-45
set x to how long the program should sleep

    # Wait x seconds
    if program_active and not paused:
        print("Waiting x seconds...")
        time.sleep(x)
