import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(
    page_title="Binary Flappy Bird",
    page_icon="🐤",
    layout="centered"
)

st.title("🐤 Binary Flappy Bird")
st.write("The word creates the map. Type 0 or 1 to control the bird!")

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

st.subheader(f"Word: {word}")

# Convert every letter into 8-bit binary
binary = ""

for letter in word:
    binary += format(ord(letter), "08b")


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
    top: 280px;

    background: #FFD700;

    border-radius: 50%;

    z-index: 10;
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

    z-index: 20;
}}

#status {{
    position: absolute;

    right: 15px;
    top: 10px;

    color: white;

    font-size: 22px;
    font-weight: bold;

    text-shadow: 2px 2px #333;

    z-index: 20;
}}

#message {{
    position: absolute;

    width: 100%;

    top: 150px;

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

    z-index: 20;
}}

</style>

</head>


<body>

<div id="game">

    <div id="bird"></div>

    <div id="score">
        Score: 0
    </div>

    <div id="status">
        TYPE 0 OR 1
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

const message = document.getElementById("message");
const status = document.getElementById("status");

const scoreDisplay =
    document.getElementById("score");

const progressDisplay =
    document.getElementById("progress");


/* -------------------------
   GAME SETTINGS
------------------------- */

const GAME_WIDTH = 700;
const GAME_HEIGHT = 450;

const BIRD_X = 100;

const PIPE_SPEED = 2.0;

const SECTION_WIDTH = 190;

const GAP_HEIGHT = 180;


/* -------------------------
   GAME VARIABLES
------------------------- */

let birdY = 280;

let velocity = 0;

let currentBit = 0;

let score = 0;

let pipes = [];

let gameStarted = false;

let gameEnded = false;

let moving = false;

let moveTimer = 0;


/* -------------------------
   CREATE THE MAP
------------------------- */

function createMap() {{

    pipes = [];

    for (let i = 0; i < binary.length; i++) {{

        const bit = binary[i];

        let gapCenter;


        /*
        1 = HIGH GAP

        The player needs to jump.
        */

        if (bit === "1") {{

            gapCenter = 145;

        }}

        /*
        0 = LOW GAP

        The player does not jump.
        */

        else {{

            gapCenter = 305;

        }}


        const gapTop =
            gapCenter - GAP_HEIGHT / 2;

        const gapBottom =
            gapCenter + GAP_HEIGHT / 2;


        pipes.push({{

            x: 500 + i * SECTION_WIDTH,

            gapTop: gapTop,

            gapBottom: gapBottom,

            passed: false
        }});
    }}
}}


/* -------------------------
   DRAW MAP
------------------------- */

function drawPipes() {{

    document
        .querySelectorAll(".pipe")
        .forEach(function(pipe) {{

            pipe.remove();

        }});


    pipes.forEach(function(pipe) {{

        if (
            pipe.x < GAME_WIDTH &&
            pipe.x > -100
        ) {{

            /*
            TOP PIPE
            */

            const topPipe =
                document.createElement("div");

            topPipe.className = "pipe";

            topPipe.style.left =
                pipe.x + "px";

            topPipe.style.top =
                "0px";

            topPipe.style.height =
                pipe.gapTop + "px";


            /*
            BOTTOM PIPE
            */

            const bottomPipe =
                document.createElement("div");

            bottomPipe.className = "pipe";

            bottomPipe.style.left =
                pipe.x + "px";

            bottomPipe.style.top =
                pipe.gapBottom + "px";

            bottomPipe.style.height =
                (GAME_HEIGHT - pipe.gapBottom) + "px";


            document
                .getElementById("game")
                .appendChild(topPipe);

            document
                .getElementById("game")
                .appendChild(bottomPipe);
        }}
    }});
}}


/* -------------------------
   PLAYER ENTERS 0 OR 1
------------------------- */

