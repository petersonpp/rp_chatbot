import gradio as gr
import openai
import os
import logging
import json
from logging.handlers import TimedRotatingFileHandler
from transformers import GPT2Tokenizer

# enable logging with daily rotating logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('chatbot.log', when='midnight')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# load openai info from .env file
from dotenv import load_dotenv
load_dotenv()
try:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")
except Exception as e:
    logger.error(f"Error while fetching environment variables: {str(e)}")
    raise

# initialize messages variable 
messages = []

# truncate context size if exceeding model limit (4096)
def truncate_messages(messages, max_tokens=4096):
    global total_tokens
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    
    total_tokens = 0
    truncated_messages = []
    
    for msg in reversed(messages):  # start from the most recent message
        tokens = tokenizer.encode(msg["content"], return_tensors="pt")
        tokens_count = tokens.shape[1]  # get the number of tokens
        
        if total_tokens + tokens_count <= max_tokens:
            total_tokens += tokens_count
            truncated_messages.append(msg)
        else:
            break  # stop if adding the next message will exceed max_tokens
    
    # reverse again to maintain the original order
    return truncated_messages[::-1]

# call openai api to respond based on the history and latest user input
def completion(user_input, chat_history):
    global messages
    if len(user_input) > 200: # limit the user input size
        return "Error: Message too long. Please limit your input to 200 characters.", chat_history, chat_history
    messages.append({"role":"user", "content":str(user_input)})
    messages = truncate_messages(messages, max_tokens=3584)  # leave 512 tokens for the response
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=512,
            temperature=0.9,
            frequency_penalty=0.7,
            presence_penalty=0.7
            )
    except Exception as e:
        logger.error(f"Error during OpenAI API call: {str(e)}")
        return "Error: Unable to process the request at this moment. Please try again later.", chat_history, chat_history
    bot_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content":str(bot_reply)})
    chat_history.append((user_input, bot_reply))
    return "", chat_history, chat_history, gr.update(value=messages)

# populate the character selection dropdown with the list of characters (.json files) available in the ./characters directory
def get_character_names(directory):
    return [os.path.splitext(file)[0] for file in os.listdir(directory) if file.endswith('.json')] 

# select the character, load the prompts from the .json and update the avatar (same filename as the character .json, but with a .png extension, in the characters directory), scenario and prompts
def character_select(choice):
    global char_name, messages, scenario_header
    char_name = choice
    with open(f'characters/{char_name}.json', 'r') as file:
        character_data = json.load(file)
    active_prompt = character_data['system prompt']
    active_description = character_data['char description']
    active_scenario = character_data['scenario']
    scenario_header = []
    scenario_header.append(("", active_scenario["content"]))
    messages = [active_prompt, active_description, active_scenario]
    return gr.update(value=f"![](file/characters/{char_name}.png)"), scenario_header

# clear all chatbot fields
def chatbot_clear():
    return gr.update(value="")

# build the gradio interface
with gr.Blocks() as demo:
    with gr.Row():    
        chatbot = gr.Chatbot(show_label=False, scale=10, height=600)
        state = gr.State()
        with gr.Column(min_width=220):
            with gr.Row():
                character_directory = 'characters'
                character_names = get_character_names(character_directory)
                dropdown = gr.Dropdown(character_names, label="Who do you approach?", allow_custom_value=False)
            with gr.Row():
                with gr.Box():
                    avatar = gr.Markdown(value="")
            dropdown.change(fn=character_select, inputs=dropdown, outputs=[avatar, chatbot])
            dropdown.change(fn=chatbot_clear, outputs=chatbot)
    with gr.Row():
        usr_msg = gr.Textbox(interactive=True, show_label=False, placeholder="Character Selection:", scale=8)
        with gr.Column(min_width=220):
            submit = gr.Button(value="Submit")
            clear = gr.ClearButton([usr_msg, chatbot])
            usr_msg.submit(fn=completion, inputs=[usr_msg, chatbot], outputs=[usr_msg, state, chatbot])
            submit.click(fn=completion, inputs=[usr_msg, chatbot], outputs=[usr_msg, state, chatbot])

# launch the chatbot
try:
    demo.queue(concurrency_count=3)
    demo.launch()
except Exception as e:
    logger.error(f"Error during application launch: {str(e)}")
    raise
