from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from helpers import World

app = Flask(
  __name__,
  static_url_path='',
  static_folder='static',
  template_folder='static'
)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

world = World("./static/green.json")
# Initialize with some characters
world.add_player('kiwi', chat={'apple': [
  {'type': 'sent', 'message': "Hey! How's it going?"},
  {'type': 'received', 'message': "Yoyo, just chilling."},
  {'type': 'sent', 'message': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset"}
]})
for name, pos in [
  ('apple', (-250, -210)),
  ('mango', (-250, 0))
]:
  world.add_npc(name, pos)


@socketio.on('connect')
def handle_connect():
  emit('update_state', world.state)


@socketio.on('move')
def handle_move(data):
  if data['mainPlayer'] in world.players:
    world.puptrons[data['mainPlayer']].move(data['direction'])
    emit('update_state', world.state, broadcast=True)


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  socketio.run(app, host="0.0.0.0", port=3000, debug=True)
