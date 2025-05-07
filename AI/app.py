from flask import Flask, render_template, request, redirect, url_for, session
from nim_utils import ai_move, check_game_over

app = Flask(__name__)
app.secret_key = "secret123"

@app.route('/')
def index():
    if 'piles' not in session:
        session['piles'] = [3, 4, 5]
        session['difficulty'] = 'hard'
        session['ai_move'] = None
    return render_template('index.html', piles=session['piles'], message="Your move!", ai_move=session.get('ai_move', None), difficulty=session.get('difficulty', 'hard'))

@app.route('/move', methods=['POST'])
def move():
    pile_index = int(request.form['pile'])
    remove_count = int(request.form['remove'])

    piles = session['piles']
    difficulty = session.get('difficulty', 'hard')

    if piles[pile_index] >= remove_count:
        piles[pile_index] -= remove_count
        if check_game_over(piles):
            message = "You win! 🎉"
            session.pop('piles', None)
            return render_template('index.html', piles=[0,0,0], message=message, ai_move=None, difficulty=difficulty)

        # AI move
        new_piles, ai_pile, ai_remove = ai_move(piles, difficulty)
        piles = new_piles
        session['ai_move'] = (ai_pile, ai_remove)

        if check_game_over(piles):
            message = "AI wins! 😭"
            session.pop('piles', None)
            return render_template('index.html', piles=[0,0,0], message=message, ai_move=None, difficulty=difficulty)

    session['piles'] = piles
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session.pop('piles', None)
    session.pop('ai_move', None)
    return redirect(url_for('index'))

@app.route('/set_difficulty', methods=['POST'])
def set_difficulty():
    difficulty = request.form['difficulty']
    session['difficulty'] = difficulty
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
