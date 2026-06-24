from PIL import Image, ImagePalette

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
            idx = A.index(block[i][j].encode())
            row += chr(A[(idx + 1) % len(A)])
        out.append(row)
    return out

def mul5x5(block):
    out = []
    for i in range(5):
        row = ""
        for j in range(5):
            idx = A.index(block[i][j].encode())
            off = M[i][j]
            row += chr(A[(idx + off) % len(A)])
        out.append(row)
    return out

# --- Generate 28 states ---
states = []
b = DAFNE
states.append(b)        # state 0
b = add1(b)
states.append(b)        # state 1
for _ in range(26):
    b = mul5x5(b)
    states.append(b)    # states 2..27

# --- Build grayscale palette (identity) ---
palette = []
for i in range(256):
    palette.extend([i, i, i])  # RGB = (i,i,i)

# --- Convert states to GIF frames ---
frames = []
scale = 20  # enlarge 5×5 to 100×100 for visibility

for block in states:
    img = Image.new("P", (5,5))
    img.putpalette(palette)

    # fill pixels with ASCII byte values
    for y in range(5):
        for x in range(5):
            img.putpixel((x,y), ord(block[y][x]))

    # upscale without interpolation (no dithering)
    img = img.resize((44, 44), Image.NEAREST)
    frames.append(img)

# --- Save GIF ---
frames[0].save(
    "cycle.gif",
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0,
    optimize=False,
    dither=Image.NONE,
)
