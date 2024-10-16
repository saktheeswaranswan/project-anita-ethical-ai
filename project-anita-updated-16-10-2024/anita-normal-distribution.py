import tkinter as tk
import random
import time

class BallSimulation:
    def __init__(self, master, num_balls, num_bins):
        self.master = master
        self.num_balls = num_balls
        self.num_bins = num_bins
        self.balls = []
        self.canvas = tk.Canvas(master, width=600, height=400, bg='white')
        self.canvas.pack()
        self.bins = [0] * self.num_bins
        self.max_height = 300
        self.bin_width = self.canvas.winfo_reqwidth() / self.num_bins

    def drop_ball(self):
        ball_x = self.canvas.winfo_reqwidth() // 2
        ball_y = 0
        while ball_y < self.max_height:
            move = random.choice([-1, 1])
            ball_x += move * self.bin_width // 2
            ball_y += 5
            self.canvas.create_oval(ball_x - 2, ball_y - 2, ball_x + 2, ball_y + 2, fill='blue', outline='blue')
            self.master.update()
            time.sleep(0.01)
        bin_index = int(ball_x // self.bin_width)
        if 0 <= bin_index < self.num_bins:
            self.bins[bin_index] += 1

    def draw_bins(self):
        for i, count in enumerate(self.bins):
            x0 = i * self.bin_width
            x1 = x0 + self.bin_width
            y0 = self.canvas.winfo_reqheight()
            y1 = y0 - (count * 5)  # Scale factor for the bin height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='black')

    def run_simulation(self):
        for _ in range(self.num_balls):
            self.drop_ball()
        self.draw_bins()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Normal Distribution Ball Simulation")
    num_balls = 1000
    num_bins = 20
    sim = BallSimulation(root, num_balls, num_bins)
    sim.run_simulation()
    root.mainloop()
