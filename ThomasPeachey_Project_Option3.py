import pygame as pyg
from pygame import gfxdraw
import matplotlib.pyplot as plt

# READ ME # v

# Change this to True if you want the program to simulate and output the data for option 3, part 2
closed = True


# Setting up the system variables
ball_temp = 313.15
env_temp = 293.15
h = 8.7  # J/s^-1m^2K^-1
area = 0.13  # m^2
m_ball = 0.1  # kg
m_air = 0.6  # kg
Cp_ball = 385  # Jkg^-1
Cp_air = 1000
t = 0
tstep = 1 # s
delta_e = 0
flag = 1
t_half = 0
clock = pyg.time.Clock()

# Setting up the display parameters
pyg.init()
pyg.display.set_caption('Cooling copper object simulation')
pyg.font.init()
size = width, height = 600, 600
screen = pyg.display.set_mode(size)
surf_1 = pyg.Surface(size)
rect1 = pyg.Rect(100, 100, 400, 400)
rect2 = pyg.Rect(0, 0, 600, 600)
backg_colour = (135, 206, 235)
black = (0, 0, 0)
my_font = pyg.font.SysFont(None, 20)  # setting up the font for display text

output_time = []
output_obj_temp = []
output_env_temp = []
output_deltat = []


# A function for displaying text
def display_text(text, surface, x, y):

    text = my_font.render(text, True, black)  # Rendering text
    surface.blit(text, [x, y])


# A function for drawing anti-aliased circles
def draw_circle(surface, x, y, radius, color):

    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)

# Running the program
run = True
while run:

    # Calculating the temperature difference
    delta_t = ball_temp - env_temp

    # Appending data to the output lists
    output_obj_temp.append(ball_temp)
    output_time.append(t)
    output_deltat.append(delta_t)
    output_env_temp.append(env_temp)

    if ball_temp <= 303.15 and flag == 1:
        t_half = str(t)
        flag = 0

    # Defining the rate of energy change
    delta_e = delta_t * h * area

    # Defining the rate of temperature change for the object
    dt = -delta_e / (m_ball * Cp_ball)

    if closed:

        # Setting background for the closed system
        colour_shift = 20 - delta_t
        surf_1.fill((135 + 3 * colour_shift, 206, 235 - 3 * colour_shift))
        pyg.draw.rect(surf_1, black, rect1, 5)
        pyg.draw.rect(surf_1, (150, 150, 150), rect2, 200)

    else:

        # Setting background for the open system
        surf_1.fill(backg_colour)

    # Drawing the object to the screen
    ball_colour = (184 + delta_t, 115 - 3 * delta_t, 50 - 2 * delta_t)
    draw_circle(surf_1, 300, 300, 103, black)
    draw_circle(surf_1, 300, 300, 100, ball_colour)

    # Drawing the relevant text to the screen
    display_text("Temperature Difference = " + str("%.2f" % delta_t) + "K", surf_1, 10, 50)
    display_text("Time = " + str(t) + " s", surf_1, 250, 10)
    display_text("Object Temperature = " + str("%.2f" % ball_temp) + "K", surf_1, 10, 10)
    display_text("Environment Temperature = " + str("%.2f" % env_temp) + "K", surf_1, 10, 30)
    if flag == 0:
        display_text(
            "It took " + t_half + " seconds for the object temp. to fall by  half the original temp. difference",
            surf_1, 30, 510)

    # Ending the program when the temperature difference is less than 0.01 K
    if delta_t < 0.01:
        run = False

    # Updating the temperature of the ball
    ball_temp += dt * tstep

    # Updating the display and time
    if closed:
        env_temp += (tstep * delta_e) / (m_air * Cp_air)
    screen.blit(surf_1, [0, 0])
    pyg.display.flip()
    t += tstep
    clock.tick(1)

    # Ending the program if the x is pressed
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False


# plotting the output data
fig1, ax1 = plt.subplots()
ax1.scatter(output_time, output_obj_temp, marker='o', label="Object temperature")
ax1.scatter(output_time, output_env_temp, marker='x', label="Environment temperature")
ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature")
ax1.legend()
plt.show()

fig2, ax2 = plt.subplots()
ax2.scatter(output_time, output_deltat, marker='+', label="Temperature difference")
ax2.set_xlabel("Time")
ax2.set_ylabel("Temperature")
ax2.legend()
plt.show()
print(t_half)













