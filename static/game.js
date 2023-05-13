const width = 600;
const height = 600;
let gameState = [];
const threePlayers = {}

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

// update player positions based on arrow key input
const handleKeyDown = (event) => {
  const id = 'puptron-0';
  const direction = event.key.replace('Arrow', '').toLowerCase();
  socket.emit('move', { id, direction });
};
document.addEventListener('keydown', handleKeyDown);

// set up socket.io connection
const socket = io();
socket.on('update_state', (data) => {
  console.log(data);
  //0. Set gamesState
  gameState = data;
  
  //1. Check if there is any new player, and create them
  //2. Move all players to the correct location
  gameState.forEach(puptron => {
    if (puptron.name in threePlayers){}
    else{
      let playerMaterial = new THREE.MeshToonMaterial({ color: new THREE.Color("#333"), emissive: new THREE.Color(puptron.color), gradientMap: fiveTone});
      let playerGeometry = new THREE.IcosahedronGeometry(15, 0);
      threePlayers[puptron.name] = new THREE.Mesh(playerGeometry, playerMaterial);
      scene.add(threePlayers[puptron.name]);
    }
    threePlayers[puptron.name].position.set(...puptron.position);
  });
});

// set up renderer and add objects to the scene
const renderer = new THREE.WebGLRenderer();
renderer.setSize(width, height);
document.getElementById('game-map').appendChild(renderer.domElement);


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


// animate the scene
const animate = () => {
  requestAnimationFrame(animate);
  // Rotate players
  gameState.forEach(puptron => {
    threePlayers[puptron.name].rotation.x += puptron.rotation[0];
    threePlayers[puptron.name].rotation.y += puptron.rotation[1];
    threePlayers[puptron.name].rotation.z += puptron.rotation[2];
  });
  renderer.render(scene, camera);
};
animate();
