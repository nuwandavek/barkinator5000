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
for idx, pos in enumerate([(-250, -210), (-250, 0)]):
  world.add_puptrons(idx, pos)


@socketio.on('connect')
def handle_connect():
  emit('update_state', world.state)


@socketio.on('move')
def handle_move(data):
  world.puptrons[data['id']].move(data['direction'], restricted_polygons=world.restricted_polygons, puptrons=world.puptrons)
  emit('update_state', world.state, broadcast=True)


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  socketio.run(app, host="0.0.0.0", port=3000, debug=True)
