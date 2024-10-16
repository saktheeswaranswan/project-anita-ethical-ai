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
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack(side=tk.TOP)
        self.bins = [0] * self.num_bins
        self.max_height = self.canvas_height - 200  # Leave space for the histogram
        self.bin_width = self.canvas_width / self.num_bins
        self.gravity = 0.5
        self.red_ball_radius = 5
        self.anita_image = Image.open(r"C:\Users\Admin\Videos\anita.png")
        self.anita_image = self.anita_image.resize((40, 40), Image.LANCZOS)  # Resize image
        self.anita_photo = ImageTk.PhotoImage(self.anita_image)
        self.red_balls = []
        self.colors = ["red", "green", "blue", "orange", "purple", "cyan", "magenta", "yellow"]
        self.create_red_balls()

        # Create a second canvas for displaying factors
        self.factor_canvas = tk.Canvas(master, width=self.canvas_width, height=200, bg='lightgrey')
        self.factor_canvas.pack(side=tk.BOTTOM)

        # Factors affecting development
        self.factors = [
            "1. Family Income",
            "2. Educational Background of Parents",
            "3. Access to Quality Schools",
            "4. Private Coaching and Tutoring",
            "5. Health and Nutrition",
            "6. Living Conditions",
            "7. Availability of Educational Resources",
            "8. Extracurricular Opportunities",
            "9. Cultural Capital",
            "10. Social Capital",
            "11. Motivation and Aspirations",
            "12. Self-Efficacy",
            "13. Resilience",
            "14. Mental Health",
            "15. Quality of Primary Education",
            "16. Availability of Career Guidance",
            "17. Competitive Exam Preparation",
            "18. Scholarships and Financial Aid",
            "19. Caste-Based Discrimination",
            "20. Reservation Policies",
            "21. Social Stigma",
            "22. Rural vs. Urban Divide",
            "23. Gender Discrimination",
            "24. Community Support",
            "25. Peer Influence",
            "26. Role Models",
            "27. Economic Stability",
            "28. Government Policies",
            "29. Globalization",
            "30. Digital Literacy",
            "31. Internet Access",
            "32. Family Responsibilities",
            "33. Work Experience",
            "34. Internships and Training",
            "35. Geographical Location",
            "36. Political Stability",
            "37. Perceptions of Professions",
            "38. Value of Education",
            "39. Fear of Failure",
            "40. Imposter Syndrome",
            "41. Parental Support",
            "42. Sibling Influence",
            "43. Job Market Trends",
            "44. Entrepreneurial Opportunities",
            "45. Cultural Expectations",
            "46. Networking Opportunities",
            "47. Personal Experiences",
            "48. Public Perception of Fields",
            "49. Cumulative Impact",
            "50. Systemic Barriers",
            "51. Family Responsibilities",
            "52. Work Experience",
            "53. Internships and Training",
            "54. Geographical Location"
        ]

        # Assign factors to red balls
        self.red_ball_factors = [self.factors[i % len(self.factors)] for i in range(len(self.red_balls))]

        # List to track hits for each ball
        self.hit_history = []

    def create_red_balls(self):
        num_rows = 5  # Fixed number of rows
        num_columns = 10  # Fixed number of columns

        # Calculate total spacing and starting position
        total_width = num_columns * 40  # Each red ball spaced 40 pixels apart
        start_x = (self.canvas_width - total_width) // 2  # Centered

        for i in range(num_rows):
            for j in range(num_columns):
                x = start_x + j * 40
                y = (self.canvas_height // 2) + i * 40  # Centered vertically
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

                # Log the factor that corresponds to the red ball hit
                self.hit_history.append(self.red_ball_factors[red_index])
                
                # Show factors on the second canvas
                self.show_factors()

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
        self.canvas.delete("bin")
        for i, count in enumerate(self.bins):
            x0 = i * self.bin_width
            x1 = x0 + self.bin_width
            y0 = self.canvas_height
            y1 = y0 - (count * 5)  # Scale factor for the bin height
            color = self.colors[i % len(self.colors)]  # Cycle through the colors list
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags="bin")

    def show_factors(self):
        self.factor_canvas.delete("factor")  # Clear previous factors
        for index, factor in enumerate(self.hit_history):
            self.factor_canvas.create_text(10, 10 + index * 15, anchor='nw', text=factor, tags="factor")
        
        # Display all factors below the canvas
        for index, factor in enumerate(self.factors):
            x = 10 + (index % 5) * 200  # 5 factors per row
            y = 10 + (index // 5) * 15
            self.factor_canvas.create_text(x, y, anchor='nw', text=factor, tags="factor")

    def save_to_csv(self):
        with open('hit_history.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Hit Number", "Factor"])  # CSV header
            for index, factor in enumerate(self.hit_history):
                writer.writerow([index + 1, factor])  # Record hit number and factor

    def run_simulation(self):
        for _ in range(self.num_balls):
            self.drop_ball()
            self.draw_bins()  # Update the histogram as balls fall
        self.save_to_csv()  # Save the hit history to CSV after the simulation

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ball Collision and Colorful Histogram Simulation")
    num_balls = 500
    num_bins = 40
    sim = BallSimulation(root, num_balls, num_bins)
    sim.run_simulation()
    root.mainloop()
