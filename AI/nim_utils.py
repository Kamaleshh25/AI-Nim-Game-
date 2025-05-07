import random
import pickle
import numpy as np

# Load trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def ai_move(piles, difficulty="hard"):
    original_piles = piles.copy()
    possible_moves = []

    # Collect all possible moves
    for i in range(len(piles)):
        for remove in range(1, piles[i]+1):
            new_piles = piles.copy()
            new_piles[i] -= remove
            pred = model.predict([new_piles])
            possible_moves.append((new_piles, i, remove, pred[0]))

    # Easy mode: random move
    if difficulty == "easy":
        move = random.choice(possible_moves)
        return move[0], move[1], move[2]

    # Medium mode: 50% smart, 50% random
    if difficulty == "medium":
        smart_moves = [m for m in possible_moves if m[3] == 1]
        if smart_moves and random.random() < 0.5:
            move = random.choice(smart_moves)
        else:
            move = random.choice(possible_moves)
        return move[0], move[1], move[2]

    # Hard mode: always try winning move
    smart_moves = [m for m in possible_moves if m[3] == 1]
    if smart_moves:
        move = random.choice(smart_moves)
        return move[0], move[1], move[2]
    
    # If no winning move possible
    move = random.choice(possible_moves)
    return move[0], move[1], move[2]

def check_game_over(piles):
    return all(p == 0 for p in piles)
