import tkinter as tk
import random
import time
import math

class BallSimulation:
    def __init__(self, master, num_balls, num_bins):
        self.master = master
        self.num_balls = num_balls
        self.num_bins = num_bins
        self.canvas_width = 1080
        self.canvas_height = 720
        self.balls = []
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()
        self.bins = [0] * self.num_bins
        self.max_height = self.canvas_height - 100  # Leave space for the histogram
        self.bin_width = self.canvas_width / self.num_bins
        self.gravity = 0.5
        self.fixed_circle_radius = 50
        self.fixed_circle_center = (self.canvas_width // 2, self.canvas_height // 3)
        self.create_fixed_circle()

    def create_fixed_circle(self):
        x, y = self.fixed_circle_center
        r = self.fixed_circle_radius
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='red', outline='black')

    def ball_hits_circle(self, ball_x, ball_y):
        # Check if the ball hits the fixed circle using distance formula
        circle_x, circle_y = self.fixed_circle_center
        distance = math.sqrt((ball_x - circle_x)**2 + (ball_y - circle_y)**2)
        return distance <= self.fixed_circle_radius

    def drop_ball(self):
        ball_x = self.canvas_width // 2
        ball_y = 0
        velocity_y = 0
        ball_size = 4
        ball = self.canvas.create_oval(ball_x - ball_size, ball_y - ball_size, 
                                       ball_x + ball_size, ball_y + ball_size, 
                                       fill='blue', outline='blue')
        
        while ball_y < self.max_height:
            velocity_y += self.gravity
            ball_y += velocity_y
            
            move = random.choice([-1, 1])
            ball_x += move * self.bin_width // 4
            
            # Check collision with the fixed circle
            if self.ball_hits_circle(ball_x, ball_y):
                # Make the ball "bounce" off the circle by reversing velocity and applying damping
                velocity_y = -velocity_y * 0.7
                ball_y += velocity_y
            
            # Update the ball's position
            self.canvas.coords(ball, ball_x - ball_size, ball_y - ball_size, 
                               ball_x + ball_size, ball_y + ball_size)
            self.master.update()
            time.sleep(0.01)
        
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
        for i in range(self.num_balls):
            self.drop_ball()
            self.draw_bins()  # Update the histogram as balls fall

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ball Collision and Normal Distribution Simulation")
    num_balls = 500
    num_bins = 40
    sim = BallSimulation(root, num_balls, num_bins)
    sim.run_simulation()
    root.mainloop()
