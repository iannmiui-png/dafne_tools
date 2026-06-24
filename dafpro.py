A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0"

M = [
    [0,4,8,3,7],
    [4,8,3,4,5],
    [8,3,7,5,3],
    [3,4,5,3,1],
    [7,5,3,1,0],
]

DAFNE = [
    "DAFNE",
    "ABDRN",
    "FR0RF",
    "NDRBA",
    "ENFAD",
]

def mul5x5(block):
    out = []
    for i in range(5):
        row = ""
        for j in range(5):
            c   = block[i][j]
            idx = A.index(c)
            off = M[i][j]
            row += A[(idx + off) % len(A)]
        out.append(row)
    return out

if __name__ == "__main__":
    b = DAFNE
    for k in range(28):
        print(f"state {k}")
        for r in b:
            print(r)
        print()
        b = mul5x5(b)
