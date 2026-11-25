import math
from cadquery import func as cf

def clutch_brick(length, width, height, stud_d, stud_h, spacing):

    body = cf.box(length, width, height)
    stud = cf.cylinder(d=stud_d, h=stud_h)

    brick = body

    # Create 8 studs (2 rows × 4 columns)
    for i in range(4):
        for j in range(2):
            x = (i - 1.5) * spacing
            y = (j - 0.5) * spacing

            new_stud = stud.moved(x=x, y=y, z=height)
            brick = brick + new_stud

    return brick


brick = clutch_brick(31.2, 15.6, 9.6, 4.8, 1.7, 8.0)

# Expected volume of body + 8 studs
expected = (
    31.2 * 15.6 * 9.6
    + 8 * math.pi * (4.8 / 2) ** 2 * 1.7
)

assert abs(brick.Volume() - expected) < 0.5

brick.exportStl("brick.stl")

print("2 × 4 Clutch Brick created successfully!")
print("Volume:", brick.Volume())