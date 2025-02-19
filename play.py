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

        # Set window size and position (unchanged)
        window_width = 800
        window_height = 600
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Label to display images
        self.image_label = tk.Label(root)
        self.image_label.pack(padx=20, pady=20)

        # Add label for upcoming chord name
        self.upcoming_label = tk.Label(root, text="", font=("Arial", 12))
        self.upcoming_label.pack(pady=10)

        # Create a main frame for all controls at the bottom
        control_frame = tk.Frame(root)
        control_frame.pack(side="bottom", pady=10)

        # Play timer section (first row)
        timer_display_frame = tk.Frame(control_frame)
        timer_display_frame.pack(side="top", pady=5)
        
        self.play_countdown_label = tk.Label(timer_display_frame, text="", font=("Arial", 14))
        self.play_countdown_label.pack(pady=5)

        play_frame = tk.Frame(control_frame)
        play_frame.pack(side="top", pady=5)
        
        play_label = tk.Label(play_frame, text="Play timer (min):")
        play_label.pack(side="left", padx=2)
        
        self.play_timer_var = tk.StringVar(value="3")
        self.play_entry = tk.Entry(play_frame, textvariable=self.play_timer_var, width=5)
        self.play_entry.pack(side="left", padx=2)
        
        self.play_button = tk.Button(play_frame, text="Start", command=self.start_play_timer)
        self.play_button.pack(side="left", padx=2)
        
        self.pause_play_button = tk.Button(play_frame, text="Pause", command=self.pause_play_timer)
        self.pause_play_button.pack(side="left", padx=2)
        
        self.reset_play_button = tk.Button(play_frame, text="Reset", command=self.reset_play_timer)
        self.reset_play_button.pack(side="left", padx=2)

        # Slideshow controls section (second row)
        slideshow_frame = tk.Frame(control_frame)
        slideshow_frame.pack(side="top", pady=5)

        timer_label = tk.Label(slideshow_frame, text="Seconds per image:")
        timer_label.pack(side="left", padx=2)
        
        self.timer_var = tk.StringVar(value="3")
        self.timer_entry = tk.Entry(slideshow_frame, textvariable=self.timer_var, width=5)
        self.timer_entry.pack(side="left", padx=2)

        self.start_button = tk.Button(slideshow_frame, text="Start", command=self.start_slideshow)
        self.start_button.pack(side="left", padx=2)

        self.stop_button = tk.Button(slideshow_frame, text="Stop", command=self.stop_slideshow)
        self.stop_button.pack(side="left", padx=2)

        # Initialize variables
        self.running = False
        self.images = []
        self.previous_image_index = -1
        self.next_image_index = -1
        self.play_timer_running = False
        self.play_seconds_remaining = 0

        self.load_images()

    def load_images(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        chords_folder = os.path.join(base_dir, "Chords")

        for filename in os.listdir(chords_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_path = os.path.join(chords_folder, filename)
                try:
                    image = Image.open(image_path)
                    photo = ImageTk.PhotoImage(image)
                    self.images.append((photo, filename))
                except Exception as e:
                    print(f"Failed to load image {filename}: {e}")

        if not self.images:
            print("No images were loaded from the 'Chords' folder.")

    def start_slideshow(self):
        if not self.images:
            return
        if not self.running:
            self.running = True
            self.show_next_image()

    def stop_slideshow(self):
        self.running = False

    def get_timer_value(self):
        """Get and validate slideshow timer value, return milliseconds"""
        try:
            seconds = float(self.timer_var.get())
            if seconds <= 0:
                print("Invalid slideshow timer value. Using default of 3 seconds.")
                self.timer_var.set("3")
                return 3000
            return int(seconds * 1000)
        except ValueError:
            print("Invalid slideshow timer value. Using default of 3 seconds.")
            self.timer_var.set("3")
            return 3000

    def show_next_image(self):
        if not self.running:
            return

        if self.next_image_index != -1:
            index = self.next_image_index
            self.previous_image_index = index
        else:
            if len(self.images) == 1:
                index = 0
            else:
                index = self.previous_image_index
                while index == self.previous_image_index:
                    index = random.randint(0, len(self.images) - 1)
            self.previous_image_index = index

        if len(self.images) == 1:
            self.next_image_index = 0
        else:
            self.next_image_index = self.previous_image_index
            while self.next_image_index == self.previous_image_index:
                self.next_image_index = random.randint(0, len(self.images) - 1)

        current_image, _ = self.images[index]
        self.image_label.config(image=current_image)

        next_image, next_filename = self.images[self.next_image_index]
        self.upcoming_label.config(text=f"Upcoming chord: {next_filename}")
        
        delay = self.get_timer_value()
        self.root.after(delay, self.show_next_image)

    def start_play_timer(self):
        """Start or resume the play countdown timer"""
        if not self.play_timer_running:
            # If no time has been set yet (initial start)
            if self.play_seconds_remaining == 0:
                try:
                    minutes = float(self.play_timer_var.get())
                    if minutes <= 0:
                        print("Invalid play timer value. Using default of 3 minutes.")
                        self.play_timer_var.set("3")
                        minutes = 3
                    self.play_seconds_remaining = int(minutes * 60)
                except ValueError:
                    print("Invalid play timer value. Using default of 3 minutes.")
                    self.play_timer_var.set("3")
                    self.play_seconds_remaining = 180  # 3 minutes
            self.play_timer_running = True
            self.update_play_timer()

    def pause_play_timer(self):
        """Pause the play timer, keeping current time displayed"""
        self.play_timer_running = False
        # Current time remains displayed as set by update_play_timer

    def reset_play_timer(self):
        """Reset the play timer to initial value"""
        self.play_timer_running = False
        self.play_seconds_remaining = 0
        self.play_countdown_label.config(text="")
        try:
            minutes = float(self.play_timer_var.get())
            if minutes <= 0:
                self.play_timer_var.set("3")
        except ValueError:
            self.play_timer_var.set("3")

    def update_play_timer(self):
        """Update the play timer display and countdown"""
        if self.play_timer_running and self.play_seconds_remaining > 0:
            mins = self.play_seconds_remaining // 60
            secs = self.play_seconds_remaining % 60
            self.play_countdown_label.config(text=f"Play: {mins:02d}:{secs:02d}")
            self.play_seconds_remaining -= 1
            self.root.after(1000, self.update_play_timer)
        elif self.play_timer_running:
            self.play_timer_running = False
            self.play_countdown_label.config(text="Practice time's up!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChordApp(root)
    root.mainloop()