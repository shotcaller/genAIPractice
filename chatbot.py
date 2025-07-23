import streamlit as st
from ollamaChatbot import memory_chatbot
from auth import is_authenticated, logout

st.title("My Chatbot")

st.write(st.session_state.get("user_info"))
#Logout button on sidebar
if is_authenticated() and st.sidebar.button("Logout"):
    logout()
    st.rerun()


if "messages" not in st.session_state:
    st.session_state.messages = []
st.write("Hello! I'm your chatbot. How can I assist you today?")

st.sidebar.title("Chatbot Settings")
domain = st.sidebar.selectbox("Select a domain:", ["DevOps", "Microsoft Azure", "GitHub"])

#user input field should be at the bottom
user_input = st.text_input("Type your message here:", key="user_input")

if st.button("Send"):
    #Show spinner while waiting for response
    with st.spinner("Generating response..."):
      st.session_state.messages.append({"role": "user", "content": user_input})
      st.write("You:", user_input)
      
      # Call the memory_chatbot function with the selected domain and user input
      response = memory_chatbot(domain, user_input, thread_id="thread-1")
      
      # Display the chatbot's response
      st.write("Chatbot:", response if response else "No response generated.")
      st.session_state.messages.append({"role": "assistant", "content": response})
      user_input = ""  # Clear the input field after sending

# Display chat history
if st.session_state.messages:
    st.write("Chat History:")
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f"You: {message['content']}")
        else:
            st.write(f"Chatbot: {message['content']}")





