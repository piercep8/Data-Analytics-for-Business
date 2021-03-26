# Import Math package to give me the value of Pi
import math


# Calculate the area of a circle
def calc_circle_area(radius):
    circle_area = round(math.pi * radius ** 2, 3)
    return circle_area


# Calculate the area of a sphere
def calc_sphere_area(radius):
    sphere_area = round(4 * math.pi * radius ** 2, 3)
    return sphere_area


print(calc_circle_area(3))
print(calc_sphere_area(3))
