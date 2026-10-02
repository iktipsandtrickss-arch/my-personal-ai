import gradio as gr

def chat(message, history):
    return "তুমি বলেছো: " + message

demo = gr.ChatInterface(
    fn=chat,
    title="My Personal AI",
    description="My own AI assistant"
)

demo.launch()
