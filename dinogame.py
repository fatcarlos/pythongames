from flask import Blueprint, Response

dino_bp = Blueprint("dino_game", __name__, url_prefix="/dinogame")

GAME_HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover"><meta name="theme-color" content="#101612"><title>BRICK REX — LEGO 3D RUNNER</title>
<style>
:root{color-scheme:dark}*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#090d0b;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;touch-action:manipulation}#game{position:fixed;inset:0;width:100%;height:100%;display:block;touch-action:none}#hud{position:fixed;inset:0;pointer-events:none;color:#e8e5d7;text-shadow:0 2px 8px #000;font-weight:800}#score{position:absolute;right:clamp(12px,3vw,38px);top:clamp(12px,2.5vh,28px);text-align:right;font-size:clamp(20px,3vw,35px);letter-spacing:2px;font-variant-numeric:tabular-nums}#best{display:block;font-size:clamp(11px,1.4vw,15px);letter-spacing:1.5px;color:#c5c9b6;margin-bottom:5px}#sound{position:absolute;left:clamp(12px,2vw,25px);top:clamp(12px,2.5vh,25px);pointer-events:auto;border:1px solid #87917a77;border-radius:3px;background:#080d0bd9;color:#eee;font:800 13px system-ui;padding:10px 13px;cursor:pointer}#view{position:absolute;left:clamp(12px,2vw,25px);top:clamp(58px,8vh,72px);pointer-events:auto;border:1px solid #87917a77;border-radius:3px;background:#080d0bd9;color:#eee;font:800 13px system-ui;padding:10px 13px;cursor:pointer}#sound,#view{backdrop-filter:blur(8px);box-shadow:0 5px 20px #0008}#panel{position:absolute;left:50%;top:46%;transform:translate(-50%,-50%);width:min(92vw,610px);padding:clamp(24px,4vw,44px);text-align:center;border:1px solid #a7a78b50;background:linear-gradient(145deg,#111914ed,#070a08f2);color:#e8e5d7;box-shadow:0 25px 90px #000b,inset 0 0 45px #6a2b1430;backdrop-filter:blur(8px)}#panel[hidden]{display:none}h1{font-size:clamp(36px,7vw,66px);line-height:.95;margin:0 0 14px;color:#c6c1a3;letter-spacing:clamp(3px,.8vw,9px);text-shadow:0 3px 0 #20251d,0 0 35px #b24c2650}#eyebrow{font-size:11px;letter-spacing:4px;color:#c36c4b;margin-bottom:12px}p{font-size:clamp(14px,2.2vw,18px);line-height:1.65;margin:0 0 23px;color:#d2d3c7}button{font:850 clamp(16px,2.5vw,21px) system-ui;border:1px solid #d58b65;border-radius:2px;padding:14px 28px;background:linear-gradient(#83432e,#43251d);color:#fff0df;box-shadow:0 5px 0 #1c120e,0 0 24px #b64b2733;cursor:pointer}button:active{transform:translateY(3px);box-shadow:0 2px 0 #1c120e}#help{position:absolute;left:50%;bottom:calc(86px + env(safe-area-inset-bottom));transform:translateX(-50%);font-size:clamp(11px,1.4vw,14px);letter-spacing:.4px;color:#e7e7d5;text-shadow:0 2px 6px #000;white-space:nowrap;text-align:center}.mobile{display:flex;position:fixed;left:0;right:0;bottom:calc(14px + env(safe-area-inset-bottom));justify-content:space-between;padding:0 16px;pointer-events:none;z-index:20}.mobile button{pointer-events:auto;min-width:76px;min-height:60px;padding:10px 17px;font-size:21px;background:#111813d9;color:#eee;box-shadow:none;border:1px solid #c2c4a566;border-radius:3px}@media(max-width:700px){#help{bottom:calc(86px + env(safe-area-inset-bottom));font-size:10px}#panel{top:42%}}
</style></head><body>
<canvas id="game" aria-label="3D dinosaur survival game"></canvas>
<div id="hud"><button id="sound">🔊 Sound: On</button><button id="view" title="Switch camera view">🎥 View: Side</button><div id="score"><span id="best">BEST 00000</span><span id="current">00000</span></div></div>
<div id="panel"><div id="eyebrow">BRICK WORLD • DINOSAUR RUN</div><h1 id="heading">PRIMAL</h1><p id="message">Enter the brick world.<br>Avoid cacti, flying birds and brick soldiers!</p><button id="action">START RUNNING ▶</button></div>
<div id="help">SPACE / ↑ JUMP  ·  ↓ DUCK  ·  C CHANGE VIEW  ·  On-screen controls are always available</div><div class="mobile"><button id="duck">↓ DUCK</button><button id="jump">↑ JUMP</button></div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>(()=>{'use strict';
const canvas=document.getElementById('game'),panel=document.getElementById('panel'),heading=document.getElementById('heading'),message=document.getElementById('message'),action=document.getElementById('action'),scoreText=document.getElementById('current'),bestText=document.getElementById('best'),soundButton=document.getElementById('sound'),viewButton=document.getElementById('view');
if(!window.THREE){heading.textContent='3D ENGINE UNAVAILABLE';message.textContent='Three.js could not be loaded. Check your internet connection and reload the game.';action.textContent='RELOAD';action.onclick=()=>location.reload();return;}
const THREE=window.THREE;
let renderer,scene,camera,clock,mode='ready',score=0,best=0,speed=15,spawnIn=1.1,elapsed=0,soundOn=true,audioCtx=null,master=null,musicTimer=null,ambienceTimer=null,musicBeat=0,lastFoot=0,ducking=false;
const cameraViews=[{name:'Chase',x:0,y:4.2,z:9.2,tx:0,ty:2.15,tz:-7.8},{name:'Side',x:29,y:8.2,z:2.2,tx:0,ty:1.8,tz:-9.5},{name:'Low angle',x:0,y:2.7,z:6.3,tx:0,ty:2.1,tz:-10.5},{name:'High angle',x:0,y:10.5,z:8.5,tx:0,ty:1.6,tz:-8.5}];let cameraViewIndex=1;
const obstacles=[],scenery=[],dust=[];const laneX=[-2.7,0,2.7];let lane=1,playerZ=1.5,groundY=0;
const mat=(color,roughness=.82,metalness=0)=>new THREE.MeshStandardMaterial({color,roughness,metalness});
const skin=mat(0x39483b,.93),skinLight=mat(0x59654d,.9),skinDark=mat(0x202b23,.95),belly=mat(0x827760,.98),mouthMat=mat(0x100b0a,.98),toothMat=mat(0xd8c9a5,.42),eyeMat=new THREE.MeshStandardMaterial({color:0xf0a12b,emissive:0x7a3105,emissiveIntensity:1.2,roughness:.22}),black=mat(0x080b08,.25),rockMat=mat(0x343a32),fernMat=mat(0x293c2a),woodMat=mat(0x302c23);
function makeRenderer(){renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:false,powerPreference:'high-performance'});renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,1.75));renderer.setSize(innerWidth,innerHeight);renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.15;scene=new THREE.Scene();scene.background=new THREE.Color(0x7bc9f5);scene.fog=new THREE.FogExp2(0x9bd7f5,.009);camera=new THREE.PerspectiveCamera(57,innerWidth/innerHeight,.1,180);clock=new THREE.Clock();}
function addLights(){scene.add(new THREE.HemisphereLight(0xe8f7ff,0x3c6a36,1.65));const sun=new THREE.DirectionalLight(0xfff1c9,3.0);sun.position.set(-12,22,5);sun.castShadow=true;sun.shadow.mapSize.set(1536,1536);sun.shadow.bias=-0.00018;sun.shadow.normalBias=0.025;sun.shadow.camera.left=-18;sun.shadow.camera.right=18;sun.shadow.camera.top=22;sun.shadow.camera.bottom=-22;scene.add(sun);const rim=new THREE.DirectionalLight(0x77c9ff,1.7);rim.position.set(8,8,-20);scene.add(rim);const red=new THREE.PointLight(0xb84c2b,35,35);red.position.set(-7,5,-20);scene.add(red);}
function makeGround(){
 // Smooth, uncluttered running surface: only gameplay hazards should demand attention.
 const floor=new THREE.Mesh(new THREE.PlaneGeometry(150,180),mat(0x4dbb55,.55));floor.rotation.x=-Math.PI/2;floor.position.z=-35;floor.receiveShadow=true;scene.add(floor);
 const path=new THREE.Mesh(new THREE.PlaneGeometry(8.4,180),mat(0xd5b46b,.82));path.rotation.x=-Math.PI/2;path.position.set(0,.025,-35);path.receiveShadow=true;scene.add(path);
}
function addFoliage(z,side){const group=new THREE.Group();group.position.set(side*(5.5+Math.random()*7),0,z);const trunk=new THREE.Mesh(new THREE.BoxGeometry(.65,1.8,.65),mat(0x9b5b2c,.55));trunk.position.y=.9;trunk.castShadow=true;group.add(trunk);for(let i=0;i<3;i++){const leaf=new THREE.Mesh(new THREE.BoxGeometry(1.55-i*.22,.8,1.4-i*.2),mat([0x16833a,0x29a84b,0x0d6b31][i],.48));leaf.position.set(0,1.75+i*.62,0);leaf.castShadow=true;group.add(leaf);for(let sx of [-.35,.35]){const stud=new THREE.Mesh(new THREE.CylinderGeometry(.09,.09,.06,8),mat(0x36c85d,.4));stud.position.set(sx,2.12+i*.62,.72-i*.1);group.add(stud);}}scene.add(group);scenery.push({mesh:group,kind:'tree',z});}
function makeWorld(){makeGround();for(let i=0;i<32;i++){const z=-8-i*4.7;addFoliage(z,-1);addFoliage(z,1);}const sky=new THREE.Mesh(new THREE.SphereGeometry(120,24,12),new THREE.MeshBasicMaterial({color:0x8bd5ff,side:THREE.BackSide}));scene.add(sky);}
function ell(parent,name,geo,material,pos,scale,rot){const m=new THREE.Mesh(geo,material);m.name=name;m.position.set(...pos);m.scale.set(...scale);if(rot)m.rotation.set(...rot);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
function bone(parent,name,a,b,r1,r2,material){const A=new THREE.Vector3(...a),B=new THREE.Vector3(...b),d=new THREE.Vector3().subVectors(B,A);const mesh=new THREE.Mesh(new THREE.CylinderGeometry(r2,r1,d.length(),9,1),material);mesh.name=name;mesh.position.copy(A).add(B).multiplyScalar(.5);mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());mesh.castShadow=true;parent.add(mesh);return mesh;}
function makeDino(){
 // LEGO-inspired T-Rex assembled from hard-edged plastic bricks and studs.
 const root=new THREE.Group();root.position.set(0,0,playerZ);scene.add(root);const rig=new THREE.Group();root.add(rig);
 const green=mat(0x4caf37,.32,.04),greenDark=mat(0x277d2a,.34,.03),lime=mat(0x80d34c,.3,.02),cream=mat(0xe7d9a5,.35),blackEye=mat(0x111820,.18),white=mat(0xffffff,.2),red=mat(0xc83225,.35),brickBlue=mat(0x1679d3,.32);
 const box=(parent,name,pos,size,material,rot=[0,0,0])=>{const m=new THREE.Mesh(new THREE.BoxGeometry(...size),material);m.name=name;m.position.set(...pos);m.rotation.set(...rot);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;};
 const stud=(parent,x,y,z,r=.095,color=lime)=>{const m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,.09,12),color);m.position.set(x,y,z);m.castShadow=true;parent.add(m);return m;};
 // blocky body and chest; facing -Z down the track
 box(rig,'hips',[0,1.5,.45],[1.25,1.05,1.35],green);
 box(rig,'torso',[0,2.12,-.18],[1.12,1.05,1.1],green);
 box(rig,'belly',[0,1.82,-.78],[.78,.68,.28],cream);
 // long segmented LEGO tail, tapering away behind the body
 const tailPivot=new THREE.Group();tailPivot.position.set(0,1.55,1.02);rig.add(tailPivot);
 box(tailPivot,'tail base',[0,0,.42],[.8,.72,.95],green,[.12,0,0]);box(tailPivot,'tail middle',[0,-.1,1.15],[.58,.52,.72],greenDark,[.16,0,0]);box(tailPivot,'tail tip',[0,-.18,1.72],[.34,.32,.55],green,[.18,0,0]);
 // upright neck and oversized square skull
 box(rig,'neck',[0,2.72,-.78],[.72,1.05,.68],green,[.22,0,0]);
 box(rig,'skull',[0,3.22,-1.38],[1.08,.86,1.12],green);
 box(rig,'snout',[0,3.02,-1.98],[1.02,.43,.78],lime);
 box(rig,'open mouth',[0,2.77,-1.96],[.88,.16,.75],red);
 box(rig,'lower jaw',[0,2.65,-1.9],[.9,.18,.76],greenDark);
 // big square eyes, black pupils, nostrils and individual triangular teeth
 for(const side of [-1,1]){box(rig,'eye white',[side*.555,3.35,-1.69],[.13,.2,.12],white);box(rig,'eye pupil',[side*.625,3.35,-1.72],[.055,.12,.055],blackEye);box(rig,'brow',[side*.55,3.49,-1.67],[.24,.1,.22],greenDark);box(rig,'nostril',[side*.28,3.12,-2.36],[.1,.07,.055],greenDark);}
 for(let i=0;i<6;i++){const x=-.38+i*.152;const tooth=new THREE.Mesh(new THREE.ConeGeometry(.075,.2,4),cream);tooth.position.set(x,2.86,-2.12);tooth.rotation.x=Math.PI;tooth.castShadow=true;rig.add(tooth);}
 // LEGO studs on head, back and tail emphasize the toy-brick aesthetic
 for(let i=0;i<5;i++){stud(rig,-.4+i*.2,3.68,-1.5,.075,lime);stud(rig,-.42+i*.21,2.7,.55,.085,greenDark);}
 for(let i=0;i<5;i++){const z=-.25+i*.32;box(rig,'back plate',[0,2.72,z],[.22,.22,.24],greenDark,[0,0,0]);}
 // short hinged forearms with tiny claws
 const arms=[];for(const side of [-1,1]){const arm=new THREE.Group();arm.position.set(side*.58,2.25,-.58);rig.add(arm);box(arm,'upper arm',[side*.08,-.08,-.12],[.22,.36,.24],greenDark,[.35,0,side*.18]);box(arm,'forearm',[side*.1,-.27,-.23],[.18,.22,.18],lime);for(let k=0;k<2;k++)box(arm,'claw',[side*.1+(k-.5)*.11,-.34,-.3],[.045,.12,.05],cream);arms.push(arm);}
 // two large hinged hind legs with square feet; absolutely bipedal
 const legs=[];for(const side of [-1,1]){const hip=new THREE.Group();hip.position.set(side*.43,1.28,.42);rig.add(hip);box(hip,'thigh',[0,-.22,0],[.48,.76,.52],greenDark);const knee=new THREE.Group();knee.position.set(0,-.58,-.05);hip.add(knee);box(knee,'shin',[0,-.22,-.06],[.34,.66,.36],green);const foot=new THREE.Group();foot.position.set(0,-.54,-.16);knee.add(foot);box(foot,'foot',[0,-.04,-.17],[.52,.18,.48],lime);for(let k=0;k<3;k++)box(foot,'toe',[(k-1)*.15,-.06,-.39],[.12,.11,.18],greenDark);legs.push({hip,knee,foot,side});}
 root.userData={rig,tailPivot,legs,arms};return root;}
