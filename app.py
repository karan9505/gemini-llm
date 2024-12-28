# from dotenv import load_dotenv
# load_dotenv() ## loading all the environment variables

# import streamlit as st
# import os
# import google.generativeai as genai

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ## function to load Gemini Pro model and get repsonses
# model=genai.GenerativeModel("gemini-pro") 
# chat = model.start_chat(history=[])
# def get_gemini_response(question):
    
#     response=chat.send_message(question,stream=True)
#     return response

# ##initialize our streamlit app

# st.set_page_config(page_title="Q&A Demo")

# st.header("Gemini LLM Application")

# # Initialize session state for chat history if it doesn't exist
# if 'chat_history' not in st.session_state:
#     st.session_state['chat_history'] = []

# input=st.text_input("Input: ",key="input")
# submit=st.button("Ask the question")

# if submit and input:
#     response=get_gemini_response(input)
#     # Add user query and response to session state chat history
#     st.session_state['chat_history'].append(("You", input))
#     st.subheader("The Response is")
#     for chunk in response:
#         st.write(chunk.text)
#         st.session_state['chat_history'].append(("Bot", chunk.text))
# st.subheader("The Chat History is")
    
# for role, text in st.session_state['chat_history']:
#     st.write(f"{role}: {text}")
    
# ===============================================================

from flask import Flask, request, render_template, session, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Initialize Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get Gemini response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Route for home page
@app.route('/', methods=['GET', 'POST'])
def home():
    # Initialize session state for chat history
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        input_text = request.form.get('input_text')
        if input_text:
            # Get Gemini response
            response = get_gemini_response(input_text)
            response_text = "".join([chunk.text for chunk in response])

            # Update session chat history
            session['chat_history'].append(("You", input_text))
            session['chat_history'].append(("Bot", response_text))
            session.modified = True  # Mark session as modified for updates

    return render_template('index.html', chat_history=session.get('chat_history', []))

# Route to clear chat history
@app.route('/clear', methods=['POST'])
def clear_chat():
    session.pop('chat_history', None)
    return jsonify({"success": True})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)