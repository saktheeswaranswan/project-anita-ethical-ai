import tkinter as tk
import random
import math
import csv

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
        self.blue_ball_radius = 20  # Adjusted for image size
        self.red_balls = []
        self.colors = ["red", "green", "blue", "orange", "purple", "cyan", "magenta", "yellow"]
        self.create_red_balls()

        # Load the image for the blue ball
        self.blue_ball_image = tk.PhotoImage(file="C:\\Users\\Admin\\Videos\\anita.png")  # Replace with your image path
        self.blue_ball_id = None  # To hold the ID of the drawn image

        # Create canvas for displaying factors
        self.factor_canvas = tk.Canvas(master, width=self.canvas_width, height=200, bg='lightgrey')
        self.factor_canvas.pack(side=tk.BOTTOM)

        # Factors affecting development
        self.factors = self.create_factors()

        # Assign factors to red balls (ensuring each ball has a factor)
        self.red_ball_factors = random.choices(self.factors, k=len(self.red_balls))

        # List to track hits for each ball
        self.hit_history = []

        # Blink state for factors
        self.blink_state = True
        self.blink_factors()

    def create_factors(self):
        return [
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
            "51. Nutritious Food",
            "52. Medical Care",
            "53. Entertainment",
            "54. Language and Communication Skills from Best Tutors"
        ]

    def create_red_balls(self):
        num_rows = random.randint(3, 5)  # Random number of rows
        num_columns = random.randint(5, 10)  # Random number of columns
        spacing = 40  # Space between balls

        # Create a grid layout
        for i in range(num_rows):
            for j in range(num_columns):
                x = (self.canvas_width // 2 - (num_columns * spacing // 2)) + j * spacing
                y = (self.canvas_height // 2 - (num_rows * spacing // 2)) + i * spacing
                
                red_ball = self.canvas.create_oval(x - self.red_ball_radius, y - self.red_ball_radius, 
                                                   x + self.red_ball_radius, y + self.red_ball_radius, 
                                                   fill='red', outline='black')
                self.red_balls.append((x, y))

    def ball_hits_red_ball(self, ball_x, ball_y):
        for index, (red_x, red_y) in enumerate(self.red_balls):
            if abs(ball_x - red_x) <= self.red_ball_radius + self.blue_ball_radius and \
               abs(ball_y - red_y) <= self.red_ball_radius + self.blue_ball_radius:
                distance = math.sqrt((ball_x - red_x)**2 + (ball_y - red_y)**2)
                if distance <= (self.red_ball_radius + self.blue_ball_radius):
                    return True, (red_x, red_y), index  # Return index of the red ball hit
        return False, (0, 0), -1  # -1 if no ball hit

    def drop_ball(self):
        ball_x = self.canvas_width // 2
        ball_y = 0
        velocity_y = 0

        # Draw the blue ball using an image
        self.blue_ball_id = self.canvas.create_image(ball_x, ball_y, image=self.blue_ball_image)

        update_interval = 5
        frame_count = 0
        hit_red_balls = set()

        while ball_y < self.max_height:
            velocity_y += self.gravity
            ball_y += velocity_y
            move = random.choice([-1, 1])
            ball_x += move * self.bin_width // 4
            
            hit, (red_x, red_y), red_index = self.ball_hits_red_ball(ball_x, ball_y)
            if hit:
                hit_red_balls.add(red_index)
                velocity_y = -velocity_y * 0.7
                if ball_y < red_y:
                    ball_y = red_y - (self.red_ball_radius + self.blue_ball_radius)
                else:
                    ball_y = red_y + (self.red_ball_radius + self.blue_ball_radius)

                # Ensure red_index is valid for red_ball_factors
                if red_index < len(self.red_ball_factors):
                    self.hit_history.append(self.red_ball_factors[red_index])
                self.show_factors()

            if len(hit_red_balls) == len(self.red_balls):
                break
            
            frame_count += 1
            if frame_count % update_interval == 0:
                self.canvas.coords(self.blue_ball_id, ball_x, ball_y)
                self.master.update()
        
        # Final position
        self.canvas.coords(self.blue_ball_id, ball_x, ball_y)
        self.master.update()
        
        bin_index = int(ball_x // self.bin_width)
        if 0 <= bin_index < self.num_bins:
            self.bins[bin_index] += 1

    def draw_bins(self):
        self.canvas.delete("bin")
        for i, count in enumerate(self.bins):
            x0 = i * self.bin_width
            x1 = x0 + self.bin_width
            y0 = self.canvas_height
            y1 = y0 - (count * 5)  # Scale factor for the bin height
            color = self.colors[i % len(self.colors)]
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags="bin")

    def show_factors(self):
        self.factor_canvas.delete("factor")
        num_factors = len(self.factors)
        factors_per_column = 6
        num_columns = (num_factors + factors_per_column - 1) // factors_per_column  # Calculate number of columns

        for col in range(num_columns):
            for row in range(factors_per_column):
                index = col * factors_per_column + row
                if index < num_factors:
                    x = 10 + col * 200  # Adjust column spacing
                    y = 10 + row * 15
                    self.factor_canvas.create_text(x, y, anchor='nw', text=self.factors[index], tags="factor")

    def blink_factors(self):
        self.blink_state = not self.blink_state
        self.show_factors()
        self.master.after(500, self.blink_factors)

    def save_to_csv(self):
        with open('hit_history.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Hit Number", "Factor"])
            for index, factor in enumerate(self.hit_history):
                writer.writerow([index + 1, factor])

    def run_simulation(self):
        for _ in range(self.num_balls):
            self.drop_ball()
            self.draw_bins()
        self.save_to_csv()

if __name__ == "__main__":
    root = tk.Tk()
    sim = BallSimulation(root, num_balls=100, num_bins=10)
    root.mainloop()
