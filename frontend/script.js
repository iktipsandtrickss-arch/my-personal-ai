const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const messages = document.querySelector(".messages");
const newChatButton = document.querySelector(".new-chat");


// ==========================================
// ADD MESSAGE TO CHAT
// ==========================================

function addMessage(text, type) {

    const message = document.createElement("div");

    message.className = `message ${type}`;

    if (type === "ai") {

        message.innerHTML = `
            <div class="avatar">
                🤖
            </div>

            <div class="bubble">

                <div class="name">
                    BRO
                </div>

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


// ==========================================
// SEND MESSAGE
// ==========================================

function sendMessage() {

    const text = input.value.trim();

    if (!text) {
        return;
    }

    // Add user message
    addMessage(text, "user");

    // Clear input
    input.value = "";

    // Temporary AI response
    setTimeout(() => {

        addMessage(
            "আমি এখনো backend-এর সাথে connected হইনি 😎\n\nপরের step-এ আমাকে তোমার SmolLM2/OpenRouter-এর সাথে connect করব।",
            "ai"
        );

    }, 500);
}


// ==========================================
// SEND BUTTON
// ==========================================

sendButton.addEventListener(
    "click",
    sendMessage
);


// ==========================================
// ENTER TO SEND
// ==========================================

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


// ==========================================
// NEW CHAT
// ==========================================

newChatButton.addEventListener(
    "click",
    function() {

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
