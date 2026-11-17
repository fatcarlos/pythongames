"""English Big 2 (Big Two) browser game for the Salary Tool portal."""
import os
from flask import Blueprint, Response, send_from_directory

big2_bp = Blueprint("big2_game", __name__, url_prefix="/big2")

@big2_bp.get("/background.png")
def big2_background():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "background.png")

GAME_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="theme-color" content="#08251b">
<title>BIG 2 — Card Game</title>
<style>
:root{color-scheme:dark}*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#08251b;color:#f7f5e9;font-family:system-ui,-apple-system,Segoe UI,sans-serif}
body{background:#061b14 url("/big2/background.png") center center/cover no-repeat}
#top{position:absolute;z-index:5;left:0;right:0;top:0;background:linear-gradient(180deg,#04130edb,#04130e70);border-bottom:1px solid #d9b45a55}
#table{position:absolute;z-index:1;inset:0;border:0;border-radius:0;background:transparent;box-shadow:none;overflow:hidden}
#tableStatus{display:none}
#seat0{left:50%;bottom:145px;transform:translateX(-50%)}
#seat1{right:8%;top:38%;transform:translateY(-50%)}
#seat2{left:50%;top:7%;transform:translateX(-50%)}
#seat3{left:8%;top:38%;transform:translateY(-50%)}
#center{top:42%;width:min(82%,620px)}


#handArea{position:absolute;z-index:4;background:linear-gradient(180deg,#061b1488,#03130fd9);border-top:1px solid #d8b45c55}



@media(max-width:700px){#seat1{right:2%;top:39%}#seat3{left:2%;top:39%}#seat0{bottom:145px}#center{top:41%}}
#top{height:58px;display:flex;align-items:center;justify-content:space-between;padding:0 18px;border-bottom:1px solid #ffffff25;background:#041b14aa}
h1{font-size:clamp(18px,3vw,26px);letter-spacing:3px;margin:0;color:#f6d77a}
#topRight{display:flex;align-items:center;gap:10px}
#topRight label{font-size:11px;color:#f6d77a;font-weight:800;letter-spacing:1px}
#aiLevel{padding:5px 9px;border:1px solid #a9c5b2;border-radius:6px;background:#123d2d;color:#fff;font-size:12px}
#stakeSelect{padding:5px 7px;border:1px solid #d2b66b;border-radius:6px;background:#123d2d;color:#ffe08a;font-size:12px;font-weight:800}
#stakeSelect:disabled,#aiLevel:disabled{opacity:.55;cursor:not-allowed}

.money-panel{display:flex;flex-direction:column;align-items:center;line-height:1.05;white-space:nowrap} .active-settings{display:flex;flex-direction:column;gap:3px;padding:4px 8px;border:1px solid #648b73;border-radius:7px;background:#0b3023;white-space:nowrap;font-size:10px;color:#c6ddcc;line-height:1.2}.active-settings strong{color:#f6d77a;font-size:11px;margin-left:3px}
.money-label{font-size:9px;letter-spacing:1px;color:#b9d4c2}
#balance{font-size:13px;color:#f6d77a;font-variant-numeric:tabular-nums}

.icon-toggle{width:32px;height:30px;padding:0!important;display:inline-flex;align-items:center;justify-content:center;border:1px solid #9cb8a5;border-radius:7px;background:#173f31;color:#f7f5e9;font-size:19px;line-height:1;box-shadow:none}
.icon-toggle.active{background:linear-gradient(#d9ad45,#9b6d20);border-color:#f4d36c;color:#17130a}
.icon-toggle:focus-visible{outline:2px solid #fff;outline-offset:2px}
.top-new-game{padding:6px 10px!important;border-radius:6px;font-size:11px;white-space:nowrap;box-shadow:0 2px 0 #533a16}
.top-new-game:disabled{opacity:.4}



#tableStatus{position:absolute;left:50%;bottom:48px;transform:translateX(-50%);width:min(88%,560px);text-align:center;font-size:13px;color:#d7e8d9;text-shadow:0 1px 3px #00190f;pointer-events:none;z-index:2}
#table{position:absolute;inset:68px 12px 150px;border:2px solid #d2b66b66;border-radius:28px;background:radial-gradient(ellipse,#1d8056 0,#11603f 58%,#0b422d 100%);box-shadow:inset 0 0 50px #03190f88,0 14px 45px #0005}
.seat{position:absolute;min-width:120px;text-align:center;font-size:13px;color:#dbe9dc}
.seat strong{display:block;color:#ffe08a;font-size:14px}.seat .count{opacity:.8;font-size:12px}

/* One-card warning: red glow + flashing reminder */
@keyframes oneCardAlertPulse{
 0%,100%{color:#ff3434;text-shadow:0 0 4px #ff0000,0 0 10px #ff0000,0 0 18px #ff2020;filter:drop-shadow(0 0 5px #ff0000)}
 50%{color:#fff0f0;text-shadow:0 0 8px #ff0000,0 0 18px #ff0000,0 0 30px #ff2020;filter:drop-shadow(0 0 11px #ff2020)}
}
.one-card-alert strong>span:first-child,.one-card-alert .count{color:#ff3838!important;animation:oneCardAlertPulse .75s ease-in-out infinite;opacity:1!important}
.one-card-alert .opponent-card{border-color:#ff2929;box-shadow:0 0 5px #ff0000,0 0 12px #ff2020;animation:oneCardAlertPulse .75s ease-in-out infinite}
#hand.one-card-alert .hand-card{outline:2px solid #ff2929;box-shadow:0 0 8px #ff0000,0 0 18px #ff2020;animation:oneCardAlertPulse .75s ease-in-out infinite}
.opponent-cards{display:flex;justify-content:center;align-items:center;height:42px;margin-top:4px;overflow:visible}
.opponent-card{flex:0 0 auto;width:19px;height:34px;border-radius:4px;border:1px solid #fff;background:repeating-linear-gradient(45deg,#174b83,#174b83 4px,#e8e1ce 4px,#e8e1ce 6px);box-shadow:0 2px 4px #0006}
.opponent-card+.opponent-card{margin-left:-11px}
#seat1 .opponent-cards,#seat3 .opponent-cards{flex-direction:column;height:auto;margin-top:5px}
#seat1 .opponent-card+.opponent-card,#seat3 .opponent-card+.opponent-card{margin-left:0;margin-top:-25px}
#seat1 .opponent-card,#seat3 .opponent-card{width:24px;height:33px}
@media(max-width:600px){
 .opponent-cards{height:34px;margin-top:2px}
 .opponent-card{width:15px;height:27px}
 .opponent-card+.opponent-card{margin-left:-9px}
 #seat1 .opponent-card,#seat3 .opponent-card{width:20px;height:28px}
 #seat1 .opponent-card+.opponent-card,#seat3 .opponent-card+.opponent-card{margin-top:-22px}
}
#seat0{left:50%;bottom:12px;transform:translateX(-50%)}#seat1{right:12px;top:50%;transform:translateY(-50%)}#seat2{left:50%;top:10px;transform:translateX(-50%)}#seat3{left:12px;top:50%;transform:translateY(-50%)}
#center{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:min(82%,620px);min-height:145px;text-align:center}

@media(max-width:600px){}
#trickLabel{font-size:12px;letter-spacing:2px;color:#f5d77d;margin-bottom:10px}

@media(max-width:600px){}

#played{display:flex;justify-content:center;align-items:center;gap:5px;flex-wrap:wrap;min-height:90px}
.card{width:clamp(44px,6vw,64px);height:clamp(66px,9vw,94px);border-radius:7px;background:#fffdf5;color:#171717;border:1px solid #d7d2c5;box-shadow:0 4px 9px #0005;display:flex;flex-direction:column;justify-content:space-between;padding:5px;font-weight:850;position:relative;user-select:none}
.card.red{color:#c62828}.card .rank{font-size:clamp(14px,2vw,20px);line-height:1}.card .suit{font-size:clamp(19px,3vw,28px);align-self:center}
.card.back{background:repeating-linear-gradient(45deg,#174b83,#174b83 5px,#e8e1ce 5px,#e8e1ce 7px);border:3px solid #fff}
#handArea{position:absolute;left:0;right:0;bottom:0;height:144px;padding:8px 12px calc(8px + env(safe-area-inset-bottom));background:linear-gradient(#061b14aa,#03130f);border-top:1px solid #ffffff25}
#hand{height:90px;display:flex;justify-content:center;align-items:flex-end;gap:clamp(0px,.7vw,7px);overflow-x:auto;overflow-y:visible;padding:4px 4px 8px}
.hand-card{flex:0 0 auto;width:clamp(32px,5.4vw,54px);height:clamp(62px,8vw,82px);padding:4px;cursor:pointer;transition:transform .12s,bottom .12s}
.hand-card.selected{transform:translateY(-15px);outline:3px solid #f4d36c}
#controls{display:flex;justify-content:center;align-items:center;column-gap:26px;row-gap:12px;margin-top:8px;flex-wrap:wrap}
#comboButtons{margin-right:12px}
#playSelectedBtn{margin-left:12px;min-width:112px}#passBtn{margin-left:16px;min-width:76px}
@media(max-width:700px){#controls{column-gap:22px;row-gap:12px;margin-top:10px}#comboButtons{margin-right:8px}#playSelectedBtn{margin-left:8px;min-width:104px}#passBtn{margin-left:12px;min-width:76px}}
#comboButtons{display:flex;justify-content:center;align-items:center;gap:5px;flex-wrap:wrap;max-width:min(78vw,900px)}
.combo-btn{display:inline-flex;align-items:center;padding:7px 10px;font-size:11px;line-height:1.1;border-radius:7px;background:linear-gradient(145deg,#244f3c,#102b20);border:1px solid #c5a45a;color:#f6df9b;box-shadow:0 2px 0 #061b14;white-space:nowrap}
.combo-btn:active{transform:translateY(1px)}
.combo-btn:disabled{opacity:.28}
@media(max-width:700px){#controls{gap:6px}#comboButtons{gap:4px;max-width:calc(100vw - 18px)}.combo-btn{padding:6px 7px;font-size:10px}#passBtn{padding:7px 14px}}
button{border:1px solid #e2c56d;border-radius:7px;padding:9px 20px;background:linear-gradient(#d9ad45,#9b6d20);color:#17130a;font-weight:900;cursor:pointer;box-shadow:0 3px 0 #533a16}
button.secondary{background:#173f31;color:#f7f5e9;border-color:#9cb8a5;box-shadow:0 3px 0 #061b14}
button:disabled{opacity:.4;cursor:not-allowed}
#hint{font-size:12px;color:#d8e5d8;text-align:center;margin-top:5px;min-height:16px}
#overlay{position:absolute;inset:0;z-index:10;display:grid;place-items:center;background:#00150fc9;padding:20px}
#overlay[hidden]{display:none}
#dialog{width:min(92vw,470px);text-align:center;padding:28px;border:1px solid #d8bd72;border-radius:16px;background:linear-gradient(145deg,#174c37,#08251b);box-shadow:0 20px 70px #0009}
#dialog h2{font-size:clamp(28px,6vw,44px);letter-spacing:3px;color:#f5d77d;margin:0 0 12px}
#dialog p{line-height:1.6;color:#e4eee3}
#dialog button{margin-top:8px} .setup-fields{display:flex;justify-content:center;gap:14px;margin:18px 0 12px;flex-wrap:wrap}.setup-field{display:flex;flex-direction:column;align-items:flex-start;gap:6px;min-width:145px;text-align:left}.setup-field label{font-size:11px;color:#f6d77a;font-weight:800;letter-spacing:1px}.setup-field select{width:100%;padding:9px 10px;border:1px solid #d2b66b;border-radius:7px;background:#123d2d;color:#ffe08a;font-size:14px;font-weight:800}.setup-field select:disabled{opacity:.55;cursor:not--allowed}
@media(max-width:600px){.active-settings{font-size:8px;padding:3px 5px;gap:2px}.active-settings strong{font-size:9px}#top{padding:0 8px}#topRight{gap:5px;flex-wrap:wrap;justify-content:flex-end}#topRight label{font-size:9px}.money-label{font-size:8px}#balance{font-size:10px}.icon-toggle{width:27px;height:26px;font-size:16px}#tableStatus{font-size:10px;bottom:42px}#table{inset:66px 6px 145px;border-radius:18px}.seat{min-width:78px;font-size:11px}.seat strong{font-size:12px}#seat1{right:3px}#seat3{left:3px}#center{width:78%}#handArea{height:142px;padding-left:3px;padding-right:3px}#hand{justify-content:flex-start}button{padding:9px 15px}}

/* The casino artwork is the only table surface; keep the game layer fully transparent. */
html,body{background-color:#061b14!important}
body{background-image:url("/big2/background.png")!important;background-position:center center!important;background-size:cover!important;background-repeat:no-repeat!important;background-color:#061b14!important}
#table{background:transparent!important;background-image:none!important;border:0!important;border-radius:0!important;box-shadow:none!important}
#table::before,#table::after{content:none!important;display:none!important}

/* Portrait: fill the screen with the center of the casino artwork, preserving its aspect ratio. */
@media (orientation:portrait){
 html,body{min-height:100%;}
 body{background-size:cover!important;background-position:center center!important;background-repeat:no-repeat!important;}
}
@media (orientation:landscape){
 body{background-size:cover!important;background-position:center center!important;background-repeat:no-repeat!important;}
}
#seat0{position:absolute}
#seat0 #hint{position:absolute;left:50%;bottom:calc(100% + 14px);transform:translateX(-50%);width:max-content;max-width:min(88vw,560px);min-height:0;margin:0;padding:7px 13px;border:1px solid #c6a65c;border-radius:18px;background:linear-gradient(145deg,#071b14eF,#0c3527eF);box-shadow:0 3px 12px #0008;color:#f5df9c;font-size:clamp(11px,1.15vw,14px);line-height:1.3;text-align:center;white-space:normal;z-index:4;pointer-events:none}
@media(max-width:700px){#seat0 #hint{bottom:calc(100% + 12px);font-size:11px;padding:6px 10px;max-width:88vw}}

#controls{column-gap:26px!important;row-gap:12px!important}
#comboButtons{margin-right:12px!important}
#passBtn{margin-left:12px!important;min-width:76px}
@media(max-width:700px){#controls{column-gap:22px!important;row-gap:12px!important}#comboButtons{margin-right:8px!important}#passBtn{margin-left:8px!important}}

#playerActionButtons{position:absolute;left:50%;bottom:calc(100% + 48px);transform:translateX(-50%);display:flex;align-items:center;justify-content:center;gap:18px;z-index:6;width:max-content;max-width:92vw}
#playerActionButtons #playSelectedBtn{margin:0;min-width:130px}
#playerActionButtons #passBtn{margin:0;min-width:82px}
#seat0 #hint{bottom:calc(100% + 10px)}
@media(max-width:700px){
 #playerActionButtons{bottom:calc(100% + 48px);gap:16px}
 #playerActionButtons #playSelectedBtn{min-width:124px}
 #playerActionButtons #passBtn{min-width:82px}
 #seat0 #hint{bottom:calc(100% + 8px)}
}

.seat strong{display:flex;align-items:center;justify-content:center;gap:7px;white-space:nowrap}
.seat-balance{font-size:11px;font-weight:700;color:#f6d77a;padding:2px 5px;border:1px solid #d4b35c66;border-radius:6px;background:#061b14a8}
#roundBalanceBoard{position:absolute;left:27%;top:9%;width:clamp(155px,19vw,235px);z-index:3;padding:4px 6px;border:1px solid #c8a552;border-radius:7px;background:linear-gradient(145deg,#061b14eF,#0c3527eF);box-shadow:0 4px 14px #0009;color:#f5e6b7;font-size:11px}
.round-history-entry{padding:0;margin:0}.round-history-title{font-size:8px;color:#f4d276;font-weight:900;letter-spacing:.3px;padding:1px 0}.round-balance-row{display:grid;grid-template-columns:1fr auto;gap:4px;padding:1px 0;border-top:1px solid #ffffff16;align-items:center}
.round-balance-row .rb-name{font-weight:800}
.round-balance-row .rb-change{font-variant-numeric:tabular-nums}

.round-balance-row .positive{color:#8ce0a2}.round-balance-row .negative{color:#ff9b91}
@media(max-width:700px){
 #roundBalanceBoard{left:3%;top:13%;width:clamp(145px,42vw,190px);padding:3px 4px;font-size:9px}
  .round-balance-row{gap:3px;padding:1px 0}
 .seat strong{gap:4px;flex-wrap:wrap}
 .seat-balance{font-size:9px;padding:1px 3px}
}

@media(min-width:701px){
 #handArea{height:178px;padding-top:10px;padding-bottom:10px}
 #hand{height:112px}
}

#roundBalanceBoard{width:max-content!important;min-width:0!important;max-width:92vw!important;padding:4px 6px!important}
#roundBalanceRows{width:max-content;max-width:100%}
.round-history-entry{width:max-content;max-width:100%}
.round-balance-row{display:grid!important;grid-template-columns:max-content max-content!important;justify-content:start;column-gap:12px!important;min-width:0}
@media(max-width:700px){
 #roundBalanceBoard{width:max-content!important;max-width:92vw!important}
 .round-balance-row{column-gap:10px!important}
}

#roundBalanceBoard{top:0!important;left:7px!important;right:auto!important;width:max-content!important;min-width:0!important;max-width:min(92vw,280px)!important;padding:3px 5px!important;margin:0!important}
#roundBalanceToggle{display:block;width:100%;margin:0 0 1px;padding:1px 2px;border:0;background:transparent;color:#f4d276;font-size:8px;font-weight:900;letter-spacing:.45px;text-align:left;cursor:pointer;line-height:1.15}
#roundBalanceRows{width:max-content;max-width:100%;margin:0;padding:0}
.round-history-entry{width:max-content;max-width:100%;padding:0!important;margin:0!important}
.round-history-title{padding:0!important;margin:0!important;line-height:1.1}
.round-balance-row{padding:0!important;margin:0!important;line-height:1.15}
@media(max-width:700px){
 #roundBalanceBoard{top:0!important;left:3px!important;max-width:70vw!important}
 #roundBalanceToggle{font-size:8px}
}

/* Larger opponent card backs: West, North and East */
#seat1 .opponent-card,#seat2 .opponent-card,#seat3 .opponent-card{
 width:28px!important;height:42px!important;border-radius:5px!important;
}
#seat1 .opponent-card+.opponent-card,#seat3 .opponent-card+.opponent-card{margin-top:-31px!important}
#seat2 .opponent-card+.opponent-card{margin-left:-17px!important}
#seat1 .opponent-cards,#seat3 .opponent-cards{min-height:42px}
#seat2 .opponent-cards{height:46px!important}
@media(max-width:600px){
 #seat1 .opponent-card,#seat2 .opponent-card,#seat3 .opponent-card{width:26px!important;height:39px!important}
 #seat1 .opponent-card+.opponent-card,#seat3 .opponent-card+.opponent-card{margin-top:-29px!important}
 #seat2 .opponent-card+.opponent-card{margin-left:-16px!important}
 #seat2 .opponent-cards{height:43px!important}
}
</style>
</head>
<body>
<header id="top"><h1>♠ BIG TWO</h1><div id="topRight"><div class="money-panel"><span class="money-label">BALANCE</span><strong id="balance">💰500,000</strong></div><div class="active-settings"><span>STAKE <strong id="activeStake">💰10,000</strong></span><span>AI <strong id="activeAI">NORMAL</strong></span></div><button type="button" class="icon-toggle" id="musicToggle" aria-label="Turn casino background music on" title="Casino music">♫</button><button type="button" class="icon-toggle active" id="sfxToggle" aria-label="Turn card sound effects off" title="Card sound effects">🔊</button><button type="button" class="top-new-game" id="newBtn">NEW GAME</button><button type="button" class="top-new-game" id="resetBtn">RESET</button></div></header>
<main id="table">
 <div id="tableStatus">Your turn — you have 3♦.</div><div id="roundBalanceBoard"><button type="button" id="roundBalanceToggle" aria-expanded="false">LAST ROUND ▾</button><div id="roundBalanceRows">No completed round yet</div></div>
 <div class="seat" id="seat0"><div id="playerActionButtons"><button id="playSelectedBtn">PLAY SELECTED</button><button id="passBtn" class="secondary">PASS</button></div><div id="hint">Select your cards, then press a combination button to play.</div><strong><span>You</span><span class="seat-balance" id="seatBalance0">💰500,000</span></strong><span class="count" id="count0">13 cards</span></div>
 <div class="seat" id="seat1"><strong><span>West</span><span class="seat-balance" id="seatBalance1">💰500,000</span></strong><span class="count" id="count1">13 cards</span><div class="opponent-cards" id="opponentCards1" aria-label="West face-down cards"></div></div>
 <div class="seat" id="seat2"><strong><span>North</span><span class="seat-balance" id="seatBalance2">💰500,000</span></strong><span class="count" id="count2">13 cards</span><div class="opponent-cards" id="opponentCards2" aria-label="North face-down cards"></div></div>
 <div class="seat" id="seat3"><strong><span>East</span><span class="seat-balance" id="seatBalance3">💰500,000</span></strong><span class="count" id="count3">13 cards</span><div class="opponent-cards" id="opponentCards3" aria-label="East face-down cards"></div></div>
 <section id="center"><div id="trickLabel">CURRENT TRICK</div><div id="played"><span style="color:#d7e8d9">The player holding 3♦ leads the first trick.</span></div></section>
</main>
<section id="handArea"><div id="hand"></div><div id="controls"><div id="comboButtons" aria-label="Available combinations"></div></div></section>
<div id="overlay"><div id="dialog"><h2>BIG TWO</h2><p>Choose your per-card stake and AI difficulty, then press START GAME.<br><br>Beat the other three players and get rid of all your cards first.<br><br>Card order: 3 (low) to 2 (high). Suit order: ♦ ♣ ♥ ♠.<br>Default play is Single. Select the exact cards you want, then press PLAY SELECTED to play them.</p><div class="setup-fields"><div class="setup-field"><label for="stakeSelect">💰 STAKE / CARD</label><select id="stakeSelect" aria-label="Choose stake"><option value="1000">💰1,000</option><option value="2000">💰2,000</option><option value="5000">💰5,000</option><option value="10000" selected>💰10,000</option><option value="20000">💰20,000</option><option value="50000">💰50,000</option></select></div><div class="setup-field"><label for="aiLevel">🤖 AI LEVEL</label><select id="aiLevel" aria-label="AI difficulty"><option value="hard">Hard</option><option value="veryhard">Very Hard</option><option value="extremehard" selected>Extreme Hard</option></select></div></div><button id="startBtn" type="button">START GAME</button></div></div>
<script>
(()=>{'use strict';
const SUITS=['♦','♣','♥','♠'], RANKS=['3','4','5','6','7','8','9','10','J','Q','K','A','2'];
const suitValue=s=>SUITS.indexOf(s), rankValue=r=>RANKS.indexOf(r);
const cardKey=c=>rankValue(c.r)*4+suitValue(c.s);
const makeDeck=()=>SUITS.flatMap(s=>RANKS.map(r=>({s,r,id:r+s})));
const sortHand=h=>h.sort((a,b)=>cardKey(a)-cardKey(b));
let hands=[],turn=0,trick=null,passes=0,trickOwner=0,selected=new Set(),gameOver=false,firstMove=true;
let aiLevel='extremehard';
const INITIAL_BANKROLL=500000;
let playerBalances=(()=>{try{const saved=JSON.parse(localStorage.getItem('big2_player_balances')||'null');return Array.isArray(saved)&&saved.length===4&&saved.every(Number.isFinite)?saved:[INITIAL_BANKROLL,INITIAL_BANKROLL,INITIAL_BANKROLL,INITIAL_BANKROLL];}catch(e){return [INITIAL_BANKROLL,INITIAL_BANKROLL,INITIAL_BANKROLL,INITIAL_BANKROLL];}})();
let roundBalanceSummary=(()=>{try{return JSON.parse(localStorage.getItem('big2_round_balance_summary')||'null');}catch(e){return null;}})();
let roundBalanceHistory=(()=>{try{const h=JSON.parse(localStorage.getItem('big2_round_balance_history')||'[]');return Array.isArray(h)?h.slice(-6):[];}catch(e){return [];}})();
let roundBalanceExpanded=false;
let bankroll=playerBalances[0];
let selectedStake=10000,currentStake=10000,handStarted=false;
const money=n=>'💰'+Math.abs(n).toLocaleString('en-US');
function renderBalances(){
 bankroll=playerBalances[0];
 $('balance').textContent=(bankroll<0?'-':'')+money(bankroll);
 for(let i=0;i<4;i++){
  const el=$('seatBalance'+i);
  if(el)el.textContent=(playerBalances[i]<0?'-':'')+money(playerBalances[i]);
 }
 const rows=$('roundBalanceRows');
 if(rows){
  rows.innerHTML='';
  if(!roundBalanceHistory.length){
   rows.textContent='No completed rounds yet';
  }else{
   roundBalanceHistory.slice(-(roundBalanceExpanded?6:2)).reverse().forEach((round,index)=>{
    const block=document.createElement('div');block.className='round-history-entry';
    const heading=document.createElement('div');heading.className='round-history-title';
    heading.textContent='ROUND '+(roundBalanceHistory.length-(roundBalanceExpanded?0:0)-index);
    block.appendChild(heading);
    (round.players||[]).forEach(p=>{
     const row=document.createElement('div');row.className='round-balance-row';
     const name=document.createElement('span');name.className='rb-name';name.textContent=p.name;
     const change=document.createElement('span');change.className='rb-change '+(p.change>0?'positive':(p.change<0?'negative':''));
     change.textContent=(p.change<0?'-':(p.change>0?'+':''))+money(p.change);
     row.append(name,change);block.appendChild(row);
    });
    rows.appendChild(block);
   });
  }
 }
 try{
  localStorage.setItem('big2_bankroll',String(bankroll));
  localStorage.setItem('big2_player_balances',JSON.stringify(playerBalances));
  localStorage.setItem('big2_round_balance_summary',JSON.stringify(roundBalanceSummary));
  localStorage.setItem('big2_round_balance_history',JSON.stringify(roundBalanceHistory));
 }catch(e){}
}
function updateBalance(){renderBalances();}


function persistGameState(){
 try{
  const snapshot={
   version:7, bankroll, playerBalances, roundBalanceSummary, roundBalanceHistory, selectedStake, currentStake, aiLevel, handStarted, 
   hands, turn, trick, passes, trickOwner, gameOver, firstMove,
   selected:[...selected], musicEnabled, sfxEnabled,
   overlayMode:gameOver?'result':(handStarted?'playing':'setup'),
   resultHtml:gameOver?$('dialog').innerHTML:null
  };
  localStorage.setItem('big2_game_state',JSON.stringify(snapshot));
 }catch(e){}
}
function restoreGameState(){
 try{
  const raw=localStorage.getItem('big2_game_state');
  if(!raw)return false;
  const s=JSON.parse(raw);
  if(!s||![2,3,4,5,6,7].includes(s.version)||!Array.isArray(s.hands)||s.hands.length!==4)return false;
  bankroll=Number.isFinite(Number(s.bankroll))?Number(s.bankroll):INITIAL_BANKROLL;
  selectedStake=[1000,2000,5000,10000,20000,50000].includes(Number(s.selectedStake))?Number(s.selectedStake):10000;currentStake=[1000,2000,5000,10000,20000,50000].includes(Number(s.currentStake))?Number(s.currentStake):selectedStake;
  aiLevel=['hard','veryhard','extremehard'].includes(s.aiLevel)?s.aiLevel:'extremehard';
  handStarted=!!s.handStarted;hands=s.hands;turn=Number(s.turn)||0;trick=s.trick||null;
  passes=Number(s.passes)||0;trickOwner=Number(s.trickOwner)||0;
  gameOver=!!s.gameOver;firstMove=!!s.firstMove;selected=new Set(Array.isArray(s.selected)?s.selected:[]);
  musicEnabled=!!s.musicEnabled;sfxEnabled=s.sfxEnabled!==false;
  updateBalance();
  $('activeStake').textContent=money(handStarted?currentStake:selectedStake);
  $('activeAI').textContent=({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||aiLevel.toUpperCase()));
  $('musicToggle').classList.toggle('active',musicEnabled);
  $('musicToggle').textContent=musicEnabled?'♫':'♪';
  $('sfxToggle').classList.toggle('active',sfxEnabled);
  $('sfxToggle').textContent=sfxEnabled?'🔊':'🔇';
  if(gameOver&&s.resultHtml){$('dialog').innerHTML=s.resultHtml;$('overlay').hidden=false;}
  else if(handStarted){$('overlay').hidden=true;}
  else{$('overlay').hidden=false;}
  return true;
 }catch(e){return false;}
}

function multiplierForCards(count){
 if(count>=13)return 4;
 if(count>=10)return 3;
 if(count>=8)return 2;
 return 1;
}
function fineForCards(count){return count*currentStake*multiplierForCards(count);}


const $=id=>document.getElementById(id);
$('roundBalanceToggle').addEventListener('click',()=>{
 roundBalanceExpanded=!roundBalanceExpanded;
 const btn=$('roundBalanceToggle');
 btn.textContent=roundBalanceExpanded?'LAST 6 ROUNDS ▴':'LAST 2 ROUNDS ▾';
 btn.setAttribute('aria-expanded',String(roundBalanceExpanded));
 renderBalances();
});
let audioCtx=null,musicEnabled=false,sfxEnabled=true,musicTimer=null,musicStep=0;
function getAudio(){
 if(!audioCtx){const AC=window.AudioContext||window.webkitAudioContext;if(AC)audioCtx=new AC();}
 if(audioCtx&&audioCtx.state==='suspended')audioCtx.resume();
 return audioCtx;
}
function audioTone(freq,duration,wave='sine',volume=.05,delay=0){
 const ctx=getAudio();if(!ctx)return;
 const osc=ctx.createOscillator(),gain=ctx.createGain(),now=ctx.currentTime+delay;
 osc.type=wave;osc.frequency.setValueAtTime(freq,now);
 gain.gain.setValueAtTime(.0001,now);gain.gain.exponentialRampToValueAtTime(volume,now+.012);
 gain.gain.exponentialRampToValueAtTime(.0001,now+duration);
 osc.connect(gain);gain.connect(ctx.destination);osc.start(now);osc.stop(now+duration+.025);
}
function playCardSound(){
 if(!sfxEnabled)return;
 audioTone(620,.055,'triangle',.055);
 audioTone(880,.07,'sine',.035,.035);
}
function startCasinoMusic(){
 if(musicTimer)return;
 const notes=[392,523.25,659.25,587.33,523.25,440,493.88,587.33,
              440,554.37,659.25,783.99,659.25,587.33,523.25,493.88];
 musicStep=0;
 musicTimer=setInterval(()=>{
  if(!musicEnabled||!audioCtx||audioCtx.state!=='running')return;
  const n=notes[musicStep%notes.length];
  audioTone(n,.34,'triangle',.018);
  if(musicStep%4===0)audioTone(n/2,.48,'sine',.025);
  if(musicStep%2===0)audioTone(1046.5,.035,'sine',.012,.08);
  musicStep++;
 },360);
}
function stopCasinoMusic(){
 if(musicTimer){clearInterval(musicTimer);musicTimer=null;}
}
function setMusicEnabled(enabled){
 musicEnabled=enabled;
 const btn=$('musicToggle');btn.classList.toggle('active',enabled);
 btn.textContent=enabled?'♫':'♪';
 btn.setAttribute('aria-label',enabled?'Turn casino background music off':'Turn casino background music on');
 btn.title=enabled?'Turn casino music off':'Turn casino music on';
 persistGameState();
 if(enabled){getAudio();startCasinoMusic();}else stopCasinoMusic();
}
function setSfxEnabled(enabled){
 sfxEnabled=enabled;
 const btn=$('sfxToggle');btn.classList.toggle('active',enabled);
 btn.textContent=enabled?'🔊':'🔇';
 btn.setAttribute('aria-label',enabled?'Turn card sound effects off':'Turn card sound effects on');
 btn.title=enabled?'Turn card sound effects off':'Turn card sound effects on';
 persistGameState();
}

function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function combos(arr,n,start=0,prefix=[],out=[]){if(prefix.length===n){out.push(prefix.slice());return out;}for(let i=start;i<=arr.length-(n-prefix.length);i++){prefix.push(arr[i]);combos(arr,n,i+1,prefix,out);prefix.pop();}return out;}
function straightHigh(cards){
 const vals=[...new Set(cards.map(c=>rankValue(c.r)))].sort((a,b)=>a-b);
 if(vals.length!==5)return -1;
 // A-2-3-4-5 is the lowest special straight; 10-J-Q-K-A is high.
 if(vals.join(',')==='0,1,2,11,12')return 3;
 if(vals[4]-vals[0]===4)return vals[4]+3;
 return -1;
}
function evaluate(cards){
 if(![1,2,3,5].includes(cards.length))return null;
 const sorted=cards.slice().sort((a,b)=>cardKey(a)-cardKey(b));
 const rv=sorted.map(c=>rankValue(c.r)), sv=sorted.map(c=>suitValue(c.s));
 if(cards.length===1)return {n:1,cat:0,high:cardKey(sorted[0]),label:'Single'};
 if(cards.length===2&&rv[0]===rv[1])return {n:2,cat:1,high:Math.max(...sorted.map(cardKey)),label:'Pair'};
 if(cards.length===3&&rv.every(v=>v===rv[0]))return {n:3,cat:2,high:Math.max(...sorted.map(cardKey)),label:'Triple'};
 if(cards.length!==5)return null;
 const counts={};rv.forEach(v=>counts[v]=(counts[v]||0)+1);
 const flush=sv.every(v=>v===sv[0]), sh=straightHigh(sorted), groups=Object.entries(counts).sort((a,b)=>b[1]-a[1]||Number(b[0])-Number(a[0]));
 let cat=-1,high=0,label='';
 if(flush&&sh>=0){cat=8;high=sh*4+Math.max(...sv);label='Straight flush';}
 else if(groups[0][1]===4){cat=7;high=Number(groups[0][0])*4+Math.max(...sv);label='Four of a kind';}
 else if(groups[0][1]===3&&groups[1][1]===2){cat=6;high=Number(groups[0][0])*4+Math.max(...sv);label='Full house';}
 else if(flush){cat=5;high=Math.max(...rv);label='Flush';}
 else if(sh>=0){cat=4;high=sh*4+Math.max(...sv);label='Straight';}
 else return null;
 return {n:5,cat,high,label,...(cat===5?{tieBreak:sorted.slice().sort((a,b)=>rankValue(b.r)-rankValue(a.r)||suitValue(b.s)-suitValue(a.s)).map(c=>[rankValue(c.r),suitValue(c.s)])}:{})};
}
function beats(a,b){if(!b)return true;if(a.n!==b.n)return false;if(a.n===5){if(a.cat!==b.cat)return a.cat>b.cat;if(a.cat===5){for(let i=0;i<5;i++){const ar=a.tieBreak?.[i]||[0,0],br=b.tieBreak?.[i]||[0,0];if(ar[0]!==br[0])return ar[0]>br[0];if(ar[1]!==br[1])return ar[1]>br[1];}return false;}return a.high>b.high;}return a.high>b.high;}
function showCard(c,extra=''){const el=document.createElement('div');el.className='card '+(['♦','♥'].includes(c.s)?'red ':'')+extra;el.innerHTML='<span class="rank">'+c.r+'</span><span class="suit">'+c.s+'</span><span class="rank" style="transform:rotate(180deg)">'+c.r+'</span>';return el;}


const COMBO_TYPES=[
 {label:'Single',n:1},
 {label:'Pair',n:2},
 {label:'Triple',n:3},
 {label:'Straight',n:5,cat:4},
 {label:'Flush',n:5,cat:5},
 {label:'Full House',n:5,cat:6},
 {label:'Four of a Kind',n:5,cat:7},
 {label:'Straight Flush',n:5,cat:8}
];
function combinationsOf(hand,size){
 const out=[];
 function walk(start,picked){
  if(picked.length===size){out.push(picked.slice());return;}
  for(let i=start;i<=hand.length-(size-picked.length);i++){
   picked.push(hand[i]);walk(i+1,picked);picked.pop();
  }
 }
 walk(0,[]);return out;
}
function legalCombo(cards){
 const combo=evaluate(cards);
 return !!combo&&(!firstMove||cards.some(c=>c.id==='3♦'))&&(!trick||beats(combo,trick.combo));
}
function availableCombos(type){
 const candidates=combinationsOf(hands[0],type.n).filter(cards=>{
  const e=evaluate(cards);
  return e&& (type.n!==5||e.cat===type.cat) && legalCombo(cards);
 });
 candidates.sort((a,b)=>{
  const ea=evaluate(a),eb=evaluate(b);
  if(ea.cat!==eb.cat)return ea.cat-eb.cat;
  if(ea.cat===5){for(let i=0;i<5;i++){const av=ea.tieBreak[i],bv=eb.tieBreak[i];if(av[0]!==bv[0])return av[0]-bv[0];if(av[1]!==bv[1])return av[1]-bv[1];}}
  return ea.high-eb.high||Math.min(...a.map(cardKey))-Math.min(...b.map(cardKey));
 });
 return candidates;
}

function renderComboButtons(){
 const box=$('comboButtons');if(!box)return;box.innerHTML='';
 COMBO_TYPES.forEach(type=>{
  const candidates=availableCombos(type);
  if(type.label!=='Single'&&!candidates.length)return;
  const btn=document.createElement('button');
  btn.type='button';
  btn.className='combo-btn';
  btn.textContent=type.label;
  btn.disabled=!candidates.length||turn!==0||gameOver;
  btn.title=candidates.length?type.label+' available ('+candidates.length+')':'No legal combination';
  btn.setAttribute('aria-label',btn.title);
  btn.addEventListener('click',()=>{
   if(turn!==0||gameOver||!candidates.length)return;
   // Select a valid combination only; the player still decides whether to play it.
   const chosen=candidates[0];
   selected.clear();
   chosen.forEach(card=>selected.add(card.id));
   render();
   $('hint').textContent='Selected '+type.label+'. Press PLAY SELECTED when you are ready.';
  });
  box.appendChild(btn);
 });
}
function render(){
 const hand=$('hand');hand.innerHTML='';
 sortHand(hands[0]);hands[0].forEach(c=>{const el=showCard(c,'hand-card'+(selected.has(c.id)?' selected':''));el.title=c.id;el.addEventListener('click',()=>{if(turn!==0||gameOver)return;if(selected.has(c.id))selected.delete(c.id);else selected.add(c.id);render();scheduleAutoPlay();});hand.appendChild(el);});
 for(let i=0;i<4;i++){
  $('count'+i).textContent=hands[i].length+' cards';
  $('seat'+i).classList.toggle('one-card-alert',hands[i].length===1);
 }
 $('hand').classList.toggle('one-card-alert',hands[0].length===1);
  for(let i=1;i<4;i++){
   const display=$('opponentCards'+i);display.innerHTML='';
   for(let n=0;n<hands[i].length;n++){
    const back=document.createElement('span');
    back.className='opponent-card';
    back.setAttribute('aria-hidden','true');
    display.appendChild(back);
   }
  }
 $('seat0').style.opacity=turn===0?'1':'.65';
 for(let i=1;i<4;i++)$('seat'+i).style.opacity=turn===i?'1':'.65';
 $('passBtn').disabled=turn!==0||gameOver||!trick||trickOwner===0;
 $('playSelectedBtn').disabled=turn!==0||gameOver||selected.size===0;
 renderComboButtons();persistGameState();
}
let autoPlayTimer=null;
function scheduleAutoPlay(){
 if(autoPlayTimer){clearTimeout(autoPlayTimer);autoPlayTimer=null;}
 const cards=hands[0].filter(c=>selected.has(c.id));
 const count=cards.length;
 if(!count){$('hint').textContent='Default: Single. Select your card(s), then press the matching combination button to play.';return;}
 const combo=evaluate(cards);
 if(!combo){
  $('hint').textContent=count===4?'Four cards selected — add one card for a five-card hand.':'Invalid combination. Select a valid Single, Pair, Triple or five-card hand.';
  return;
 }
 if(firstMove&&!cards.some(c=>c.id==='3♦')){
  $('hint').textContent='Opening play must include 3♦. Detected: '+combo.label+'.';return;
 }
 if(trick&&!beats(combo,trick.combo)){
  $('hint').textContent='Detected '+combo.label+', but it does not beat the current play.';return;
 }
 $('hint').textContent='Detected '+combo.label+'. Press PLAY SELECTED when you are ready.';
}

function setStatus(t){$('tableStatus').textContent=t;persistGameState();}
function renderTrick(cards,label){const box=$('played');box.innerHTML='';if(!cards||!cards.length){box.innerHTML='';return;}cards.forEach(c=>box.appendChild(showCard(c)));$('trickLabel').textContent=label||'CURRENT TRICK';}
function startGame(){
 handStarted=true;
 $('stakeSelect').disabled=true;$('aiLevel').disabled=true;
 currentStake=selectedStake;
 $('activeStake').textContent=money(currentStake); $('activeAI').textContent=({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||aiLevel.toUpperCase()));
 const deck=shuffle(makeDeck());hands=[deck.slice(0,13),deck.slice(13,26),deck.slice(26,39),deck.slice(39,52)].map(sortHand);
 turn=hands.findIndex(h=>h.some(c=>c.id==='3♦'));trick=null;passes=0;trickOwner=turn;selected.clear();gameOver=false;firstMove=true;
 $('overlay').hidden=true;renderTrick(null);setStatus(turn===0?'Your turn — you have 3♦.':'Waiting for the opening lead…');render();persistGameState();if(turn!==0)setTimeout(aiTurn,650);
}
function playCards(player,cards){
 if(player===0&&autoPlayTimer){clearTimeout(autoPlayTimer);autoPlayTimer=null;}
 playCardSound();
 const combo=evaluate(cards);if(!combo)return false;
 if(firstMove&&player===turn&&!cards.some(c=>c.id==='3♦'))return false;
 if(trick&&!beats(combo,trick.combo))return false;
 const ids=new Set(cards.map(c=>c.id));hands[player]=hands[player].filter(c=>!ids.has(c.id));
 trick={cards:cards.slice(),combo,player};trickOwner=player;passes=0;firstMove=false;
 renderTrick(cards,combo.label.toUpperCase()+' — '+['You','West','North','East'][player]);
 if(hands[player].length===0){finish(player);return true;}
 turn=(player+1)%4;render();setStatus(player===0?'You played '+combo.label+'.':'A player has played.');return true;
}
function pass(player){
 if(!trick||player===trickOwner)return false;
 passes++;turn=(player+1)%4;
 if(passes>=3){turn=trickOwner;trick=null;passes=0;renderTrick(null,'NEW TRICK');setStatus(['You','West','North','East'][turn]+' leads the next trick.');}
 else setStatus(['You','West','North','East'][player]+' passed.');
 render();return true;
}
function finish(winner){
 gameOver=true;render();
 const names=['You','West','North','East'],name=names[winner];
 const changes=[0,0,0,0],payments=[];
 for(let i=0;i<4;i++){
  if(i===winner)continue;
  const count=hands[i].length,mult=multiplierForCards(count),amount=fineForCards(count);
  changes[i]-=amount;changes[winner]+=amount;
  payments.push(names[i]+': '+count+' cards × '+money(currentStake)+' / card ×'+mult+' = '+money(amount));
 }
 for(let i=0;i<4;i++)playerBalances[i]+=changes[i];
 bankroll=playerBalances[0];
 roundBalanceSummary={winner:name,players:names.map((n,i)=>({name:n,change:changes[i],balance:playerBalances[i]}))};
 roundBalanceHistory.push({winner:name,players:names.map((n,i)=>({name:n,change:changes[i]}))});roundBalanceHistory=roundBalanceHistory.slice(-6);
 updateBalance();
 let change=changes[0],detail='Winner: '+name+'.<br>'+payments.join('<br>');
 setStatus(name+' wins! '+(change>=0?'+':'-')+money(change));
 const result=change>=0?'YOU WIN!':'GAME OVER';
 const signed=(change>=0?'+':'-')+money(change);
 $('dialog').innerHTML='<h2>'+result+'</h2><p><strong>'+signed+'</strong><br>Stake per card: '+money(currentStake)+'<br>Balance: '+money(bankroll)+'</p><p style="font-size:13px;line-height:1.65">'+detail+'</p><button id="againBtn">PLAY AGAIN</button>';
 $('overlay').hidden=false;
 $('againBtn').textContent='NEW GAME';
 persistGameState();
}
// Delegated handler: the result dialog is rebuilt dynamically after every hand.
$('overlay').addEventListener('click',function(event){
 const again=event.target.closest('#againBtn');
 if(again){
  event.preventDefault();
  event.stopPropagation();
  showSetupPopup();
 }
});

function handleStartGame(event){
 if(event){event.preventDefault();event.stopPropagation();}
 const button=$('startBtn');
 if(!button||button.disabled)return;
 if(button.dataset.starting==='1')return;
 button.dataset.starting='1';button.disabled=true;
 try{
  const stakeEl=$('stakeSelect'),aiEl=$('aiLevel');
  if(!stakeEl||!aiEl)throw new Error('Game settings are missing. Please reopen the setup window.');
  const stake=Number(stakeEl.value);
  if(![1000,2000,5000,10000,20000,50000].includes(stake))throw new Error('Please choose a valid stake.');
  if(!['hard','veryhard','extremehard'].includes(aiEl.value))throw new Error('Please choose a valid AI level.');
  selectedStake=stake;aiLevel=aiEl.value;
  startGame();
 }catch(err){
  button.dataset.starting='0';button.disabled=false;
  const p=$('dialog')?.querySelector('p');
  if(p)p.textContent='Unable to start: '+(err&&err.message?err.message:'Please try again.');
  console.error('Big Two START GAME failed:',err);
 }
}

function showSetupPopup(){
 handStarted=false;
 $('overlay').innerHTML='<div id="dialog"><h2>BIG TWO</h2><p>Choose your per-card stake and AI difficulty, then press START GAME.</p><div class="setup-fields"><div class="setup-field"><label for="stakeSelect">💰 STAKE / CARD</label><select id="stakeSelect" aria-label="Choose stake"><option value="1000">💰1,000</option><option value="2000">💰2,000</option><option value="5000">💰5,000</option><option value="10000" selected>💰10,000</option><option value="20000">💰20,000</option><option value="50000">💰50,000</option></select></div><div class="setup-field"><label for="aiLevel">🤖 AI LEVEL</label><select id="aiLevel" aria-label="AI difficulty"><option value="hard" selected>Hard</option><option value="veryhard">Very Hard</option><option value="extremehard">Extreme Hard</option></select></div></div><button id="startBtn" type="button">START GAME</button></div>';
 $('stakeSelect').value=String(selectedStake);
 $('aiLevel').value=aiLevel;
 $('stakeSelect').onchange=e=>{selectedStake=Number(e.target.value);$('activeStake').textContent=money(selectedStake);persistGameState();};
 $('aiLevel').onchange=e=>{aiLevel=e.target.value;$('activeAI').textContent=({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||aiLevel.toUpperCase()));persistGameState();};
 $('activeStake').textContent=money(selectedStake);
 $('activeAI').textContent=({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||aiLevel.toUpperCase()));
 $('overlay').hidden=false;
 $('startBtn').disabled=false;$('startBtn').dataset.starting='0';$('startBtn').onclick=handleStartGame;
 persistGameState();
}


function chooseAI(player){
 const hand=hands[player],level=aiLevel;
 let candidates=[];
 const sizes=trick?[trick.combo.n]:[1,2,3,5];
 sizes.forEach(n=>combos(hand,n).forEach(cs=>{
  const e=evaluate(cs);
  if(e&&(!trick||beats(e,trick.combo))&&(!firstMove||cs.some(c=>c.id==='3♦')))
   candidates.push({cs,e});
 }));
 if(!candidates.length)return null;

 // Estimate how efficiently the remaining hand can be partitioned into
 // singles, pairs, triples and five-card poker hands.
 function planCost(cards){
  const n=cards.length;
  if(!n)return 0;
  const valid=[];
  for(const size of [1,2,3,5]){
   if(size>n)continue;
   for(const group of combos(cards,size)){
    const e=evaluate(group);
    if(e)valid.push({mask:group.reduce((m,c)=>m|(1<<cards.indexOf(c)),0),size,e,group});
   }
  }
  const byFirst=Array.from({length:n},()=>[]);
  valid.forEach(g=>{for(let i=0;i<n;i++)if(g.mask&(1<<i)){byFirst[i].push(g);break;}});
  const full=(1<<n)-1,memo=new Map();
  function solve(mask){
   if(mask===full)return {turns:0,cost:0};
   if(memo.has(mask))return memo.get(mask);
   let first=0;while(mask&(1<<first))first++;
   let best={turns:99,cost:Infinity};
   for(const g of byFirst[first]){
    if((g.mask&mask)!==0)continue;
    const rest=solve(mask|g.mask);
    const high=g.group.reduce((s,c)=>s+cardKey(c),0)/g.size;
    // Fewer future plays dominate; among equal plans, preserve high cards
    // and prefer naturally strong multi-card combinations.
    const groupCost=(g.size===1?0.34:0)+(g.size===5?Math.max(0,5-g.e.cat)*0.035:0)+high*0.006;
    const candidate={turns:rest.turns+1,cost:rest.cost+groupCost};
    if(candidate.turns<best.turns||(candidate.turns===best.turns&&candidate.cost<best.cost))best=candidate;
   }
   memo.set(mask,best);return best;
  }
  const p=solve(0);
  return p.turns*100+p.cost;
 }
 const remainingPlan=cs=>{
  const used=new Set(cs.map(c=>c.id));
  return planCost(hand.filter(c=>!used.has(c.id)));
 };
 const cardStrength=cs=>cs.reduce((s,c)=>s+cardKey(c),0)/cs.length;
 const urgency=()=>{
  let u=0;
  for(let step=1;step<=3;step++){
   const count=hands[(player+step)%4].length;
   if(count<=2)u+=7;
   else if(count<=4)u+=4;
   else if(count<=6)u+=1.5;
  }
  return u;
 };
 const score=c=>{
  if(c.cs.length===hand.length)return -100000;
  const plan=remainingPlan(c.cs),strength=cardStrength(c.cs);
  const cat=c.e.cat||0,n=c.e.n;
  let s=plan*10;
  // Prefer shedding useful groups when doing so materially improves the
  // remaining hand plan; avoid mechanically leading high singles.
  if(!trick){
   if(n===1)s+=2.8+strength*0.12;
   if(n===2)s+=0.8+strength*0.035;
   if(n===3)s+=0.25+strength*0.02;
   if(n===5)s+=Math.max(0,5-cat)*0.16+strength*0.012;
   if(level==='veryhard')s-=({1:0,2:1.2,3:1.8,5:2.1}[n]||0);
   if(level==='extremehard')s-=({1:0,2:2.0,3:2.8,5:3.2}[n]||0);
  }else{
   const over=(cat*100+c.e.high)-(trick.combo.cat*100+trick.combo.high);
   // Use the cheapest sufficient winning combination, but take control
   // decisively when an opponent is close to finishing.
   s+=Math.max(0,over)*0.008+strength*0.018;
   if(n===1)s+=0.7;
   if(level==='veryhard')s-=Math.min(3,urgency()*0.22);
   if(level==='extremehard')s-=Math.min(6,urgency()*0.42);
   if(level==='extremehard'&&over>35&&urgency()<3)s+=1.2;
  }
  // Preserve valuable high cards as controls unless the hand plan improves.
  const highCards=c.cs.filter(x=>cardKey(x)>=cardKey({r:'A',s:'♠'})).length;
  s+=highCards*(level==='extremehard'?0.55:(level==='veryhard'?0.32:0.12));
  // Small deterministic-looking variation without fixed largest-to-smallest play.
  if(level==='veryhard')s+=Math.sin(c.cs.reduce((v,x)=>v+cardKey(x),0))*0.12;
  if(level==='extremehard')s+=Math.cos(c.cs.reduce((v,x)=>v+cardKey(x)*3,0))*0.18;
  return s;
 };
 candidates.sort((a,b)=>score(a)-score(b));
 const best=score(candidates[0]);
 const tolerance=level==='extremehard'?0.08:(level==='veryhard'?0.14:0.25);
 const near=candidates.filter(c=>score(c)<=best+tolerance);
 return near[Math.floor(Math.random()*near.length)];
}
function aiTurn(){
 if(gameOver||turn===0)return;
 const player=turn,choice=chooseAI(player);
 if(choice){playCards(player,choice.cs);if(!gameOver&&turn!==0)setTimeout(aiTurn,550);}
 else{pass(player);if(!gameOver&&turn!==0)setTimeout(aiTurn,550);}
}
$('playSelectedBtn').onclick=()=>{
 if(turn!==0||gameOver)return;
 const cards=hands[0].filter(c=>selected.has(c.id));
 const combo=evaluate(cards);
 if(!combo){$('hint').textContent='Please select a valid Single, Pair, Triple or five-card combination.';return;}
 if(firstMove&&!cards.some(c=>c.id==='3♦')){$('hint').textContent='Your opening play must include 3♦.';return;}
 if(trick&&!beats(combo,trick.combo)){$('hint').textContent='That '+combo.label+' cannot beat the current play.';return;}
 selected.clear();
 if(playCards(0,cards)&&!gameOver&&turn!==0)setTimeout(aiTurn,500);
 render();
};
$('passBtn').onclick=()=>{if(autoPlayTimer)clearTimeout(autoPlayTimer);selected.clear();if(pass(0)&&turn!==0)setTimeout(aiTurn,500);render();};
$('aiLevel').value=aiLevel;
$('aiLevel').addEventListener('change',e=>{if(!handStarted){aiLevel=e.target.value;$('activeAI').textContent=({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||aiLevel.toUpperCase()));persistGameState();}else e.target.value=aiLevel;});
$('stakeSelect').value=String(selectedStake);
$('stakeSelect').addEventListener('change',e=>{if(!handStarted){selectedStake=Number(e.target.value);$('activeStake').textContent=money(selectedStake);persistGameState();}else e.target.value=String(currentStake);});
$('resetBtn').addEventListener('click',()=>{
 if(!confirm('Reset all four balances to 💰500,000 and start a new game?'))return;
 playerBalances=[INITIAL_BANKROLL,INITIAL_BANKROLL,INITIAL_BANKROLL,INITIAL_BANKROLL];
 bankroll=INITIAL_BANKROLL;roundBalanceSummary=null;roundBalanceHistory=[];gameOver=false;handStarted=false;
 try{localStorage.removeItem('big2_game_state');localStorage.removeItem('big2_bankroll');localStorage.removeItem('big2_player_balances');localStorage.removeItem('big2_round_balance_summary');localStorage.removeItem('big2_round_balance_history');}catch(e){}
 updateBalance();showSetupPopup();setStatus('Balances reset to 💰500,000. Choose your per-card stake and AI difficulty, then press START GAME.');
});
$('newBtn').addEventListener('click',()=>{
 showSetupPopup();
 setStatus('Choose your per-card stake and AI difficulty, then press START GAME.');
});
$('musicToggle').onclick=()=>setMusicEnabled(!musicEnabled);
$('sfxToggle').onclick=()=>setSfxEnabled(!sfxEnabled);
$('startBtn').onclick=null;
$('hand').addEventListener('contextmenu',e=>e.preventDefault());
const initialStartButton=$('startBtn');if(initialStartButton)initialStartButton.onclick=handleStartGame;
const restored=restoreGameState();

if(restored){
 renderBalances();
 $('stakeSelect').value=String(selectedStake);$('aiLevel').value=aiLevel;
 $('activeStake').textContent=money(handStarted?currentStake:selectedStake);
 $('activeAI').textContent=({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||aiLevel.toUpperCase()));
 if(gameOver){
  $('overlay').hidden=false;
 }else if(handStarted){
  $('overlay').hidden=true;
  renderTrick(trick?trick.cards:null,trick?trick.combo.label.toUpperCase()+' — '+['You','West','North','East'][trick.player]:'CURRENT TRICK');
  render();
  if(turn===0&&selected.size)scheduleAutoPlay();
  if(turn!==0)setTimeout(aiTurn,650);
 }else{
  $('overlay').hidden=false;
 }
}else{
 updateBalance();
 $('activeStake').textContent=money(selectedStake);
 $('activeAI').textContent=({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||({hard:'HARD',veryhard:'VERY HARD',extremehard:'EXTREME HARD'}[aiLevel]||aiLevel.toUpperCase()));
 persistGameState();
}
setMusicEnabled(musicEnabled);
setSfxEnabled(sfxEnabled);
})();
</script>
</body></html>"""

@big2_bp.get("/")
def play_big2():
    return Response(GAME_HTML, mimetype="text/html; charset=utf-8")
