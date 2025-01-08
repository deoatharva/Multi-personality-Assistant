import streamlit as st
from chatbot import generate_response  # Import the function from chatbot.py

def main():
    st.title("Chatbot")

    user_input = st.text_input("You:", "")

    if st.button("Send"):
        if user_input:
            response = generate_response(user_input)
            st.text_area("Chatbot:", value=response, height=10000)
        else:
            st.warning("Please enter a message.")

if __name__ == "__main__":
    main()