answer.addEventListener("input", function() {{

    if (!gameStarted || gameEnded) {{
        return;
    }}


    const input = answer.value;


    /*
    Only allow 0 or 1.
    */

    if (
        input !== "0" &&
        input !== "1"
    ) {{

        answer.value = "";

        return;
    }}


    const correctBit =
        binary[currentBit];


    /*
    CORRECT ANSWER
    */

    if (input === correctBit) {{

        /*
        1 = JUMP
        */

        if (input === "1") {{

            velocity = -5.5;

        }}

        /*
        0 = DON'T JUMP
        */

        else {{

            velocity = 1.5;

        }}


        /*
        Start moving through
        this map section.
        */

        moving = true;

        moveTimer = 0;


        answer.value = "";


        status.innerText =
            "GOOD!";


        message.innerText =
            "";


        progressDisplay.innerText =
            currentBit +
            " / " +
            binary.length;


    }}


    /*
    WRONG ANSWER
    */

    else {{

        message.innerText =
            "WRONG!";

        status.innerText =
            "TRY AGAIN";

        answer.value = "";


        setTimeout(function() {{

            if (!gameEnded) {{

                message.innerText = "";

                status.innerText =
                    "TYPE 0 OR 1";
            }}

        }}, 600);
    }}

}});


/* -------------------------
   COLLISION
------------------------- */

function checkCollision(pipe) {{

    const birdLeft =
        BIRD_X;

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


    const horizontal =
        birdRight > pipeLeft &&
        birdLeft < pipeRight;


    const vertical =
        birdTop < pipe.gapTop ||
        birdBottom > pipe.gapBottom;


    return horizontal && vertical;
}}


/* -------------------------
   GAME OVER
------------------------- */

function endGame() {{

    gameEnded = true;

    gameStarted = false;

    moving = false;

    answer.disabled = true;


    message.innerText =
        "GAME OVER! Score: " +
        score;

    status.innerText =
        "GAME OVER";
}}


/* -------------------------
   WIN
------------------------- */

function finishGame() {{

    gameEnded = true;

    gameStarted = false;

    moving = false;

    answer.disabled = true;


    message.innerText =
        "🎉 YOU FINISHED!";

    status.innerText =
        "COMPLETE!";

    progressDisplay.innerText =
        binary.length +
        " / " +
        binary.length;
}}


/* -------------------------
   GAME LOOP
------------------------- */

function gameLoop() {{

    /*
    IMPORTANT:

    The bird and map DON'T MOVE
    while the player is deciding
    what to type.

    This prevents the bird from
    dying before the player answers.
    */


    if (gameStarted && moving) {{

        /*
        Bird physics
        */

        velocity += 0.12;

        birdY += velocity;


        bird.style.top =
            birdY + "px";


        /*
        Move the map
        */

        pipes.forEach(function(pipe) {{

            pipe.x -= PIPE_SPEED;


            /*
            Score when passing
            the pipe.
            */

            if (
                !pipe.passed &&
                pipe.x + 60 < BIRD_X
            ) {{

                pipe.passed = true;

                score++;

                scoreDisplay.innerText =
                    "Score: " + score;


                /*
                The current section
                is finished.
                */

                currentBit++;


                /*
                Stop moving and wait
                for the next answer.
                */

                moving = false;

                moveTimer = 0;


                if (
                    currentBit <
                    binary.length
                ) {{

                    status.innerText =
                        "TYPE 0 OR 1";

                    progressDisplay.innerText =
                        currentBit +
                        " / " +
                        binary.length;

                    answer.focus();

                }}

                else {{

                    finishGame();

                }}
            }});


        /*
        Collision with pipes
        */

        pipes.forEach(function(pipe) {{

            if (checkCollision(pipe)) {{

                endGame();

            }}
        }});


        /*
        Ceiling / floor
        */

        if (
            birdY < 0 ||
            birdY + 30 > GAME_HEIGHT
        ) {{

            endGame();

        }}
    }}


    /*
    Draw the map continuously.
    */

    drawPipes();


    requestAnimationFrame(gameLoop);
}}


/* -------------------------
   START
------------------------- */

createMap();

drawPipes();


setTimeout(function() {{

    message.innerText =
        "";

    gameStarted = true;

    status.innerText =
        "TYPE " + binary[0];

    answer.focus();

}}, 1500);


requestAnimationFrame(gameLoop);

</script>

</body>

</html>
"""


components.html(
    game,
    height=470
)
