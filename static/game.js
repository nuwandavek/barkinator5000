const width = 600;
const height = 600;

const scene = new THREE.Scene();
const camera = new THREE.OrthographicCamera(
  width / -2,
  width / 2,
  height / 2,
  height / -2,
  0.1,
  1000
);

camera.position.set(0, 0, 50);
camera.rotation.set(0, 0, 0);

// add players to the scene
const fiveTone = new THREE.TextureLoader().load('fiveTone.jpg')
fiveTone.minFilter = THREE.NearestFilter
fiveTone.magFilter = THREE.NearestFilter
const player1Material = new THREE.MeshToonMaterial({ color: new THREE.Color("#333"), emissive: new THREE.Color("#c0392b"), gradientMap: fiveTone});
const player2Material = new THREE.MeshToonMaterial({ color: new THREE.Color("#333"), emissive: new THREE.Color("#27ae60"), gradientMap: fiveTone});
const playerGeometry = new THREE.IcosahedronGeometry(15, 0);
// const playerGeometry = new THREE.SphereGeometry(20, 30, 15);
const player1 = new THREE.Mesh(playerGeometry, player1Material);
const player2 = new THREE.Mesh(playerGeometry, player2Material);

// update player positions based on arrow key input
const handleKeyDown = (event) => {
  const player_id = 'player1'; // TODO: set player id dynamically
  const direction = event.key.replace('Arrow', '').toLowerCase();
  socket.emit('move', { player_id, direction });
};
document.addEventListener('keydown', handleKeyDown);

// set up socket.io connection
const socket = io();
socket.on('update_state', (game_state) => {
  // update player positions based on game state
  player1.position.set(...game_state.player1.position);
  player2.position.set(...game_state.player2.position);
});

// set up renderer and add objects to the scene
const renderer = new THREE.WebGLRenderer();
renderer.setSize(width, height);
document.getElementById('game-container').appendChild(renderer.domElement);


var textureLoader = new THREE.TextureLoader();
textureLoader.load('green.png', function(texture) {
  var geometry = new THREE.PlaneGeometry(width, height);
  var material = new THREE.MeshBasicMaterial({map: texture});
  var mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);
});

var light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(500, 500, 50);
scene.add(light);



scene.add(player1);
scene.add(player2);

// animate the scene
const animate = () => {
  requestAnimationFrame(animate);
  player1.rotation.y += 0.01;
  player2.rotation.y += 0.01;
  player2.rotation.z += 0.01;
  renderer.render(scene, camera);
};
animate();
