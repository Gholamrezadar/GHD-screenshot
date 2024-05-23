# TODO:
# 0. take a screenshot of the screen.
# 1. start a pygame window with the screenshot as the background. full screen no border.
# 2. allow the user to draw a rectangle on the screen with the mouse.
# 3. get the coordinates of the rectangle.
# 4. crop the screenshot to the rectangle.
# 5. open up a file save dialog defaulting to a custom directory.
# 6. save the cropped screenshot to the directory.
# 7. close the pygame window.
# 8. exit the program.


import pygame
import sys
import os
import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab, Image
import datetime

CUSTOM_DIR = "~/Pictures/Screenshots"
WINDOW_SIZE = (960, 540)
SCREEN_SIZE = (1920, 1080)
# get the screen size from the system

# Function to take a screenshot
def take_screenshot(window_size=(960, 540)):
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    screenshot_resized = screenshot.resize(window_size, Image.BILINEAR)
    # make the screenshot a little darker
    screenshot_resized = screenshot_resized.point(lambda p: p * 0.85)
    screenshot_resized.save("screenshot_resized.png")
    return screenshot

# Function to crop the screenshot
def crop_image(screenshot, rect):
    cropped_image = screenshot.crop(rect)
    return cropped_image

# Function to show file save dialog
def save_file_dialog(default_dir, cropped_image):
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Generate the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%d-%m-%H-%M-%S")
    default_filename = f"{timestamp}.png"

    file_path = filedialog.asksaveasfilename(
        initialdir=default_dir,
        initialfile=default_filename,
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )

    if file_path:
        cropped_image.save(file_path)
        print(f"> Cropped screenshot saved to {file_path}. size: {cropped_image.size}")
    root.destroy()

def take_gui_screenshot():
    # Step 0: Take a screenshot of the screen
    screenshot = take_screenshot(window_size=WINDOW_SIZE)
    print("> Screenshot taken.")

    # Step 1: Start a pygame window with the screenshot as the background
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.NOFRAME)
    pygame.display.set_caption('Screenshot Cropper')
    screenshot_image = pygame.image.load("screenshot_resized.png")
    # screenshot_surface = pygame.transform.scale(screenshot_image, WINDOW_SIZE)
    screenshot_surface = screenshot_image.convert()
    screen.blit(screenshot_surface, (0, 0))
    pygame.display.flip()
    print("> Screenshot is displayed in a pygame window.")

    # Variables for rectangle drawing
    drawing = False
    start_pos = (0, 0)
    end_pos = WINDOW_SIZE

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    drawing = True
                    start_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    drawing = False
                    end_pos = event.pos

                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))

                    # Get the coordinates of the rectangle
                    x1, y1 = rect.topleft
                    x2, y2 = rect.bottomright

                    # Convert from window coordinates to screen coordinates
                    x1 = int(x1 * SCREEN_SIZE[0] / WINDOW_SIZE[0])
                    y1 = int(y1 * SCREEN_SIZE[1] / WINDOW_SIZE[1])
                    x2 = int(x2 * SCREEN_SIZE[0] / WINDOW_SIZE[0])
                    y2 = int(y2 * SCREEN_SIZE[1] / WINDOW_SIZE[1])

                    # Step 4: Crop the screenshot to the rectangle
                    cropped_image = crop_image(screenshot, (x1, y1, x2, y2))

                    # Step 5: Open up a file save dialog defaulting to a custom directory
                    default_dir = os.path.expanduser(CUSTOM_DIR)
                    if not os.path.exists(default_dir):
                        os.makedirs(default_dir)

                    save_file_dialog(default_dir, cropped_image)

                    # Step 7: Close the pygame window
                    pygame.quit()

                    # Step 8: Exit the program
                    sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    end_pos = event.pos
                    screen.blit(screenshot_surface, (0, 0))
                    # draw the rectangle no matter which corner we start
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                    LINE_WIDTH = 1
                    LINE_COLOR = (255, 0, 0) # red
                    pygame.draw.rect(screen, LINE_COLOR, rect, LINE_WIDTH)

                    pygame.display.flip()


def main():
    global WINDOW_SIZE
    global SCREEN_SIZE

    # Initialize pygame
    pygame.init()
    print("> Pygame initialized.")
    SCREEN_SIZE = pygame.display.Info().current_w, pygame.display.Info().current_h
    WINDOW_SIZE = SCREEN_SIZE
    print(f"Screen size: {SCREEN_SIZE}")
    print(f"window size: {WINDOW_SIZE}")

    take_gui_screenshot()

if __name__ == "__main__":
    main()
