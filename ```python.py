```python
import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(
    page_title="Binary Flappy Bird",
    page_icon="🐤",
    layout="centered"
)

st.title("🐤 Binary Flappy Bird")
st.write("Follow the map by converting the word into binary!")

# -----------------------------
# Generate a random word
# -----------------------------

words = [
    "CAT",
    "DOG",
    "BIRD",
    "CODE",
    "BYTE",
    "ROBOT",
    "MATH",
    "SPACE",
    "LIGHT",
    "COMPUTER"
]

if "word" not in st.session_state:
    st.session_state.word = random.choice(words)

if st.button("New Word"):
    st.session_state.word = random.choice(words)
    st.rerun()

word = st.session_state.word

st.subheader(f"Word: **{word}**")

# -----------------------------
# Convert word to binary
# -----------------------------

binary = ""

for letter in word:
    binary += format(ord(letter), "08b")

# The binary is NOT shown to the player.
# It is sent to the game instead.

game = f"""
<!DOCTYPE html>
<html>

<head>

<style>

#game {{
    width: 700px;
    max-width: 100%;
    height: 450px;

    position: relative;
    overflow: hidden;

    background: #87CEEB;

    border: 4px solid #222;
    border-radius: 12px;

    font-family: Arial, sans-serif;
}}

#bird {{
    position: absolute;

    width: 30px;
    height: 30px;

    left: 100px;
    top: 200px;

    background: #FFD700;

    border-radius: 50%;

    z-index: 5;
}}

#bird::after {{
    content: "";

    position: absolute;

    right: -10px;
    top: 9px;

    border-top: 6px solid transparent;
    border-bottom: 6px solid transparent;
    border-left: 12px solid orange;
}}

.pipe {{
    position: absolute;

    width: 60px;

    background: #35a853;

    border: 3px solid #176b2e;
}}

#score {{
    position: absolute;

    left: 15px;
    top: 10px;

    color: white;

    font-size: 24px;
    font-weight: bold;

    text-shadow: 2px 2px #333;

    z-index: 10;
}}

#bit {{
    position: absolute;

    right: 15px;
    top: 10px;

    color: white;

    font-size: 22px;
    font-weight: bold;

    text-shadow: 2px 2px #333;

    z-index: 10;
}}

#message {{
    position: absolute;

    width: 100%;

    top: 160px;

    text-align: center;

    color: white;

    font-size: 30px;
    font-weight: bold;

    text-shadow: 2px 2px #333;

    z-index: 20;
}}

#answer {{
    position: absolute;

    left: 50%;
    transform: translateX(-50%);

    bottom: 20px;

    width: 70px;
    height: 45px;

    font-size: 28px;

    text-align: center;

    border: 3px solid #222;
    border-radius: 8px;

    z-index: 30;
}}

#progress {{
    position: absolute;

    left: 15px;
    bottom: 15px;

    color: white;

    font-size: 16px;

    text-shadow: 2px 2px #333;

    z-index: 10;
}}

</style>

</head>

<body>

<div id="game">

    <div id="bird"></div>

    <div id="score">
        Score: 0
    </div>

    <div id="bit">
        Ready
    </div>

    <div id="message">
        Get Ready!
    </div>

    <input
        id="answer"
        type="text"
        maxlength="1"
        inputmode="numeric"
        autocomplete="off"
        autofocus
    >

    <div id="progress">
        0 / {len(binary)}
    </div>

</div>


<script>

const binary = "{binary}";

const bird = document.getElementById("bird");
const answer = document.getElementById("answer");

const bitDisplay = document.getElementById("bit");
const message = document.getElementById("message");

const scoreDisplay = document.getElementById("score");
const progressDisplay = document.getElementById("progress");


/* -----------------------------
   GAME SETTINGS
----------------------------- */

const GAME_WIDTH = 700;
const GAME_HEIGHT = 450;

const BIRD_X = 100;

const GRAVITY = 0.18;
const JUMP_POWER = -5;

const PIPE_SPEED = 1.2;

const GAP_HEIGHT = 170;

const SECTION_WIDTH = 180;


/* -----------------------------
   GAME VARIABLES
----------------------------- */

let birdY = 210;
let velocity = 0;

let currentBit = 0;

let score = 0;

let pipes = [];

let gameStarted = false;
let gameEnded = false;


/* -----------------------------
   CREATE THE MAP
----------------------------- */

function createMap() {{

    pipes = [];

    for (let i = 0; i < binary.length; i++) {{

        const bit = binary[i];

        /*
        Each binary digit creates one
        section of the level.

        1 = higher path
        0 = lower path
        */

        let gapCenter;

        if (bit === "1") {{

            gapCenter = 150;

        }} else {{

            gapCenter = 300;

        }}

        const gapTop =
            gapCenter - GAP_HEIGHT / 2;

        const gapBottom =
            gapCenter + GAP_HEIGHT / 2;

        pipes.push({{

            x:
                500 + i * SECTION_WIDTH,

            gapTop: gapTop,

            gapBottom: gapBottom,

            passed: false
        }});
    }}
}


/* -----------------------------
   JUMP
----------------------------- */

function jump() {{

    velocity = JUMP_POWER;

}}


/* -----------------------------
   SHOW CURRENT BIT
----------------------------- */

function showBit() {{

    if (currentBit >= binary.length) {{

        finishGame();

        return;
    }}

    bitDisplay.innerText =
        "TYPE: " + binary[currentBit];

    progressDisplay.innerText =
        currentBit + " / " + binary.length;

    answer.value = "";

    answer.focus();
}}


/* -----------------------------
   PLAYER INPUT
----------------------------- */

answer.addEventListener("input", function() {{

    if (!gameStarted || gameEnded) {{
        return;
    }}

    const input = answer.value;

    if (input !== "0" && input !== "1") {{

        answer.value = "";

        return;
    }}

    const correctBit =
        binary[currentBit];


    /*
    The player entered the
    correct binary digit.
    */

    if (input === correctBit) {{

        /*
        If the binary is 1,
        the bird jumps.
        */

        if (input === "1") {{

            jump();

        }}

        currentBit++;

        showBit();

    }} else {{

        /*
        Wrong answer.
        The player stays on
        the same section.
        */

        message.innerText = "WRONG!";

        answer.value = "";

        setTimeout(() => {{

            if (!gameEnded) {{

                message.innerText = "";

            }}

        }}, 500);
    }}

}});


/* -----------------------------
   DRAW PIPES
----------------------------- */

function drawPipes() {{

    document
        .querySelectorAll(".pipe")
        .forEach(pipe => pipe.remove());


    pipes.forEach(pipe => {{

        /*
        Only draw pipes that are
        visible.
        */

        if (
            pipe.x < GAME_WIDTH &&
            pipe.x > -100
        ) {{

            // Top pipe

            const topPipe =
                document.createElement("div");

            topPipe.className = "pipe";

            topPipe.style.left =
                pipe.x + "px";

            topPipe.style.top =
                "0px";

            topPipe.style.height =
                pipe.gapTop + "px";


            // Bottom pipe

            const bottomPipe =
                document.createElement("div");

            bottomPipe.className = "pipe";

            bottomPipe.style.left =
                pipe.x + "px";

            bottomPipe.style.top =
                pipe.gapBottom + "px";

            bottomPipe.style.height =
                (GAME_HEIGHT - pipe.gapBottom)
                + "px";


            document
                .getElementById("game")
                .appendChild(topPipe);

            document
                .getElementById("game")
                .appendChild(bottomPipe);
        }}
    }});
}}


/* -----------------------------
   COLLISION
----------------------------- */

function checkCollision(pipe) {{

    const birdLeft = BIRD_X;

    const birdRight =
        BIRD_X + 30;

    const birdTop =
        birdY;

    const birdBottom =
        birdY + 30;


    const pipeLeft =
        pipe.x;

    const pipeRight =
        pipe.x + 60;


    const horizontalCollision =
        birdRight > pipeLeft &&
        birdLeft < pipeRight;


    const verticalCollision =
        birdTop < pipe.gapTop ||
        birdBottom > pipe.gapBottom;


    return (
        horizontalCollision &&
        verticalCollision
    );
}}


/* -----------------------------
   END GAME
----------------------------- */

function endGame() {{

    gameEnded = true;

    gameStarted = false;

    answer.disabled = true;

    message.innerText =
        "GAME OVER! Score: " + score;

}}


/* -----------------------------
   FINISH
----------------------------- */

function finishGame() {{

    gameEnded = true;

    gameStarted = false;

    answer.disabled = true;

    bitDisplay.innerText =
        "DONE";

    message.innerText =
        "🎉 YOU FINISHED! Score: " + score;

}}


/* -----------------------------
   GAME LOOP
----------------------------- */

function gameLoop() {{

    if (!gameStarted) {{

        drawPipes();

        requestAnimationFrame(gameLoop);

        return;
    }}


    /*
    Bird physics
    */

    velocity += GRAVITY;

    birdY += velocity;

    bird.style.top =
        birdY + "px";


    /*
    Move the map
    */

    pipes.forEach(pipe => {{

        pipe.x -= PIPE_SPEED;


        /*
        Score when the bird
        passes a pipe.
        */

        if (
            !pipe.passed &&
            pipe.x + 60 < BIRD_X
        ) {{

            pipe.passed = true;

            score++;

            scoreDisplay.innerText =
                "Score: " + score;
        }}


        /*
        Collision
        */

        if (checkCollision(pipe)) {{

            endGame();

        }}
    }});


    /*
    Remove old pipes
    */

    pipes = pipes.filter(
        pipe => pipe.x > -70
    );


    /*
    Ground and ceiling
    */

    if (
        birdY < 0 ||
        birdY + 30 > GAME_HEIGHT
    ) {{

        endGame();

    }}


    drawPipes();

    requestAnimationFrame(gameLoop);

}}


/* -----------------------------
   START GAME
----------------------------- */

createMap();


setTimeout(() => {{

    message.innerText = "";

    gameStarted = true;

    showBit();

    answer.focus();

}}, 2000);


requestAnimationFrame(gameLoop);

</script>

</body>

</html>
"""

components.html(
    game,
    height=470
)
```
