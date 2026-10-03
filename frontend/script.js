const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const messages = document.querySelector(".messages");
const newChatButton = document.querySelector(".new-chat");


// =====================================================
// BACKEND
// =====================================================

// Render-এ তোমার Gradio app-এর URL
const BACKEND_URL = "vhttps://my-personal-ai-bwfc.onrender.com/";


// =====================================================
// CHAT HISTORY
// =====================================================

let chatHistory = [];


// =====================================================
// ADD MESSAGE
// =====================================================

function addMessage(text, type) {

    const message = document.createElement("div");

    message.className = `message ${type}`;

    if (type === "ai") {

        message.innerHTML = `
            <div class="avatar">🤖</div>

            <div class="bubble">
                <div class="name">BRO</div>
                <div class="text"></div>
            </div>
        `;

    } else {

        message.innerHTML = `
            <div class="bubble">
                <div class="text"></div>
            </div>
        `;
    }

    message.querySelector(".text").textContent = text;

    messages.appendChild(message);

    messages.scrollTop = messages.scrollHeight;
}


// =====================================================
// TYPING
// =====================================================

function showTyping() {

    const message = document.createElement("div");

    message.id = "typingMessage";
    message.className = "message ai";

    message.innerHTML = `
        <div class="avatar">🤖</div>

        <div class="bubble">
            <div class="name">BRO</div>
            <div class="text">Thinking...</div>
        </div>
    `;

    messages.appendChild(message);

    messages.scrollTop = messages.scrollHeight;
}


function removeTyping() {

    const typing =
        document.getElementById("typingMessage");

    if (typing) {
        typing.remove();
    }
}


// =====================================================
// SEND MESSAGE
// =====================================================

async function sendMessage() {

    const text = input.value.trim();

    if (!text) return;

    sendButton.disabled = true;

    addMessage(text, "user");

    input.value = "";

    showTyping();


    try {

        // =================================================
        // STEP 1 — START GRADIO API CALL
        // =================================================

        const response = await fetch(
            `${BACKEND_URL}/gradio_api/call/chat`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    data: [
                        text,
                        chatHistory
                    ]
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const result =
            await response.json();


        console.log(
            "Gradio start response:",
            result
        );


        const eventId =
            result.event_id;


        if (!eventId) {

            throw new Error(
                "Gradio event ID পাওয়া যায়নি"
            );
        }


        // =================================================
        // STEP 2 — WAIT FOR RESULT
        // =================================================

        const resultResponse =
            await fetch(
                `${BACKEND_URL}/gradio_api/call/chat/${eventId}`
            );


        if (!resultResponse.ok) {

            throw new Error(
                `Result HTTP ${resultResponse.status}`
            );
        }


        const resultText =
            await resultResponse.text();


        console.log(
            "Gradio result:",
            resultText
        );


        // =================================================
        // PARSE SSE
        // =================================================

        let answer = null;

        const lines =
            resultText.split("\n");


        for (const line of lines) {

            if (!line.startsWith("data:")) {
                continue;
            }


            const jsonText =
                line.substring(5).trim();


            if (!jsonText) {
                continue;
            }


            try {

                const data =
                    JSON.parse(jsonText);


                if (Array.isArray(data)) {

                    const last =
                        data[data.length - 1];


                    // Gradio ChatInterface সাধারণত
                    // output-এর মধ্যে string দেয়

                    if (typeof last === "string") {

                        answer = last;

                    } else if (
                        last &&
                        typeof last === "object"
                    ) {

                        answer =
                            last.text ||
                            last.content ||
                            JSON.stringify(last);
                    }
                }


            } catch (error) {

                console.log(
                    "SSE parse error:",
                    error
                );
            }
        }


        removeTyping();


        if (!answer) {

            answer =
                "BRO কোনো response দিতে পারেনি 😕";
        }


        // =================================================
        // SAVE HISTORY
        // =================================================

        chatHistory.push([
            text,
            answer
        ]);


        // =================================================
        // SHOW ANSWER
        // =================================================

        addMessage(
            answer,
            "ai"
        );


    } catch (error) {

        console.error(
            "Backend connection error:",
            error
        );


        removeTyping();


        addMessage(
            "Backend-এর সাথে connection হচ্ছে না bro 😕\n\n" +
            "Render URL অথবা Gradio API check করতে হবে।",
            "ai"
        );
    }


    sendButton.disabled = false;

    input.focus();
}


// =====================================================
// SEND BUTTON
// =====================================================

sendButton.addEventListener(
    "click",
    sendMessage
);


// =====================================================
// ENTER
// =====================================================

input.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);


// =====================================================
// NEW CHAT
// =====================================================

newChatButton.addEventListener(
    "click",
    function() {

        chatHistory = [];

        messages.innerHTML = `
            <div class="message ai">

                <div class="avatar">
                    🤖
                </div>

                <div class="bubble">

                    <div class="name">
                        BRO
                    </div>

                    <div class="text">
                        New chat started 👋
                        <br><br>
                        What's up bro?
                    </div>

                </div>

            </div>
        `;

        input.focus();
    }
);
