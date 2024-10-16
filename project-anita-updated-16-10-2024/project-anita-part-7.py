import tkinter as tk
import random
import math
import time

class BallSimulation:
    def __init__(self, master, num_balls, num_bins):
        self.master = master
        self.num_balls = num_balls
        self.num_bins = num_bins
        self.canvas_width = 1080
        self.canvas_height = 720
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()
        self.bins = [0] * self.num_bins
        self.max_height = self.canvas_height - 100  # Leave space for the histogram
        self.bin_width = self.canvas_width / self.num_bins
        self.gravity = 1.2
        self.red_ball_radius = 5
        self.blue_ball_radius = 4
        self.red_balls = []
        self.create_evenly_spaced_red_balls()
        self.animation_direction = 1  # Direction of vertical compression/expansion

    def create_evenly_spaced_red_balls(self):
        num_rows = 10  # Number of rows for red balls
        num_columns = 15  # Number of columns for red balls
        horizontal_spacing = self.canvas_width // (num_columns + 1)
        vertical_spacing = 50

        for i in range(num_rows):
            row = []
            for j in range(num_columns):
                x = (j + 1) * horizontal_spacing
                y = (self.canvas_height // 2 - (num_rows // 2) * vertical_spacing) + i * vertical_spacing
                
                red_ball = self.canvas.create_oval(x - self.red_ball_radius, y - self.red_ball_radius,
                                                   x + self.red_ball_radius, y + self.red_ball_radius,
                                                   fill='red', outline='black')
                row.append((red_ball, x, y))
            self.red_balls.append(row)

    def animate_red_balls(self):
        # Compress and expand the rows of red balls vertically
        vertical_shift = 10  # Maximum shift amount for compression/expansion
        speed = 0.05  # Speed of animation

        while True:
            for row_index, row in enumerate(self.red_balls):
                shift_amount = math.sin(time.time() + row_index) * vertical_shift * self.animation_direction
                for red_ball, x, original_y in row:
                    new_y = original_y + shift_amount
                    self.canvas.coords(red_ball, x - self.red_ball_radius, new_y - self.red_ball_radius,
                                       x + self.red_ball_radius, new_y + self.red_ball_radius)
            self.master.update_idletasks()
            time.sleep(speed)

    def ball_hits_red_ball(self, ball_x, ball_y):
        for row in self.red_balls:
            for red_ball, red_x, red_y in row:
                if abs(ball_x - red_x) <= self.red_ball_radius + self.blue_ball_radius and \
                   abs(ball_y - red_y) <= self.red_ball_radius + self.blue_ball_radius:
                    distance = math.sqrt((ball_x - red_x)**2 + (ball_y - red_y)**2)
                    if distance <= (self.red_ball_radius + self.blue_ball_radius):
                        return True, (red_x, red_y)
        return False, (0, 0)

    def drop_ball(self):
        ball_x = self.canvas_width // 2
        ball_y = 0
        velocity_y = 0
        ball_size = self.blue_ball_radius
        ball = self.canvas.create_oval(ball_x - ball_size, ball_y - ball_size,
                                       ball_x + ball_size, ball_y + ball_size,
                                       fill='blue', outline='blue')
        
        while ball_y < self.max_height:
            velocity_y += self.gravity
            ball_y += velocity_y
            move = random.choice([-1, 1])
            ball_x += move * (self.bin_width // 8)
            
            # Check collision with red balls
            hit, (red_x, red_y) = self.ball_hits_red_ball(ball_x, ball_y)
            if hit:
                velocity_y = -velocity_y * 0.5  # Apply damping for bounce
                if ball_y < red_y:
                    ball_y = red_y - (self.red_ball_radius + ball_size)
                else:
                    ball_y = red_y + (self.red_ball_radius + ball_size)
            
            self.canvas.coords(ball, ball_x - ball_size, ball_y - ball_size,
                               ball_x + ball_size, ball_y + ball_size)
            self.master.update_idletasks()  # Update the GUI

        # Determine which bin the ball falls into
        bin_index = int(ball_x // self.bin_width)
        if 0 <= bin_index < self.num_bins:
            self.bins[bin_index] += 1

    def draw_bins(self):
        # Clear the previous histogram
        self.canvas.delete("bin")
        for i, count in enumerate(self.bins):
            x0 = i * self.bin_width
            x1 = x0 + self.bin_width
            y0 = self.canvas_height
            y1 = y0 - (count * 5)  # Scale factor for the bin height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='black', tags="bin")

    def run_simulation(self):
        self.master.after(0, self.animate_red_balls)  # Run red ball animation in parallel
        for i in range(self.num_balls):
            self.drop_ball()
            self.draw_bins()  # Update the histogram as balls fall

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fast Ball Collision and Normal Distribution Simulation")
    num_balls = 500
    num_bins = 40
    sim = BallSimulation(root, num_balls, num_bins)
    sim.run_simulation()
    root.mainloop()
