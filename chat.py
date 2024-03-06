import streamlit as st
import random
import time
import biteChatRAG
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI with your API key
field_id = os.getenv('FIELD_ID')
assistant_id = os.getenv('ASSISTANT_ID')
api_key = os.getenv('API_KEY')
client=OpenAI(api_key = api_key)

assistant = biteChatRAG.BiteChaAssistant(client, assistant_id)

# Layout configuration for full width
st.set_page_config(layout="wide")

# Assuming you've saved your logo as 'logo.png' in your project directory
logo_html = """<img src="./bitechat_logo.png" alt="Logo" width="70" height="70">"""

col1, col2 = st.columns([1, 8])  # Adjust the ratio as needed

with col1:
    st.markdown(logo_html, unsafe_allow_html=True)
with col2:
    st.title("BiteChat")



# Adding a sidebar for filters and logo at the top of the main page
with st.sidebar:
    st.title("Filters")
    # Example filter: Cuisine Type
    cuisine_type = st.selectbox("Choose a cuisine", ["Any", "Italian", "Mexican", "Chinese", "Indian"])
    
    # Food Type
    food_type = st.selectbox("Food Type", ["Any", "Vegan", "Non-Veg", "Gluten-Free"])
    
    # Restaurant Type
    restaurant_type = st.selectbox("Restaurant Type", ["Any", "Cafe", "Bistro", "Fine Dining", "Fast Food"])
    
    # Dine In or Takeaway
    dining_option = st.radio("Dining Option", ["Any", "Dine-In", "Takeaway"])
    
    # Pet Friendly
    pet_friendly = st.checkbox("Pet Friendly")
    
    # Children Friendly
    children_friendly = st.checkbox("Children Friendly")



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message_container():
        st.chat_message(message=message["content"], is_user=message["role"] == "user")

# Accept user input
with st.spinner("Spooning..."):
    if "message" not in st.session_state:
        st.session_state.message = []

    for message in st.session_state.message:
        with st.chat_message(message["role"]):
            st.markdown(message['content'])

    if prompt := st.chat_input("Seeking any food suggestion?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = ""
            response = assistant.run_bitechat(prompt)
            message_placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})