
from dataclasses import dataclass
from cadquery import func as cf

@dataclass
class CellSpec:
    r_cell: float
    h_cell: float


def make_cell(spec):
    return cf.cylinder(d=2 * spec.r_cell, h=spec.h_cell)


def tray(spec, n=3, clearance=0.3, wall=4.0,
         thickness=6.0, depth=3.0):

    pocket_r = spec.r_cell + clearance
    pitch = 2 * pocket_r + wall

    plate_length = n * pitch + wall
    plate_width = 2 * pocket_r + 2 * wall

    plate = cf.box(plate_length, plate_width, thickness)

    pocket = cf.cylinder(
        d=2 * pocket_r,
        h=depth + 1
    ).moved(z=thickness - depth)

    # Create three battery pockets
    for i in range(n):
        x = (i - (n - 1) / 2) * pitch
        plate = plate - pocket.moved(x=x)

    # Add two mirrored mounting holes
    hole_d = 3.0
    hole = cf.cylinder(d=hole_d, h=thickness + 2)

    hole_x = plate_length / 2 - 2.0

    for x in [-hole_x, hole_x]:
        plate = plate - hole.moved(x=x)

    return plate


cells = {
    "18650": CellSpec(9.0, 65.0),
    "21700": CellSpec(10.5, 70.0),
    "4680": CellSpec(23.0, 80.0),
}


if __name__ == "__main__":
    for name, spec in cells.items():
        t = tray(spec)

        print(name, t.isValid(), round(t.Volume(), 1))

        t.exportStl(f"tray_{name}.stl")
