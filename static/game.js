const width = 600;
const height = 600;
let gameState = [];
const threePlayers = {}
const mainPlayer = 'kiwi';
let chatPlayer = null;

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
  if (event.key === 'Enter'){
    sendChat();
  }
  const direction = event.key.replace('Arrow', '').toLowerCase();
  if ((['up', 'right', 'left', 'down'].includes(direction)) && !($("#input-send").is( ":focus" ))){
    socket.emit('move', { mainPlayer, direction });
  }
};
document.addEventListener('keydown', handleKeyDown);

// set up socket.io connection
const socket = io();
socket.on('update_state', (data) => {
  // console.log(data);
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
    if (puptron.name === mainPlayer){
      if (puptron.bark != null){
        enableGameChat(gameState.filter( pup => pup.name === puptron.barkable)[0], puptron.bark);
      }
      else{
        disableGameChat();
      }
    }
  });
});


function populateChats(chats){
  let chatbody = $("#chat-body");
  chatbody.html('');
  chats.forEach(chat=>{
    if(chat.type === 'sent'){
      chatbody.append("<div class='chat-sent'><p class='chat'>"+chat.message+"</p></div>");
    }
    else if(chat.type === 'received'){
      chatbody.append("<div class='chat-received'><p class='chat'>"+chat.message+"</p></div>");
    }
  });
  chatbody.animate({scrollTop: chatbody[0].scrollHeight});
  $("#input-send").val('');

}

function enableGameChat(character, chats){
  chatPlayer = character.name;
  $("#overlay").hide();
  // $("#game-chat-2").removeClass('disableDiv');
  $(".chat-character-dp").css('color', character.color);
  // $("#chat-character-name").text(character.name);
  populateChats(chats);
  $("#loading").hide();
}

function disableGameChat(){
  chatPlayer = null;
  $("#overlay").show();
  // $("#game-chat-2").addClass('disableDiv');
  $(".chat-character-dp").css('color', "#fff");
  // $("#chat-character-name").text('');
  $("#chat-body").html('')

}


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


$("#button-send").click(()=>sendChat());

function sendChat(){
  let message = $("#input-send").val()
  if (message != ""){
    socket.emit('chat', { mainPlayer, chatPlayer, message});
  }
  $("#input-send").val('');
  $("#loading").show();
}


// create an AudioListener and add it to the camera
const listener = new THREE.AudioListener();
camera.add( listener );

// create a global audio source
const sound = new THREE.Audio( listener );

// load a sound and set it as the Audio object's buffer
const audioLoader = new THREE.AudioLoader();
audioLoader.load( 'sounds.mp3', function( buffer ) {
	sound.setBuffer( buffer );
	sound.setLoop( true );
	sound.setVolume( 0.5 );
	sound.play();
});