let dino;
function makeObstacle(type,x,z){const g=new THREE.Group();g.position.set(x,0,z);const box=(pos,size,color,rot=[0,0,0])=>{const m=new THREE.Mesh(new THREE.BoxGeometry(...size),mat(color,.38,.02));m.position.set(...pos);m.rotation.set(...rot);m.castShadow=true;m.receiveShadow=true;g.add(m);return m;};const stud=(pos,color)=>{const m=new THREE.Mesh(new THREE.CylinderGeometry(.09,.09,.07,10),mat(color,.3));m.position.set(...pos);m.castShadow=true;g.add(m);};
 if(type==='cactus'){const green=0x25a849,light=0x4acb5a;box([0,.85,0],[.52,1.7,.48],green);box([-.42,.75,0],[.28,.72,.32],light,[0,0,-.22]);box([-.3,1.08,0],[.48,.27,.32],green);box([.42,1.12,0],[.28,.75,.32],light,[0,0,.2]);box([.3,1.42,0],[.45,.25,.32],green);for(let y=.45;y<1.5;y+=.38)stud([-.03,y,-.255],0x91e96d);}
 else if(type==='bird'){g.position.y=1.9;const blue=0x176bd1,yellow=0xffd52e;box([0,0,0],[.45,.34,.55],blue);box([0,.13,-.35],[.25,.2,.34],blue);box([0,.06,-.55],[.13,.1,.2],yellow);box([-.42,.03,0],[.62,.12,.28],yellow);box([.42,.03,0],[.62,.12,.28],yellow);const left=box([-.48,.12,-.02],[.65,.1,.5],blue),right=box([.48,.12,-.02],[.65,.1,.5],blue);box([-.1,.17,-.42],[.08,.08,.06],0xffffff);box([.1,.17,-.42],[.08,.08,.06],0xffffff);g.userData.wings=[left,right];}
 else if(type==='soldier'){const green=0x426b37,skinTone=0xffc58c,black=0x253027;box([0,1.25,0],[.72,.82,.42],green);box([0,1.84,0],[.5,.45,.45],skinTone);box([0,2.08,0],[.62,.18,.56],0x344e2d);box([0,2.2,0],[.56,.16,.52],0x344e2d);box([-.2,.45,0],[.22,.78,.28],black);box([.2,.45,0],[.22,.78,.28],black);box([-.43,1.25,0],[.2,.68,.25],green,[0,0,-.12]);box([.43,1.25,0],[.2,.68,.25],green,[0,0,.12]);box([.32,1.15,-.28],[.14,.16,.85],0x202722,[.15,0,0]);box([.32,1.18,-.72],[.12,.12,.25],0x111713);for(let sx of [-.18,.18])stud([sx,2.12,-.27],0x8eb46a);}
 scene.add(g);const h=type==='bird'?2.3:type==='soldier'?2.2:1.7;obstacles.push({mesh:g,type,x,z,w:type==='cactus'?1.15:1.25,h});}
