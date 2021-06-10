import math


def cal(a, b):
    c = math.sqrt((a - 9) ** 2 + (b - 9) ** 2)
    return c


def mul(m):
    multi = m * math.sqrt(2)
    return multi


if __name__ == "__main__":
    x = 6
    y = 6
    h = cal(x, y)
    gnew = mul(5)
    print(h)
    print(gnew)
    print(h+gnew)
    print(h + 4*1.414+1)
