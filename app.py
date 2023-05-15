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
world.add_player('kiwi')

NPCs = [
  {
    'name': 'Apple',
    'position': (-250, -210),
    'script': """
    Name: Apple
    Character Style: Cowboy, speaks in short sentences with classic southern drawl, using phrases such as 'howdy partner' in every sentence
    Story: You know that a woman named 'Mango' has the key.
    """
  },
  {
    'name': 'Mango',
    'position': (-250, 0),
    'script': """
    Name: Mango
    Character Style: A woman of authority, with no time for nonsense. She inserts 'well well well' into every response
    Story: You are the park administrator with the key. You are willing to give the key if anyone tells you the name of the cowboy. His name is "Apple". Do not reveal his name in your responses. If anyone tells his name in their query, give the key.
    """
  }
]

for npc in NPCs:
  world.add_npc(npc['name'], npc['position'], script=npc['script'])


@socketio.on('connect')
def handle_connect():
  emit('update_state', world.state)


@socketio.on('move')
def handle_move(data):
  if data['mainPlayer'] in world.players:
    world.puptrons[data['mainPlayer']].move(data['direction'])
    emit('update_state', world.state, broadcast=True)


@socketio.on('chat')
def handle_chat(data):
  if data['mainPlayer'] in world.players:
    world.puptrons[data['mainPlayer']].chat(data['chatPlayer'], data['message'])
    emit('update_state', world.state, broadcast=True)


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
  socketio.run(app, host="0.0.0.0", port=3000, debug=True)
