import tkinter as tk
import time
import datetime
import pytz

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.configure(bg='black')  # Set background color to black
        self.root.geometry("800x600")    # Set an initial size for the window
        self.root.resizable(True, True)  # Make the window resizable
        
        self.running = True
        self.target_time = self.get_target_time()

        # Title Label ("Remaining Time:")
        self.title_label = tk.Label(
            self.root,
            text="Remaining Time:",
            font=("Helvetica", 24),  # Smaller font size for the title
            fg="white",    # White text color
            bg="black",    # Black background
        )
        self.title_label.pack(pady=10)  # Add some padding above the title

        # Label for displaying the time
        self.time_display = tk.Label(
            self.root,
            text="00:00:00",
            font=("Helvetica", 150),  # Initial large font size
            fg="white",    # White text color
            bg="black",    # Black background
            width=10,
            height=2
        )
        self.time_display.pack(padx=20, pady=20, expand=True)

        # Control buttons
        self.reset_button = tk.Button(
            self.root,
            text="Reset",
            font=("Helvetica", 20),
            command=self.reset_timer
        )
        self.reset_button.pack(side="left", padx=10)

        # Update the timer's font size dynamically
        self.root.bind("<Configure>", self.resize_font)

        self.update_timer()

    def get_target_time(self):
        """Returns the target time (December 18, 4 PM EST)"""
        # Create a timezone for EST (Eastern Standard Time)
        est = pytz.timezone("US/Eastern")
        
        # Set the target time: December 18, 4 PM
        target_time = datetime.datetime(2024, 12, 18, 16, 0, 0, 0)  # 4:00 PM on December 18
        target_time = est.localize(target_time)  # Localize to EST

        return target_time

    def resize_font(self, event=None):
        """Dynamically resize the font so that the entire width of the text is 75% of the window's width."""
        width = event.width
        
        # Time format "hh:mm:ss" has 8 characters
        text = "00:00:00"
        num_chars = len(text)
        
        # Calculate the font size to make the text width 75% of the window width
        target_width = width * 0.75
        
        # Estimate the width of the text. This depends on the font and number of characters.
        # For simplicity, let's assume an average character width of around 0.6 for each character in the "00:00:00" string.
        avg_char_width = 0.6  # This is an estimate, may vary slightly depending on the font
        total_text_width = num_chars * avg_char_width * 100  # Initial font size of 100
        
        # Calculate the font size so that the text width fits within 75% of the window width
        font_size = int((target_width / total_text_width) * 100)  # Scale by 100 to match the initial size

        # Set a reasonable minimum and maximum font size to avoid being too small or too large
        font_size = max(80, min(font_size, 400))

        # Update the font size
        self.time_display.config(font=("Helvetica", font_size))

    def reset_timer(self):
        """Resets the timer to the target time."""
        self.target_time = self.get_target_time()

    def update_timer(self):
        """Updates the countdown timer display"""
        now = datetime.datetime.now(pytz.timezone("US/Eastern"))  # Get current time in EST
        remaining_time = self.target_time - now
        
        if remaining_time.total_seconds() <= 0:
            self.time_display.config(text="00:00:00")
            self.running = False
        else:
            hours = int(remaining_time.total_seconds() // 3600)
            minutes = int((remaining_time.total_seconds() % 3600) // 60)
            seconds = int(remaining_time.total_seconds() % 60)
            
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.time_display.config(text=time_str)
        
        # Update the countdown every 1000ms (1 second)
        if self.running:
            self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
