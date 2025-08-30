import gradio as gr
import requests, json
from app_env import *
from flask import redirect

# Call Ollama API
def generate(prompt, context):
    r = requests.post(ollama_api_host + ':' + ollama_api_port + ollama_api_path,
                     json={
                         'model': model,
                         'prompt': prompt,
                         'context': context,
                         'system': system,
                     },
                     stream=False)
    r.raise_for_status() 
    response = ""  
    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        print(response_part)
        if 'error' in body:
            raise Exception(body['error'])

        response += response_part

        if body.get('done', False):
            context = body.get('context', [])
            return response, context

# Call for chatbot
def chat(input, chat_history):
    chat_history = chat_history or []
    global context
    output, context = generate(input, context)
    chat_history.append((input, output))
    return chat_history, chat_history, None

#########################Gradio Code##########################
block = gr.Blocks()

with gr.Blocks(theme=gr.themes.Base()) as app:    
    
    m = gr.Markdown()

    with gr.Tab("Chat"):
        state = gr.State()
        with gr.Row() as row:
            with gr.Column():
                chatbot = gr.Chatbot()
                message = gr.Textbox(label="Write here")
                submit = gr.Button("Query")
                submit.click(chat, inputs=[message, state], outputs=[chatbot, state, message])
    
app.queue().launch(show_api=False,server_port=7070)