import json
import numpy as np
import random
from collections import defaultdict
from shapely.geometry import Point, Polygon


class Colors():
  colors = ["#c0392b", "#2980b9", "#27ae60", "#f39c12", "#2c3e50", "#8e44ad"]

  def __new__(self, idx):
    return self.colors[idx % len(self.colors)]


MAP_LIMITS = (-300, -300, 300, 300)
RESTRICTED_NAME = 'restricted'


class World:
  def __init__(self, map=None):
    self.npcs = defaultdict()
    self.players = defaultdict()
    self.restricted_polygons = self.get_restricted_polygons(map)
    self.conversations = defaultdict(dict)

  def add_npc(self, name, pos=[]):
    self.npcs[name] = Puptron(name, pos, self)
    print(f"{name} added at {self.npcs[name].position}")

  def add_player(self, name, pos=None):
    self.players[name] = Puptron(name, pos, self)
    print(f"{name} added at {self.players[name].position}")

  @property
  def puptrons(self):
    return {**self.npcs, **self.players}

  @property
  def state(self):
    return [x.state for x in self.puptrons.values()]

  def get_restricted_polygons(self, map):
    polygons = []
    if map:
      with open(map, "r") as fob:
        map = json.load(fob)
      restricted_objects = [x['objects'] for x in map['layers'] if RESTRICTED_NAME in x['name']]
      restricted_objects = [x for sublist in restricted_objects for x in sublist]
      map_height = map['height'] * map['tileheight']
      map_width = map['width'] * map['tilewidth']
      for obj in restricted_objects:
        x1 = np.interp(obj['x'], [0, map_width], [MAP_LIMITS[0], MAP_LIMITS[2]])
        y1 = np.interp(obj['y'], [0, map_height], [MAP_LIMITS[3], MAP_LIMITS[1]])
        x2 = np.interp(obj['x'] + obj['width'], [0, map_width], [MAP_LIMITS[0], MAP_LIMITS[2]])
        y2 = np.interp(obj['y'] + obj['height'], [0, map_height], [MAP_LIMITS[3], MAP_LIMITS[1]])
        polygons.append(Polygon(((x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1))))
    return polygons


class Puptron:
  def __init__(self, name, pos=None, world=None):
    self.name = name
    self._world = world
    self.color = Colors(len(world.puptrons.values()))
    self.position = self.spawn(MAP_LIMITS) if pos is None else [*pos, 0]
    self.rotation = self.init_rotation()
    self.barkable = []

  def spawn(self, bounds):
    while True:
      pos = [random.randint(bounds[0], bounds[2]), random.randint(bounds[1], bounds[3]), 0]
      if self.is_valid_pos(pos):
        break
    return pos

  @staticmethod
  def init_rotation():
    rots = np.zeros(3)
    rots[np.random.randint(0, 3)] = 0.05
    return rots

  @property
  def state(self):
    return {
      'name': self.name,
      'color': self.color,
      'position': list(self.position),
      'rotation': list(self.rotation),
      'barkable': self.barkable
    }

  def move(self, direction, movement=5):
    tempos = self.position.copy()
    if direction == 'up':
      tempos[1] += movement
    elif direction == 'down':
      tempos[1] -= movement
    elif direction == 'left':
      tempos[0] -= movement
    elif direction == 'right':
      tempos[0] += movement

    if self.is_valid_pos(tempos):
      self.position = tempos
    self.set_barkable()

  def set_barkable(self, min_bark_distance=30):
    point = Point(self.position[0], self.position[1])
    character_dists = {x.name: point.distance(Point(x.position[0], x.position[1])) for x in self._world.puptrons.values() if x.name != self.name}
    self.barkable = [k for k, v in character_dists.items() if v <= min_bark_distance]

  def is_valid_pos(self, pos, tolerance_dist=15):
    objects = self._world.restricted_polygons + [Point(x.position[0], x.position[1]) for x in self._world.puptrons.values() if x.name != self.name]
    point = Point(pos[0], pos[1])
    for polygon in objects:
      if point.distance(polygon) < tolerance_dist:
        return False

    if (pos[0] < MAP_LIMITS[0] + tolerance_dist) or (pos[0] > MAP_LIMITS[2] - tolerance_dist) or\
       (pos[1] < MAP_LIMITS[1] + tolerance_dist) or (pos[1] > MAP_LIMITS[3] - tolerance_dist):
      return False
    return True
