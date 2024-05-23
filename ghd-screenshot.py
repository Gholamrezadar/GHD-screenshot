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

# Function to take a screenshot
def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
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
    timestamp = datetime.datetime.now().strftime("%Y-%d-%m-%H-%M")
    default_filename = f"{timestamp}.png"

    file_path = filedialog.asksaveasfilename(
        initialdir=default_dir,
        initialfile=default_filename,
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    if file_path:
        cropped_image.save(file_path)
        print(f"> Cropped screenshot saved to {file_path}.")
    root.destroy()

def main():
    # Step 0: Take a screenshot of the screen
    screenshot = take_screenshot()
    print("> Screenshot taken.")
    
    # Initialize pygame
    pygame.init()
    print("> Pygame initialized.")

    # Step 1: Start a pygame window with the screenshot as the background
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
    screen = pygame.display.set_mode((960, 540))
    pygame.display.set_caption('Screenshot Cropper')
    screenshot_image = pygame.image.load("screenshot.png")
    screenshot_surface = pygame.transform.scale(screenshot_image, (960, 540))
    screen.blit(screenshot_surface, (0, 0))
    pygame.display.flip()
    print("> Screenshot is displayed in a pygame window.")

    # Variables for rectangle drawing
    drawing = False
    start_pos = None
    end_pos = None

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
                    rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))

                    # Step 3: Get the coordinates of the rectangle
                    x1, y1 = rect.topleft
                    x2, y2 = rect.bottomright

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
                    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])), 2)
                    pygame.display.flip()

if __name__ == "__main__":
    main()
