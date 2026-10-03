// ===============================
// BRO FRONTEND → GRADIO BACKEND
// ===============================

const BACKEND_URL = "https://my-personal-ai-bwfc.onrender.com";

const input = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const messages = document.querySelector(".messages");
const newChatButton = document.querySelector(".new-chat");

let chatHistory = [];


// ===============================
// ADD MESSAGE
// ===============================

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

    return message;
}


// ===============================
// TYPING / LOADING
// ===============================

function addTyping() {
    const message = document.createElement("div");

    message.className = "message ai";
    message.id = "typingMessage";

    message.innerHTML = `
        <div class="avatar">🤖</div>
        <div class="bubble">
            <div class="name">BRO</div>
            <div class="text">
                <span class="typing">Thinking...</span>
            </div>
        </div>
    `;

    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
}


function removeTyping() {
    const typing = document.getElementById("typingMessage");

    if (typing) {
        typing.remove();
    }
}


// ===============================
// SEND MESSAGE
// ===============================

async function sendMessage() {

    const text = input.value.trim();

    if (!text) return;

    // Show user message
    addMessage(text, "user");

    // Clear input
    input.value = "";

    // Disable button
    sendButton.disabled = true;

    // Show typing
    addTyping();

    try {

        // Gradio API
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
            throw new Error(`HTTP ${response.status}`);
        }

        const result = await response.json();

        // Gradio returns an event ID
        const eventId = result.event_id;
        console.log("GRADIO START RESPONSE:", result);
alert(JSON.stringify(result));

        if (!eventId) {
            throw new Error("No event_id returned by Gradio");
        }


        // ===============================
        // WAIT FOR GRADIO RESULT
        // ===============================

        const resultResponse = await fetch(
            `${BACKEND_URL}/gradio_api/call/chat/${eventId}`
        );

        if (!resultResponse.ok) {
            throw new Error(`Result HTTP ${resultResponse.status}`);
        }


        // Gradio streams events
        const reader = resultResponse.body.getReader();
        const decoder = new TextDecoder();

        let buffer = "";
        let finalAnswer = "";


        while (true) {

            const { value, done } = await reader.read();

            if (done) break;

            buffer += decoder.decode(value, {
                stream: true
            });

            const lines = buffer.split("\n");

            buffer = lines.pop();


            for (const line of lines) {

                if (!line.startsWith("data:")) {
                    continue;
                }

                const data = line.substring(5).trim();

                if (!data) continue;

                try {

                    const parsed = JSON.parse(data);

                    if (Array.isArray(parsed)) {

                        // Usually Gradio output is:
                        // [answer]

                        if (parsed.length > 0) {
                            finalAnswer = parsed[0];
                        }

                    }

                } catch (e) {

                    // Ignore non-JSON streaming lines

                }
            }
        }


        removeTyping();


        if (!finalAnswer) {
            finalAnswer =
                "Bro, backend থেকে কোনো response আসেনি 😕";
        }


        // Show AI response
        addMessage(finalAnswer, "ai");


        // Save conversation locally
        chatHistory.push({
            role: "user",
            content: text
        });

        chatHistory.push({
            role: "assistant",
            content: finalAnswer
        });


    } catch (error) {

        console.error("BRO ERROR:", error);

        removeTyping();

        addMessage(
            "Backend-এর সাথে connection problem হচ্ছে bro 😕\n\n" +
            "Render server বা Gradio API check করো।",
            "ai"
        );

    } finally {

        sendButton.disabled = false;
        input.focus();

    }
}


// ===============================
// ENTER TO SEND
// ===============================

input.addEventListener("keydown", function(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }

});


// ===============================
// SEND BUTTON
// ===============================

sendButton.addEventListener("click", sendMessage);


// ===============================
// NEW CHAT
// ===============================

newChatButton.addEventListener("click", function() {

    chatHistory = [];

    messages.innerHTML = `
        <div class="message ai">

            <div class="avatar">🤖</div>

            <div class="bubble">

                <div class="name">BRO</div>

                <div class="text">
                    New chat started 👋
                    <br><br>
                    What's up bro?
                </div>

            </div>

        </div>
    `;

    input.focus();

});
