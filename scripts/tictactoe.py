import sys
import re
import random

REPO = "codewithayuu/codewithayuu"
WINS = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
        [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
SYM = {"_": "⬜", "X": "❌", "O": "⭕"}
ROWS = "ABC"


def check(b):
    for w in WINS:
        if b[w[0]] == b[w[1]] == b[w[2]] != "_":
            return b[w[0]]
    return "D" if "_" not in b else None


def ai(b):
    for p in ["O", "X"]:
        for i in range(9):
            if b[i] == "_":
                b[i] = p
                if check(b) == p:
                    b[i] = "_"
                    return i
                b[i] = "_"
    if b[4] == "_":
        return 4
    c = [i for i in [0, 2, 6, 8] if b[i] == "_"]
    if c:
        return random.choice(c)
    e = [i for i in [1, 3, 5, 7] if b[i] == "_"]
    return random.choice(e) if e else -1


def board_md(b):
    md = "|   | **1** | **2** | **3** |\n|:---:|:---:|:---:|:---:|\n"
    for r in range(3):
        md += f"| **{ROWS[r]}** |"
        for c in range(3):
            i = r*3+c
            if b[i] == "_":
                pos = f"{ROWS[r]}{c+1}"
                md += f" [{SYM['_']}](https://github.com/{REPO}/issues/new?title=tictactoe%7C{
                    pos}&body=Just+click+submit!) |"
            else:
                md += f" {SYM[b[i]]} |"
        md += "\n"
    return md


parts = sys.argv[1].split("|")
move = parts[1].strip().upper()
with open("README.md", "r") as f:
    readme = f.read()
m = re.search(r"<!-- TICTACTOE_STATE:(.{9}) -->", readme)
board = list(m.group(1)) if m else list("_"*9)
if check(board):
    board = list("_"*9)
idx = (ord(move[0])-65)*3+(int(move[1])-1)
if not (0 <= idx <= 8) or board[idx] != "_":
    sys.exit(0)
board[idx] = "X"
r = check(board)
if not r:
    ci = ai(board)
    if ci >= 0:
        board[ci] = "O"
    r = check(board)
if r == "X":
    st = "🎉 **You won!** Click any square for a new game!"
elif r == "O":
    st = "🤖 **Bot wins!** Click any square for a new game!"
elif r == "D":
    st = "🤝 **Draw!** Click any square for a new game!"
else:
    st = f"✅ You placed ❌ at **{move}** — 🤖 responded — **your turn!**"
if r:
    board = list("_"*9)
bmd = board_md(board)
section = f"{bmd}\n> {st}"
readme = re.sub(r"<!-- TICTACTOE_BOARD_START -->.*?<!-- TICTACTOE_BOARD_END -->",
                f"<!-- TICTACTOE_BOARD_START -->\n\n{section}\n\n<!-- TICTACTOE_BOARD_END -->", readme, flags=re.DOTALL)
readme = re.sub(r"<!-- TICTACTOE_STATE:.*?-->",
                f"<!-- TICTACTOE_STATE:{''.join(board)} -->", readme)
with open("README.md", "w") as f:
    f.write(readme)
