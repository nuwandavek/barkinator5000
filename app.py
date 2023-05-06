from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(
  __name__,
  static_url_path='',
  static_folder='static',
  template_folder='static'
)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# define initial state of the game
game_state = {
  'player1': {
    'position': [0, 0, 0]
  },
  'player2': {
    'position': [10, 0, 0]
  }
}


@socketio.on('connect')
def handle_connect():
  # send initial game state to the client
  emit('update_state', game_state)


@socketio.on('move')
def handle_move(data):
  # update player position based on arrow key input
  player_id = data['player_id']
  direction = data['direction']
  position = game_state[player_id]['position']
  if direction == 'up':
    position[1] += 5
  elif direction == 'down':
    position[1] -= 5
  elif direction == 'left':
    position[0] -= 5
  elif direction == 'right':
    position[0] += 5

  # send updated game state to all clients
  emit('update_state', game_state, broadcast=True)


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  socketio.run(app, host="0.0.0.0", port=3000, debug=True)
