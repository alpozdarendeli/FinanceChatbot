import json
import os
import threading
import time
import tkinter as tk
from tkinter import scrolledtext, font

from openai import OpenAI
from agent import initialize_finance_agent, initialize_search_agent, web_search_agent_func_schema, finance_search_agent_func_schema
from config import MODEL_NAME

# Load API keys from 'keys.json' and set environment variables
keys = {}
with open("keys.json", "r") as f:
    keys = json.load(f)

os.environ["OPENAI_API_KEY"] = keys["OPENAI_API_KEY"]

# Initialize web and finance search agents
web_search_agent = initialize_search_agent(serp_api_key=keys["SERP_API_KEY"])
finance_agent = initialize_finance_agent(serp_api_key=keys["SERP_API_KEY"])

# Initialize OpenAI client and create an assistant
client = OpenAI()
assistant = client.beta.assistants.create(
    name="Finance Chatbot",
    instructions="You are a financial chatbot. Use both of your tools to answer financial queries. Rely on webSearch as much as possible, you should use financeSearch only scholar or stock price queries. Summarize your findings to give a coherent answer.",
    tools=[
        {"type": "function", "function": web_search_agent_func_schema},
        {"type": "function", "function": finance_search_agent_func_schema}
    ],
    model=MODEL_NAME
)
print(assistant.id)

# Create a new conversation thread
thread = client.beta.threads.create()

# Function definitions for various operations
def financeSearch(input: str):
    return finance_agent.run({"input": input})

def webSearch(input: str):
    return web_search_agent.run({"input": input})

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.05)
    return run

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()

def handle_query(query):
    run = submit_message(assistant.id, thread, query)
    while run.status == "in_progress" or run.status == "queued":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run.status == "completed":
            return client.beta.threads.messages.list(
              thread_id=thread.id
            )
        if run.status == "requires_action":
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                if tool_call.function.name == "webSearch":
                    input = json.loads(tool_call.function.arguments)['input']
                    response = webSearch(input)
                    run = client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=[
                            {
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(response),
                            }
                        ],
                    )
                    run = wait_on_run(run, thread)
                elif tool_call.function.name == "financeSearch":
                    prompt = json.loads(tool_call.function.arguments)['input']
                    response = financeSearch(prompt)
                    run = client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=[
                            {
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(response),
                            }
                        ],
                    )
                    run = wait_on_run(run, thread)
    pretty_print(get_response(thread))
    messages = get_response(thread)
    responses = [m.content[0].text.value for m in messages if m.role == "assistant"]
    return '\n'.join(responses)

def process_query(query):
    response = handle_query(query)
    output_field.config(state='normal')
    for char in 'Bot: ' + response + '\n\n':
        output_field.insert('end', char, 'light_red_tag')
        output_field.see(tk.END)  # Scroll to the end
        time.sleep(0.012)  # Adjust typing speed as needed
    output_field.config(state='disabled')

def on_submit():
    user_query = input_field.get()
    output_field.config(state='normal')
    output_field.insert('end', 'User: ' + user_query + '\n', 'light_green_tag')
    input_field.delete(0, 'end')
    threading.Thread(target=lambda: process_query(user_query)).start()

def setup_gui():
    root = tk.Tk()
    root.title("Chatbot")
    root.geometry("1000x800")

    # Check if Georgia font is available, otherwise use Arial as fallback
    available_fonts = list(font.families())
    text_font_name = 'Georgia' if 'Georgia' in available_fonts else 'Arial'
    text_font = (text_font_name, 16)
    button_font = (text_font_name, 14, "bold")

    theme_color = "#062635"
    input_bg_color = "#0E3948"
    hover_color = "#87CEEB"
    root.configure(bg=theme_color)

    output_frame = tk.Frame(root, bg=theme_color)
    output_frame.pack(side='top', fill='both', expand=True, padx=30, pady=30)

    global output_field
    output_field = scrolledtext.ScrolledText(output_frame, state='disabled', wrap='word', font=text_font, bg=theme_color, fg="#EAEAEA")
    output_field.pack(side='left', fill='both', expand=True)
    output_field.tag_config('light_green_tag', foreground='#98FB98')
    output_field.tag_config('light_red_tag', foreground='#FFB6C1')

    input_frame = tk.Frame(root, bg=theme_color)
    input_frame.pack(side='bottom', fill='x', padx=30, pady=20)

    global input_field
    input_field = tk.Entry(input_frame, font=text_font, bg=input_bg_color, fg="#EAEAEA", relief="groove", borderwidth=2)
    input_field.pack(side='left', fill='x', expand=True, padx=10)
    input_field.bind("<Return>", lambda event: on_submit())

    submit_button = tk.Button(input_frame, text="Submit", command=on_submit, font=button_font, bg=hover_color, fg="black")
    submit_button.pack(side='right', padx=10)

    root.mainloop()

setup_gui()
