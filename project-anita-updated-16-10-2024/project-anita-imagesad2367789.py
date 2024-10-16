import tkinter as tk
import random
import math
import csv
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class BallSimulation:
    def __init__(self, master, num_balls, num_bins):
        self.master = master
        self.num_balls = num_balls
        self.num_bins = num_bins
        self.canvas_width = 1080
        self.canvas_height = 720
        
        # Main canvas for everything
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()
        
        self.bins = [0] * self.num_bins
        self.max_height = self.canvas_height - 250  # Leave space for the histogram
        self.bin_width = self.canvas_width / self.num_bins
        self.gravity = 0.5
        self.red_ball_radius = 5
        
        # Load and resize Anita image
        self.anita_image = Image.open(r"C:\Users\Admin\Videos\anita.png")
        self.anita_image = self.anita_image.resize((40, 40), Image.LANCZOS)  # Resize image
        self.anita_photo = ImageTk.PhotoImage(self.anita_image)
        
        self.red_balls = []
        self.create_red_balls()
        
        # Create separate canvas for histogram
        self.histogram_canvas = tk.Canvas(master, width=self.canvas_width, height=250, bg='lightgrey')
        self.histogram_canvas.pack()

    def create_red_balls(self):
        # Create a grid for red balls to simulate a uniform distribution
        num_rows = 5
        num_columns = self.num_bins // num_rows
        
        # Calculate spacing
        spacing_x = self.canvas_width / num_columns
        spacing_y = (self.canvas_height // 2) / num_rows
        
        for i in range(num_rows):
            for j in range(num_columns):
                x = (j + 0.5) * spacing_x
                y = (i + 0.5) * spacing_y + 50  # Offset for visual appeal
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
                self.canvas.coords(ball, ball_x, ball_y)  # Update position of the Anita image
                self.master.update()
        
        # Update the final position of the ball
        self.canvas.coords(ball, ball_x, ball_y)
        self.master.update()
        
        # Determine which bin the ball falls into
        bin_index = int(ball_x // self.bin_width)
        if 0 <= bin_index < self.num_bins:
            self.bins[bin_index] += 1

            # Stack Anita images in the histogram area
            self.add_anita_to_histogram(bin_index)

    def add_anita_to_histogram(self, bin_index):
        # Position for Anita image in histogram
        x = (bin_index + 0.5) * self.bin_width
        # Calculate the vertical position based on how many are stacked
        y = self.canvas_height - 50 - (self.bins[bin_index] * 5)  # Scale to fit the canvas
        self.canvas.create_image(x, y, image=self.anita_photo)

    def draw_bins(self):
        # Clear the previous histogram
        self.histogram_canvas.delete("bin")
        max_bin_height = max(self.bins) if self.bins else 1  # Avoid division by zero
        scale_factor = 200 / max_bin_height  # Scale to fit in the canvas height

        for i, count in enumerate(self.bins):
            x0 = (i * self.bin_width)
            x1 = x0 + self.bin_width
            y0 = 250  # Start from the bottom of the histogram canvas
            y1 = y0 - (count * scale_factor)  # Scale factor for the bin height
            color = f'#{random.randint(0, 0xFFFFFF):06x}'  # Random color for each bin
            self.histogram_canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black', tags="bin")

    def save_histogram_as_png(self):
        # Create a histogram plot
        plt.figure(figsize=(10, 5))  # Set figure size
        plt.bar(range(self.num_bins), self.bins, color=[f'#{random.randint(0, 0xFFFFFF):06x}' for _ in range(self.num_bins)])
        plt.title("Histogram of Anita Counts")
        plt.xlabel("Bins")
        plt.ylabel("Counts")
        plt.xticks(range(self.num_bins))
        plt.yticks(range(0, max(self.bins) + 1, 5))
        
        # Save the figure
        plt.savefig("histogram.png")
        plt.close()

    def save_to_pdf(self):
        # Save the PNG as a PDF in A0 format
        from matplotlib.backends.backend_pdf import PdfPages

        with PdfPages('histogram.pdf') as pdf:
            # Create a new figure
            plt.figure(figsize=(33.1, 46.8))  # A0 size in inches
            plt.bar(range(self.num_bins), self.bins, color=[f'#{random.randint(0, 0xFFFFFF):06x}' for _ in range(self.num_bins)])
            plt.title("Histogram of Anita Counts")
            plt.xlabel("Bins")
            plt.ylabel("Counts")
            plt.xticks(range(self.num_bins))
            plt.yticks(range(0, max(self.bins) + 1, 5))
            pdf.savefig()  # saves the current figure into a pdf page
            plt.close()

    def run_simulation(self):
        for _ in range(self.num_balls):
            self.drop_ball()
        self.draw_bins()  # Draw the histogram after all balls have dropped
        self.save_histogram_as_png()  # Save the histogram as PNG
        self.save_to_pdf()  # Save the histogram as PDF

if __name__ == "__main__":
    root = tk.Tk()
    num_balls = 10000  # Number of balls to drop
    num_bins = 40  # Number of histogram bins
    sim = BallSimulation(root, num_balls, num_bins)
    sim.run_simulation()
    root.mainloop()
