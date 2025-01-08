import streamlit as st
from transformers import pipeline

# Initialize the text generation model
chatbot = pipeline("text-generation", model="facebook/blenderbot-400M-distill")

# Streamlit application
st.title("Girlfriend Chatbot")
st.write("Hello! I'm here to chat with you. Feel free to ask me anything.")

if 'history' not in st.session_state:
    st.session_state.history = []

def generate_response(prompt):
    # Generate a response using the model
    response = chatbot(prompt, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        # Append user input to history
        st.session_state.history.append({"user": user_input})

        # Construct the prompt by combining previous history
        conversation_history = "\n".join(f"You: {item['user']}" for item in st.session_state.history if 'user' in item)
        prompt = f"{conversation_history}\nAssistant:"
        
        # Generate response from the model
        assistant_response = generate_response(prompt)

        # Append assistant response to history
        st.session_state.history.append({"assistant": assistant_response.strip()})

        # Display conversation history
        for exchange in st.session_state.history:
            if 'user' in exchange:
                st.write(f"You: {exchange['user']}")
            if 'assistant' in exchange:
                st.write(f"Assistant: {exchange['assistant']}")
