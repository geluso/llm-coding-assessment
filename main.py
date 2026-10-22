import pandas as pd
import requests
from io import StringIO

from collections import defaultdict

url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"

response = requests.get(url, timeout=30)
response.raise_for_status()

tables = pd.read_html(StringIO(response.text))

for i, df in enumerate(tables):
    xs = df[0]
    chars = df[1]
    ys = df[2]

    # Collect the coordinates of each character in the grid
    # Keep track of the largest x and y coordinate
    max_xx = 0
    max_yy = 0
    grid = defaultdict(lambda: " ")
    for xx, char, yy in zip(xs, chars, ys):
        if xx == "x-coordinate":
            continue

        xx = int(xx)
        yy = int(yy)
        coordinate = f"{xx},{yy}"
        grid[coordinate] = char
        print("in", coordinate, char)

        max_xx = max(max_xx, xx)
        max_yy = max(max_yy, yy)

    print(max_xx, max_yy)

    # Print out the grid
    for row in range(0, max_yy + 1):
        line = ""
        for col in range(0, max_xx + 1):
            coord = f"{col},{row}"
            cell = grid[coord]
            line += cell
        print(line)