function spawnObstacle(){const r=Math.random();const type=r<.43?'cactus':r<.7?'bird':'soldier';const lanePick=Math.floor(Math.random()*3);makeObstacle(type,laneX[lanePick],-72);if(score>250&&Math.random()<.2){const other=(lanePick+1+Math.floor(Math.random()*2))%3;makeObstacle(Math.random()<.5?'cactus':'soldier',laneX[other],-86);}}
function initAudio(){if(!soundOn)return;try{if(!audioCtx){audioCtx=new(window.AudioContext||window.webkitAudioContext)();master=audioCtx.createGain();master.gain.value=1.0;const comp=audioCtx.createDynamicsCompressor();comp.threshold.value=-18;comp.knee.value=18;comp.ratio.value=5;comp.attack.value=.004;comp.release.value=.22;master.connect(comp);comp.connect(audioCtx.destination);}if(audioCtx.state==='suspended')audioCtx.resume();startAudioBeds();}catch(e){}}
function tone(freq,dur,wave='sine',vol=.12,end=null,delay=0){if(!soundOn||!audioCtx)return;try{const t=audioCtx.currentTime+delay,o=audioCtx.createOscillator(),g=audioCtx.createGain(),f=audioCtx.createBiquadFilter();o.type=wave;o.frequency.setValueAtTime(Math.max(18,freq),t);if(end)o.frequency.exponentialRampToValueAtTime(Math.max(18,end),t+dur);f.type='lowpass';f.frequency.value=wave==='sawtooth'?2600:1900;g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(Math.max(.0002,vol),t+.012);g.gain.setValueAtTime(Math.max(.0002,vol),Math.max(t+.013,t+dur*.55));g.gain.exponentialRampToValueAtTime(.0001,t+dur);o.connect(f);f.connect(g);g.connect(master);o.start(t);o.stop(t+dur+.04);}catch(e){}}
function noise(dur=.2,vol=.1,cutoff=500){if(!soundOn||!audioCtx)return;try{const n=Math.max(1,Math.floor(audioCtx.sampleRate*dur)),b=audioCtx.createBuffer(1,n,audioCtx.sampleRate),a=b.getChannelData(0);for(let i=0;i<n;i++)a[i]=(Math.random()*2-1)*(1-i/n);const src=audioCtx.createBufferSource(),f=audioCtx.createBiquadFilter(),g=audioCtx.createGain();src.buffer=b;f.type='lowpass';f.frequency.value=cutoff;g.gain.value=vol;src.connect(f);f.connect(g);g.connect(master);src.start();}catch(e){}}
function roar(){tone(92,1.3,'sawtooth',.48,29);tone(59,1.4,'triangle',.42,22,.04);tone(180,.7,'sawtooth',.25,43,.1);noise(.95,.34,650);}
function guitarChord(root,delay=0,dur=.22,vol=.105){[1,1.26,1.5,2].forEach((r,i)=>tone(root*r,dur,'sawtooth',vol/(i===0?1:1.65),root*r*.92,delay+i*.004));noise(.055,vol*.65,2400);}
function kick(vol=.32){tone(105,.18,'sine',vol,38);noise(.11,vol*.45,150);}
function snare(vol=.18){noise(.16,vol,2200);tone(185,.09,'triangle',vol*.5,85);}
function cymbal(vol=.12){noise(.32,vol,7000);}
function startAudioBeds(){
 if(!audioCtx||!soundOn)return;
 if(!musicTimer){
  musicBeat=0;
  // Original cheerful major-key game loop: bright plucks, bouncy bass and light taps.
  const melody=[523.25,659.25,783.99,659.25,587.33,698.46,880,698.46,
                523.25,659.25,783.99,1046.5,880,783.99,659.25,587.33];
  const bass=[130.81,130.81,164.81,164.81,174.61,174.61,146.83,146.83];
  musicTimer=setInterval(()=>{
   if(!soundOn||!audioCtx||mode==='over')return;
   const step=musicBeat%16;
   const note=melody[step];
   tone(note,.17,'triangle',.105,note*1.015);
   if(step%2===0)tone(bass[(step/2)%8],.22,'sine',.075,bass[(step/2)%8]*.98);
   if(step%4===0)tone(880,.045,'sine',.035,660,.025);
   if(step%4===2)tone(1174.66,.04,'sine',.025,880,.025);
   musicBeat++;
  },175);
 }
}
function playRetroGameOver(){if(!soundOn||!audioCtx)return;/* Original gentle, playful end-of-round jingle. */[659.25,783.99,880,1046.5].forEach((f,i)=>tone(f,.18,'triangle',.11,f*.99,i*.13));tone(783.99,.32,'sine',.09,659.25,.56);}
function stopAudioBeds(){if(musicTimer){clearInterval(musicTimer);musicTimer=null;}if(ambienceTimer){clearInterval(ambienceTimer);ambienceTimer=null;}}
function jumpSound(){tone(160,.22,'sawtooth',.2,650);noise(.15,.13,1000);}function stepSound(){tone(62,.16,'triangle',.19,29);noise(.12,.15,200);}function impactSound(){tone(75,.3,'triangle',.28,20);noise(.28,.24,260);}
soundButton.addEventListener('click',()=>{soundOn=!soundOn;soundButton.textContent=soundOn?'🔊 Sound: On':'🔇 Sound: Off';if(soundOn){initAudio();tone(440,.12,'sine',.06,660);}else stopAudioBeds();});
function cycleCamera(){cameraViewIndex=(cameraViewIndex+1)%cameraViews.length;viewButton.textContent='🎥 View: '+cameraViews[cameraViewIndex].name;}
viewButton.addEventListener('click',cycleCamera);
function start(){initAudio();stopAudioBeds();startAudioBeds();roar();score=0;speed=15;spawnIn=1.05;elapsed=0;lane=1;ducking=false;dino.position.set(0,0,playerZ);dino.userData.rig.position.y=0;for(const o of obstacles)scene.remove(o.mesh);obstacles.length=0;mode='running';panel.hidden=true;scoreText.textContent='00000';clock.getDelta();}
function endGame(){if(mode!=='running')return;mode='over';stopAudioBeds();impactSound();playRetroGameOver();const n=Math.floor(score);if(n>best){best=n;try{localStorage.setItem('salaryDino3DBest',String(best));}catch(e){}bestText.textContent='BEST '+String(best).padStart(5,'0');}heading.textContent='HUNT ENDED';message.innerHTML='Your score: <b>'+String(n).padStart(5,'0')+'</b><br>The prehistoric arena is waiting. Ready for another run?';action.textContent='RUN AGAIN ↻';panel.hidden=false;}
let vy=0,onGround=true;function jump(){if(mode!=='running'){start();return;}if(onGround){vy=10.8;onGround=false;ducking=false;jumpSound();}}
function setDuck(v){if(mode==='running')ducking=v;}
function updateDino(dt){const {rig,tailPivot,legs,arms}=dino.userData;const t=elapsed;dino.position.x=THREE.MathUtils.damp(dino.position.x,laneX[lane],6,dt);if(!onGround){vy-=25*dt;dino.position.y+=vy*dt;if(dino.position.y<=0){dino.position.y=0;vy=0;onGround=true;impactSound();}}const run=t*speed*.48;rig.rotation.x=ducking&&onGround?.26:Math.sin(run*2)*.035;rig.position.y=onGround?(ducking?-.35:Math.abs(Math.sin(run*2))*.055):0;tailPivot.rotation.x=Math.sin(run*1.1)*.12;tailPivot.rotation.y=Math.sin(run*.6)*.12;legs.forEach((l,i)=>{const phase=run+(i?Math.PI:0);l.hip.rotation.x=Math.sin(phase)*.62;l.knee.rotation.x=Math.max(0,Math.sin(phase+1))*.72;l.foot.rotation.x=-Math.max(0,Math.sin(phase+1))*.45;});arms.forEach((a,i)=>{a.rotation.x=Math.sin(run+(i?Math.PI:0))*.13;});if(onGround&&!ducking&&t-lastFoot>.34*(15/speed)){stepSound();lastFoot=t;}}
function update(dt){if(mode!=='running')return;elapsed+=dt;score+=dt*speed*8;speed=Math.min(31,15+score*.006);scoreText.textContent=String(Math.floor(score)).padStart(5,'0');updateDino(dt);spawnIn-=dt;if(spawnIn<=0){spawnObstacle();spawnIn=Math.max(.65,1.45-Math.min(.7,(speed-15)*.035)+Math.random()*.55);}for(let i=obstacles.length-1;i>=0;i--){const o=obstacles[i];o.mesh.position.z+=speed*dt;if(o.type==='bird'&&o.mesh.userData.wings){const flap=Math.sin(elapsed*15)*.38;o.mesh.userData.wings[0].rotation.z=flap;o.mesh.userData.wings[1].rotation.z=-flap;}if(o.mesh.position.z>camera.position.z+4){scene.remove(o.mesh);obstacles.splice(i,1);continue;}const dx=Math.abs(o.mesh.position.x-dino.position.x),dz=Math.abs(o.mesh.position.z-dino.position.z);const height=ducking?.85:2.9;const laneHit=dx<(o.type==='bird'?1.05:1.0)&&dz<(o.type==='bird'?1.35:1.25);const hitsBird=o.type==='bird'&&height>1.1;const hitsGround=o.type!=='bird'&&dino.position.y<o.h;if(laneHit&&(hitsBird||hitsGround)){endGame();break;}}
 for(const s of scenery){s.mesh.position.z+=speed*dt*.78;if(s.mesh.position.z>camera.position.z+9){s.mesh.position.z=-130-Math.random()*35;if(s.kind==='tree'){s.mesh.position.x=Math.sign(s.mesh.position.x)*(5.5+Math.random()*7);} }}
 // Switchable cinematic camera presets. Camera remains smooth while the game keeps running.
 let view=cameraViews[cameraViewIndex];
 // Portrait phones need a less extreme side angle and more distance behind the runner.
 // This keeps the whole dinosaur inside the narrow horizontal field of view.
 if(cameraViewIndex===1 && innerWidth/innerHeight<0.8){
  view={name:'Side',x:11.5,y:5.8,z:8.5,tx:0,ty:1.55,tz:-5.5};
 }else if(cameraViewIndex===1){
  view={name:'Side',x:22,y:7.2,z:8.5,tx:0,ty:1.65,tz:-7.5};
 }
 const desiredX=dino.position.x+view.x;
 const desiredY=view.y+dino.position.y*.3;
 const desiredZ=playerZ+view.z;
 const target=new THREE.Vector3(dino.position.x*.22+view.tx,view.ty+dino.position.y*.22,playerZ+view.tz);
 camera.position.x=THREE.MathUtils.damp(camera.position.x,desiredX,2.8,dt);
 camera.position.y=THREE.MathUtils.damp(camera.position.y,desiredY,2.4,dt);
 camera.position.z=THREE.MathUtils.damp(camera.position.z,desiredZ,2.4,dt);
 camera.lookAt(target);
 if(cameraViewIndex===0)camera.rotation.z=THREE.MathUtils.damp(camera.rotation.z,(laneX[lane]-dino.position.x)*-.018,3,dt);
}
function render(){requestAnimationFrame(render);const dt=Math.min(.035,clock.getDelta());update(dt);renderer.render(scene,camera);}
function resize(){if(!renderer)return;renderer.setSize(innerWidth,innerHeight);camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();}
function moveLane(dir){if(mode!=='running')return;lane=Math.max(0,Math.min(2,lane+dir));}
action.addEventListener('click',start);canvas.addEventListener('pointerdown',e=>{if(mode!=='running'){start();return;}if(e.clientX<innerWidth*.32)moveLane(-1);else if(e.clientX>innerWidth*.68)moveLane(1);else jump();});addEventListener('keydown',e=>{if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code))e.preventDefault();if(e.code==='Space'||e.code==='ArrowUp'||e.code==='KeyW')jump();if(e.code==='ArrowDown'||e.code==='KeyS')setDuck(true);if(e.code==='ArrowLeft'||e.code==='KeyA')moveLane(-1);if(e.code==='ArrowRight'||e.code==='KeyD')moveLane(1);if(e.code==='KeyC')cycleCamera();if(e.code==='Enter'&&mode!=='running')start();},{passive:false});addEventListener('keyup',e=>{if(e.code==='ArrowDown'||e.code==='KeyS')setDuck(false);});document.getElementById('jump').addEventListener('pointerdown',e=>{e.preventDefault();jump();});document.getElementById('duck').addEventListener('pointerdown',e=>{e.preventDefault();setDuck(true);});['pointerup','pointercancel','pointerleave'].forEach(ev=>document.getElementById('duck').addEventListener(ev,()=>setDuck(false)));addEventListener('resize',resize);
try{best=Number(localStorage.getItem('salaryDino3DBest')||0)||0;}catch(e){}bestText.textContent='BEST '+String(best).padStart(5,'0');
makeRenderer();addLights();makeWorld();dino=makeDino();
 if(innerWidth/innerHeight<0.8){camera.position.set(11.5,5.8,playerZ+8.5);camera.lookAt(0,1.55,playerZ-5.5);}
 else{camera.position.set(22,7.2,playerZ+8.5);camera.lookAt(0,1.65,playerZ-7.5);}
 render();
})();</script></body></html>'''

@dino_bp.get("/")
def play_dino_run():
    # Serve the true 3D browser game at the existing /dinogame/ route.
    return Response(GAME_HTML, mimetype="text/html; charset=utf-8")
