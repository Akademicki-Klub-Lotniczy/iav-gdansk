NORTH = [54.370418, 18.630057]
WEST =  [54.370014, 18.629358]

SOUTH = [54.369374, 18.630439]
EAST =  [54.369780, 18.631139]


EAST2 =  [54.369980, 18.631139]
EAST3 =  [54.369780, 18.631339]

from geopy.distance import geodesic

print(geodesic(EAST, EAST2).m)
print(geodesic(EAST, EAST3).m)

def calculate_mesh5(c1, c2, c3, c4):
    # Does stuff
    return [
        #Square one
        [
            [],
            [],
            [],
            [],
        ],

        # Square two
        [
            # 4 cords
        ],
        # Etc...
    ]