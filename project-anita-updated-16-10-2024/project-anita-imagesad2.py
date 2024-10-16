import tkinter as tk
import random
import math
import csv
from PIL import Image, ImageTk

class BallSimulation:
    def __init__(self, master, num_balls, num_bins):
        self.master = master
        self.num_balls = num_balls
        self.num_bins = num_bins
        self.canvas_width = 1080
        self.canvas_height = 720
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height - 250, bg='white')
        self.canvas.pack(side=tk.TOP)
        self.bins = [0] * self.num_bins
        self.max_height = self.canvas_height - 250  # Leave space for the histogram
        self.bin_width = self.canvas_width / self.num_bins
        self.gravity = 0.5
        self.red_ball_radius = 5
        self.anita_image = Image.open(r"C:\Users\Admin\Videos\anita.png")
        self.anita_image = self.anita_image.resize((40, 40), Image.LANCZOS)  # Resize image
        self.anita_photo = ImageTk.PhotoImage(self.anita_image)
        self.red_balls = []
        self.colors = ["red", "green", "blue", "orange", "purple", "cyan", "magenta", "yellow"]
        self.create_red_balls()

        # Create a canvas for the histogram
        self.histogram_canvas = tk.Canvas(master, width=320, height=230, bg='lightgrey')
        self.histogram_canvas.pack(side=tk.BOTTOM, anchor='ne')  # Anchor to the bottom right corner

    def create_red_balls(self):
        # Place red balls evenly spaced across the canvas
        for i in range(self.num_bins):
            x = (i + 0.5) * self.bin_width  # Center of each bin
            y = random.randint(self.canvas_height // 2 - 50, self.canvas_height // 2 + 50)  # Randomize y position
            red_ball = self.canvas.create_oval(x - self.red_ball_radius, y - self.red_ball_radius,
                                                x + self.red_ball_radius, y + self.red_ball_radius,
                                                fill='red', outline='black')
            self.red_balls.append((x, y))

    def ball_hits_red_ball(self, ball_x, ball_y):
        for index, (red_x, red_y) in enumerate(self.red_balls):
            if abs(ball_x - red_x) <= self.red_ball_radius + self.red_ball_radius and \
               abs(ball_y - red_y) <= self.red_ball_radius + self.red_ball_radius:
                distance = math.sqrt((ball_x - red_x)**2 + (ball_y - red_y)**2)
                if distance <= (self.red_ball_radius + self.red_ball_radius):
                    return True, (red_x, red_y), index  # Return index of the red ball hit
        return False, (0, 0), -1  # -1 if no ball hit

    def drop_ball(self):
        ball_x = random.randint(0, self.canvas_width - 40)  # Random horizontal start
        ball_y = 0
        velocity_y = 0

        # Create the anita.png ball
        ball = self.canvas.create_image(ball_x, ball_y, image=self.anita_photo)

        update_interval = 5  # Only update canvas every few frames for efficiency
        frame_count = 0

        # Keep track of red balls hit
        hit_red_balls = set()

        while ball_y < self.max_height:
            velocity_y += self.gravity
            ball_y += velocity_y
            move = random.choice([-1, 1])
            ball_x += move * self.bin_width // 4
            
            # Check collision with red balls
            hit, (red_x, red_y), red_index = self.ball_hits_red_ball(ball_x, ball_y)
            if hit:
                hit_red_balls.add(red_index)  # Track the hit red ball
                velocity_y = -velocity_y * 0.7  # Apply damping
                if ball_y < red_y:
                    ball_y = red_y - self.red_ball_radius
                else:
                    ball_y = red_y + self.red_ball_radius

            # Ensure all red balls are hit at least once
            if len(hit_red_balls) == len(self.red_balls):
                break
            
            frame_count += 1
            if frame_count % update_interval == 0:
                # Only update every 'update_interval' frames to reduce canvas redraws
                self.canvas.coords(ball, ball_x, ball_y)  # Update position of the anita image
                self.master.update()
        
        # Update the final position of the ball
        self.canvas.coords(ball, ball_x, ball_y)
        self.master.update()
        
        # Determine which bin the ball falls into
        bin_index = int(ball_x // self.bin_width)
        if 0 <= bin_index < self.num_bins:
            self.bins[bin_index] += 1

    def draw_bins(self):
        # Clear the previous histogram
        self.histogram_canvas.delete("bin")
        for i, count in enumerate(self.bins):
            x0 = (i * 320 / self.num_bins)
            x1 = x0 + (320 / self.num_bins)
            y0 = 230
            y1 = y0 - (count * 4)  # Scale factor for the bin height
            color = self.colors[i % len(self.colors)]  # Cycle through the colors list
            self.histogram_canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags="bin")

    def run_simulation(self):
        for _ in range(self.num_balls):
            self.drop_ball()
        self.draw_bins()  # Draw the histogram after all balls have dropped
        self.save_to_csv()

    def save_to_csv(self):
        with open('hit_history.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Bin", "Count"])  # CSV header
            for index, count in enumerate(self.bins):
                writer.writerow([index, count])  # Record bin index and count

if __name__ == "__main__":
    root = tk.Tk()
    num_balls = 10000  # Number of balls to drop
    num_bins = 40  # Number of histogram bins
    sim = BallSimulation(root, num_balls, num_bins)
    sim.run_simulation()
    root.mainloop()
