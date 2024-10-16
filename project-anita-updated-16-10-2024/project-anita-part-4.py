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
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()
        self.bins = [0] * self.num_bins
        self.max_height = self.canvas_height - 100  # Leave space for the histogram
        self.bin_width = self.canvas_width / self.num_bins
        self.gravity = 0.5
        self.red_ball_radius = 5
        self.blue_ball_radius = 4
        self.red_balls = []
        self.create_red_balls()

    def create_red_balls(self):
        # Arrange red balls randomly in the middle part of the canvas
        num_rows = random.randint(3, 5)  # Random number of rows
        num_columns = random.randint(5, 10)  # Random number of columns
        for i in range(num_rows):
            for j in range(num_columns):
                # Random position offsets to create arbitrary patterns
                x_offset = random.randint(-20, 20)
                y_offset = random.randint(-20, 20)
                x = (self.canvas_width // 2 - num_columns * 20) + j * 40 + x_offset
                y = (self.canvas_height // 2 - num_rows * 20) + i * 40 + y_offset
                
                red_ball = self.canvas.create_oval(x - self.red_ball_radius, y - self.red_ball_radius, 
                                                   x + self.red_ball_radius, y + self.red_ball_radius, 
                                                   fill='red', outline='black')
                self.red_balls.append((x, y))

    def ball_hits_red_ball(self, ball_x, ball_y):
        for red_x, red_y in self.red_balls:
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
            ball_x += move * self.bin_width // 4
            
            # Check collision with red balls
            hit, (red_x, red_y) = self.ball_hits_red_ball(ball_x, ball_y)
            if hit:
                # Reflect the velocity upon hitting the red ball
                velocity_y = -velocity_y * 0.7  # Apply damping
                # Adjust the ball position to simulate bouncing off the red ball
                if ball_y < red_y:
                    ball_y = red_y - (self.red_ball_radius + ball_size)
                else:
                    ball_y = red_y + (self.red_ball_radius + ball_size)
            
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
