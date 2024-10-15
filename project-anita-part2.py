import tkinter as tk
import random
import time

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
        self.gravity = 0.98

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
            ball_x += move * self.bin_width // 2
            
            # Update the ball's position
            self.canvas.coords(ball, ball_x - ball_size, ball_y - ball_size, 
                               ball_x + ball_size, ball_y + ball_size)
            self.master.update()
            time.sleep(0.01)
        
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
    root.title("Normal Distribution Ball Simulation")
    num_balls = 500
    num_bins = 40
    sim = BallSimulation(root, num_balls, num_bins)
    sim.run_simulation()
    root.mainloop()
