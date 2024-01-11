import json
import openai
import os
import tkinter as tk
from tkinter import scrolledtext, font
from agent import initialize_finance_agent, initialize_search_agent
import threading
import random
import time

# Load API keys from 'keys.json'
keys = {}
with open("keys.json", "r") as f:
    keys = json.load(f)

# Set OpenAI API key from the loaded keys
openai_api_key = keys["OPENAI_API_KEY"]
os.environ["OPENAI_API_KEY"] = openai_api_key

# Initialize agents
web_search_agent = initialize_search_agent(serp_api_key=keys["SERP_API_KEY"])
finance_agent = initialize_finance_agent(serp_api_key=keys["SERP_API_KEY"])

def handle_query(query):
    # Determine if the question is trivial or not
    if is_trivial_question(query):
        response = web_search_agent.invoke({"input": query})
    else:
        try:
            response = finance_agent.invoke({"input": query})
        except Exception as e:  # Catch any errors from finance_agent
            response = web_search_agent.invoke({"input": query})
    if response == "N/A":
        response = web_search_agent.invoke({"input": query})
    return response['output']

def is_trivial_question(query):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides information.",
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
        )
        response = completion.choices[0].message.content
        print(response)
        return True if response == "True" else False
    except Exception as e:
        # Handle exceptions, possibly default to False if API call fails
        print(f"Error in OpenAI API call: {e}")
        return False

def on_submit():
    user_query = input_field.get()
    output_field.config(state='normal')
    output_field.insert('end', 'User: ' + user_query + '\n', 'light_green_tag')
    input_field.delete(0, 'end')

    # Run the query handling in a separate thread to keep the UI responsive
    threading.Thread(target=lambda: process_query(user_query)).start()

def process_query(query):
    response = handle_query(query)

    # Insert response with typing animation
    output_field.config(state='normal')
    for char in 'Bot: ' + response + '\n\n':
        output_field.insert('end', char, 'light_red_tag')
        output_field.see(tk.END)  # Scroll to the end
        time.sleep(0.012)  # Adjust typing speed as needed
    output_field.config(state='disabled')

# GUI setup
root = tk.Tk()
root.title("Chatbot")
root.geometry("1000x800")

# Check if Georgia font is available, otherwise use Arial as fallback
available_fonts = list(font.families())
if 'Georgia' in available_fonts:
    text_font_name = 'Georgia'
else:
    text_font_name = 'Arial'  # Fallback font

text_font = (text_font_name, 16)
button_font = (text_font_name, 14, "bold")

# Style configuration
theme_color = "#062635"  # Dark grey color for the theme
input_bg_color = "#0E3948"  # Slightly lighter grey for the input field
hover_color = "#87CEEB"

root.configure(bg=theme_color)

# Output Frame
output_frame = tk.Frame(root, bg=theme_color)
output_frame.pack(side='top', fill='both', expand=True, padx=30, pady=30)

# Output Field
output_field = scrolledtext.ScrolledText(output_frame, state='disabled', wrap='word', font=text_font, bg=theme_color, fg="#EAEAEA")
output_field.pack(side='left', fill='both', expand=True)
output_field.tag_config('light_green_tag', foreground='#98FB98')  # Light green color
output_field.tag_config('light_red_tag', foreground='#FFB6C1')    # Light red color

# Input Frame
input_frame = tk.Frame(root, bg=theme_color)
input_frame.pack(side='bottom', fill='x', padx=30, pady=20)

# Input Field
input_field = tk.Entry(input_frame, font=text_font, bg=input_bg_color, fg="#EAEAEA", relief="groove", borderwidth=2)
input_field.pack(side='left', fill='x', expand=True, padx=10)
input_field.bind("<Return>", lambda event: on_submit())

# Submit Button
submit_button = tk.Button(input_frame, text="Submit", command=on_submit, font=button_font, bg=hover_color, fg="black")
submit_button.pack(side='right', padx=10)

root.mainloop()
