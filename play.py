import tkinter as tk
from PIL import Image, ImageTk
import os
import random

class ChordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chord Practice")
        
        # Make window stay on top
        self.root.attributes('-topmost', True)

        # Set window size and position
        window_width = 800
        window_height = 600
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Calculate position coordinates
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # Set window size and position
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Label to display images
        self.image_label = tk.Label(root)
        self.image_label.pack(padx=20, pady=20)  # Increased padding

        # Create a frame to hold the buttons and position it at the bottom
        button_frame = tk.Frame(root)
        button_frame.pack(side="bottom", pady=20)

        # Start and Stop buttons in the button frame
        self.start_button = tk.Button(button_frame, text="Start", command=self.start_slideshow)
        self.start_button.pack(side="left", padx=5)

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_slideshow)
        self.stop_button.pack(side="left", padx=5)

        self.running = False
        self.images = []
        self.previous_image_index = -1

        self.load_images()

    def load_images(self):
        # Determine the folder path for the Chords folder
        base_dir = os.path.dirname(os.path.abspath(__file__))
        chords_folder = os.path.join(base_dir, "Chords")

        # Load images that match common image extensions
        for filename in os.listdir(chords_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_path = os.path.join(chords_folder, filename)
                try:
                    image = Image.open(image_path)
                    # Optionally, you can resize the image here if needed
                    photo = ImageTk.PhotoImage(image)
                    self.images.append(photo)
                except Exception as e:
                    print(f"Failed to load image {filename}: {e}")

        if not self.images:
            print("No images were loaded from the 'Chords' folder.")

    def start_slideshow(self):
        if not self.images:
            return  # Do nothing if there are no images
        if not self.running:
            self.running = True
            self.show_next_image()

    def stop_slideshow(self):
        self.running = False

    def show_next_image(self):
        if not self.running:
            return

        # Choose a random index that is not the same as the previous one
        if len(self.images) == 1:
            index = 0
        else:
            index = self.previous_image_index
            while index == self.previous_image_index:
                index = random.randint(0, len(self.images) - 1)

        self.previous_image_index = index

        # Update the label with the new image
        self.image_label.config(image=self.images[index])
        
        # Schedule the next image after 3000 milliseconds (3 seconds)
        self.root.after(3000, self.show_next_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChordApp(root)
    root.mainloop()