import tkinter as tk
import random
import time
import math
import csv
from PIL import Image, ImageTk  # Import PIL for image handling
import os  # Import os to check for file existence

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
        self.red_balls = []
        self.colors = ["red", "green", "blue", "orange", "purple", "cyan", "magenta", "yellow"]
        self.create_red_balls()

        # Load and resize the image for the blue ball
        image_path = "C:\\Users\\Admin\\Videos\\Anitha.JPEG"  # Path to the image
        if os.path.exists(image_path):  # Check if the file exists
            self.blue_ball_image = Image.open(image_path)  # Load the image
            self.blue_ball_image = self.blue_ball_image.resize((30, 30))  # Resize image (30x30)
            self.blue_ball_photo = ImageTk.PhotoImage(self.blue_ball_image)  # Convert to PhotoImage
        else:
            print("Error: The image file was not found. Please check the path.")
            self.blue_ball_photo = None  # Set to None if image is not found

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
            "50. Systemic Barriers"
        ]

        # Assign factors to red balls
        self.red_ball_factors = [self.factors[i % len(self.factors)] for i in range(len(self.red_balls))]

        # List to track hits for each ball
        self.hit_history = []

    def create_red_balls(self):
        # Arrange red balls with a left skew
        num_rows = random.randint(3, 5)  # Random number of rows
        num_columns = random.randint(5, 10)  # Random number of columns
        skew_factor = 20  # Adjust this value to control the skew effect
        for i in range(num_rows):
            for j in range(num_columns):
                # Random position offsets to create arbitrary patterns
                x_offset = random.randint(-20, 20)
                y_offset = random.randint(-20, 20)
                # Skew the x position to the left
                x = (self.canvas_width // 2 - num_columns * 20) + j * 40 - (skew_factor * (num_columns - j)) + x_offset
                y = (self.canvas_height // 2 - num_rows * 20) + i * 40 + y_offset
                
                red_ball = self.canvas.create_oval(x - self.red_ball_radius, y - self.red_ball_radius, 
                                                   x + self.red_ball_radius, y + self.red_ball_radius, 
                                                   fill='red', outline='black')
                self.red_balls.append((x, y))

    def ball_hits_red_ball(self, ball_x, ball_y):
        for index, (red_x, red_y) in enumerate(self.red_balls):
            if abs(ball_x - red_x) <= self.red_ball_radius + 15 and \
               abs(ball_y - red_y) <= self.red_ball_radius + 15:  # Adjusted for image size
                distance = math.sqrt((ball_x - red_x)**2 + (ball_y - red_y)**2)
                if distance <= (self.red_ball_radius + 15):  # Adjusted for image size
                    return True, (red_x, red_y), index  # Return index of the red ball hit
        return False, (0, 0), -1  # -1 if no ball hit

    def drop_ball(self):
        ball_x = self.canvas_width // 2
        ball_y = 0
        velocity_y = 0
        ball_size = 30  # Size of the image
        if self.blue_ball_photo:  # Only create image if it exists
            ball = self.canvas.create_image(ball_x, ball_y, image=self.blue_ball_photo)  # Use image instead of oval
        else:
            ball = self.canvas.create_oval(ball_x - ball_size // 2, ball_y - ball_size // 2, 
                                           ball_x + ball_size // 2, ball_y + ball_size // 2, 
                                           fill='blue', outline='black')  # Create a placeholder ball if image not found
        
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
                    ball_y = red_y - (self.red_ball_radius + ball_size)
                else:
                    ball_y = red_y + (self.red_ball_radius + ball_size)

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
                if ball:  # Check if ball is created
                    self.canvas.coords(ball, ball_x, ball_y)  # Update image position
                    self.master.update()
        
        # Update the final position of the ball
        self.canvas.coords(ball, ball_x, ball_y)  # Update final position
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
            y0 = self.max_height - (count * (self.max_height / max(self.bins) if max(self.bins) > 0 else 1))
            x1 = (i + 1) * self.bin_width
            y1 = self.max_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='grey', outline='black', tags="bin")

    def show_factors(self):
        # Clear previous factors displayed
        self.factor_canvas.delete("factor_text")
        for i, factor in enumerate(self.hit_history[-5:], 1):  # Show the last 5 factors
            self.factor_canvas.create_text(10, 10 + i * 20, anchor='nw', text=factor, tags="factor_text")

    def save_to_csv(self):
        with open('hit_history.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Hit Number', 'Factor'])
            for i, factor in enumerate(self.hit_history, 1):
                writer.writerow([i, factor])

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
