from flask import Flask, request, render_template, session, redirect, url_for
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Flask app
app = Flask(__name__,static_folder="static")
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


@app.route('/clear', methods=['POST'])
def clear_chat():
    session.pop('chat_history', None)  # Clear the chat history
    return redirect(url_for('home'))  # Redirect to the home route



# Run the app
if __name__ == '__main__':
    app.run(debug=True,port=5000)
