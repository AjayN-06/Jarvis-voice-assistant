from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [[" " for _ in range(3)] for _ in range(3)]
players = ["X", "O"]
current_player = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global current_player, board
    data = request.json
    row, col = data["row"], data["col"]

    if board[row][col] != " ":
        return jsonify({"error": "Cell already taken"}), 400

    board[row][col] = players[current_player]
    winner = check_winner(board, players[current_player])
    full = is_full(board)

    if winner:
        return jsonify({"winner": players[current_player]})
    elif full:
        return jsonify({"winner": "Draw"})

    current_player = 1 - current_player
    return jsonify({"board": board, "next_player": players[current_player]})

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(all(cell != " " for cell in row) for row in board)

if __name__ == "__main__":
    app.run(debug=True)
    