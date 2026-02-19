#!/usr/bin/env python3
"""
Tic-Tac-Toe game engine for GitHub Profile README.
Players move via GitHub Issues. A simple AI responds automatically.
"""

import sys
import re
import random

REPO = "codewithayuu/codewithayuu"
WINS = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
        [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
ROWS = "ABC"
SYM = {"_": "⬜", "X": "❌", "O": "⭕"}


def check_winner(board):
    """Return 'X', 'O', 'D' (draw), or None."""
    for w in WINS:
        if board[w[0]] == board[w[1]] == board[w[2]] != "_":
            return board[w[0]]
    return "D" if "_" not in board else None


def ai_move(board):
    """Simple AI: win > block > center > corner > edge."""
    for piece in ["O", "X"]:
        for i in range(9):
            if board[i] == "_":
                board[i] = piece
                if check_winner(board) == piece:
                    board[i] = "_"
                    return i
                board[i] = "_"
    if board[4] == "_":
        return 4
    corners = [i for i in [0, 2, 6, 8] if board[i] == "_"]
    if corners:
        return random.choice(corners)
    edges = [i for i in [1, 3, 5, 7] if board[i] == "_"]
    return random.choice(edges) if edges else -1


def pos_to_idx(pos):
    """Convert 'A1' → 0, 'B2' → 4, 'C3' → 8, etc."""
    return (ord(pos[0].upper()) - 65) * 3 + (int(pos[1]) - 1)


def generate_board_md(board):
    """Generate the markdown table for the game board."""
    md = "|   | **1** | **2** | **3** |\n|:---:|:---:|:---:|:---:|\n"
    for r in range(3):
        md += f"| **{ROWS[r]}** |"
        for c in range(3):
            i = r * 3 + c
            if board[i] == "_":
                pos = f"{ROWS[r]}{c + 1}"
                url = (
                    f"https://github.com/{REPO}/issues/new?"
                    f"title=tictactoe%7C{pos}&body=Just+click+submit!"
                )
                md += f" [{SYM['_']}]({url}) |"
            else:
                md += f" {SYM[board[i]]} |"
        md += "\n"
    return md


def main():
    if len(sys.argv) < 2:
        print("Usage: tictactoe.py 'tictactoe|A1'")
        sys.exit(1)

    # Parse move from issue title  (format: "tictactoe|A1")
    parts = sys.argv[1].split("|")
    if len(parts) < 2:
        print("Invalid format")
        sys.exit(1)
    move = parts[1].strip().upper()

    # Read README
    with open("README.md", "r") as f:
        readme = f.read()

    # Parse board state
    m = re.search(r"<!-- TICTACTOE_STATE:(.{9}) -->", readme)
    board = list(m.group(1)) if m else list("_" * 9)

    # If previous game ended, reset
    if check_winner(board):
        board = list("_" * 9)

    # Validate & apply player move
    idx = pos_to_idx(move)
    if not (0 <= idx <= 8) or board[idx] != "_":
        print(f"Invalid or taken: {move}")
        sys.exit(0)

    board[idx] = "X"
    result = check_winner(board)

    # AI responds if game isn't over
    if not result:
        ci = ai_move(board)
        if ci >= 0:
            board[ci] = "O"
        result = check_winner(board)

    # Determine status message
    if result == "X":
        status = "🎉 **You won!** Board resets — click any square for a new game!"
    elif result == "O":
        status = "🤖 **Computer wins!** Board resets — click any square for a new game!"
    elif result == "D":
        status = "🤝 **It's a draw!** Board resets — click any square for a new game!"
    else:
        status = f"✅ You placed ❌ at **{move}** — 🤖 responded — **your turn!**"

    # If game ended, show result then reset
    if result:
        # Build final board display, then reset state for next game
        final_md = generate_board_md(board)
        board = list("_" * 9)
        new_md = generate_board_md(board)
        board_section = (
            f"{final_md}\n"
            f"> {status}\n\n"
            f"**🆕 New game ready!**\n\n"
            f"{new_md}\n"
            f"> 🎮 **Click any square to start playing!**"
        )
    else:
        board_md = generate_board_md(board)
        board_section = f"{board_md}\n> {status}"

    state_str = "".join(board)

    # Update README
    readme = re.sub(
        r"<!-- TICTACTOE_BOARD_START -->.*?<!-- TICTACTOE_BOARD_END -->",
        f"<!-- TICTACTOE_BOARD_START -->\n\n{
            board_section}\n\n<!-- TICTACTOE_BOARD_END -->",
        readme,
        flags=re.DOTALL,
    )
    readme = re.sub(
        r"<!-- TICTACTOE_STATE:.*?-->",
        f"<!-- TICTACTOE_STATE:{state_str} -->",
        readme,
    )

    with open("README.md", "w") as f:
        f.write(readme)

    print(f"✅ Move={move} | Result={result or 'ongoing'} | State={state_str}")


if __name__ == "__main__":
    main()
