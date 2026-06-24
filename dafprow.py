import math

A = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ0"

M = [
    [0,4,8,3,7],
    [4,8,3,4,5],
    [8,3,7,5,3],
    [3,4,5,3,1],
    [7,5,3,1,0],
]

DAFNE = [
    "DAFNE",
    "ABRDN",
    "FR0RF",
    "NDRBA",
    "ENFAD",
]

def add1(block):
    out = []
    for i in range(5):
        row = ""
        for j in range(5):
            c   = block[i][j]
            idx = A.index(c.encode())
            row += chr(A[(idx + 1) % len(A)])
        out.append(row)
    return out

def mul5x5(block):
    out = []
    for i in range(5):
        row = ""
        for j in range(5):
            c   = block[i][j]
            idx = A.index(c.encode())
            off = M[i][j]
            row += chr(A[(idx + off) % len(A)])
        out.append(row)
    return out

# --- COLORS ----------------------------------------------------------

BG   = (255, 192, 85)   # background
ZERO = (255, 85, 192)   # DAFNE '0'

ZERO_IDX = A.index(b"0")

def color_of(c):
    idx = A.index(c.encode())
    if idx == ZERO_IDX:
        return ZERO
    return (
        (idx * 9) % 256,
        (idx * 5) % 256,
        (idx * 3) % 256,
    )

# --------------------------------------------------------------------

N = 28
R = 40
BLOCK = 5
PAD = 2
SIZE = 2*R + BLOCK + PAD + BLOCK

# Start with None so background can be applied AFTER block placement
img = [[None for _ in range(SIZE)] for _ in range(SIZE)]

states = []

# state 0: original DAFNE block
b = DAFNE
states.append(b)

# state 1: +1 everywhere
b = add1(b)
states.append(b)

# states 2..27: mul5x5
for _ in range(26):
    b = mul5x5(b)
    states.append(b)

# place blocks
for k, block in enumerate(states):
    ang = 2*math.pi * k / N - math.pi/2
    cx = int(SIZE/2 + R*math.cos(ang))
    cy = int(SIZE/2 + R*math.sin(ang))

    for i in range(BLOCK):
        for j in range(BLOCK):
            x = cx + j
            y = cy + i
            if 0 <= x < SIZE and 0 <= y < SIZE:
                img[y][x] = color_of(block[i][j])

# fill background ONLY where untouched
for y in range(SIZE):
    for x in range(SIZE):
        if img[y][x] is None:
            img[y][x] = BG

# write PPM (P6)
with open("pro.ppm", "wb") as f:
    f.write(f"P6\n{SIZE} {SIZE}\n255\n".encode())
    for row in img:
        for (r, g, b) in row:
            f.write(bytes([r, g, b]))
