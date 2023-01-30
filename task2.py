def mystery(n):
    v = 0
    for index in range(1, n + 1):
        v += int(f"{index}"*index)
    return v

print(mystery(4))

