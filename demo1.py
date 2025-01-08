import streamlit as st
from transformers import pipeline

# Initialize the model
chatbot = pipeline("text-generation", model="facebook/blenderbot-400M-distill")

# Streamlit application
st.title("Chat with Aarti")
st.write("Hello! I'm Aarti, your friendly chatbot. Feel free to ask me anything.")

if 'history' not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        # Update history with user input
        st.session_state.history.append({"user": user_input})

        # Generate response from the model
        response = chatbot(user_input, max_length=100, num_return_sequences=1)
        assistant_response = response[0]['generated_text']

        # Clean up response for better conversational flow
        assistant_response = assistant_response.replace(user_input, "").strip()

        # Update history with assistant response
        st.session_state.history.append({"assistant": f"Aarti: {assistant_response}"})

        # Display conversation history
        for exchange in st.session_state.history:
            if 'user' in exchange:
                st.write(f"You: {exchange['user']}")
            if 'assistant' in exchange:
                st.write(f"{exchange['assistant']}")
