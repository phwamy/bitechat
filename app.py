import streamlit as st
from bitechat_elasticsearch import chat
import uuid

def initialize_session_state():
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4()) 
    if 'filter' not in st.session_state:
        st.session_state.filter = []
    if "messages" not in st.session_state:
        st.session_state.messages = []

def setup_page_layout():
    st.set_page_config(layout="wide")
    logo_html = """<img src="https://github.com/phwamy/bitechat/blob/main/bitechat_logo.png?raw=true" alt="Logo" width="70" height="70">"""
    col1, col2 = st.columns([1, 8])  # Adjust the ratio as needed
    with col1:
        st.markdown(logo_html, unsafe_allow_html=True)
    with col2:
        st.title("BiteChat")

def setup_sidebar():
    # Initialize the 'filter' key in session_state if it doesn't already exist
    if 'filter' not in st.session_state:
        st.session_state.filter = []

    # Function to update the session state based on checkbox interactions
    def update_filter(option, is_checked):
        if is_checked:
            if option not in st.session_state.filter:
                st.session_state.filter.append(option)
        else:
            if option in st.session_state.filter:
                st.session_state.filter.remove(option)

    with st.sidebar:
        st.write("## Price")
        price_options = {"$": "price level inexpensive", "$$": "price level moderate", "$$$": "price level expensive"}
        for price, label in price_options.items():
            if st.checkbox(price, key=f"price_{price}"):
                update_filter(label, True)
            else:
                update_filter(label, False)
        
        st.write("## Dining Options")
        dining_options = {"Dine-in": "Dine-in", "Takeout": "Takeout", "Delivery": "Delivery", "Curbside Pickup": "Curbside Pickup"}
        for option, label in dining_options.items():
            if st.checkbox(option, key=f"dining_{option}"):
                update_filter(label, True)
            else:
                update_filter(label, False)
        
        st.write("## Dietary Preferences")
        for preference in ["Vegetarian", "Vegan", "Gluten-Free"]:
            if st.checkbox(preference, key=f"diet_{preference}"):
                update_filter(preference, True)
            else:
                update_filter(preference, False)
        
        st.write("## Atmosphere")
        atmosphere_options = {
            "Kid-Friendly": "good for children",
            "Pet-Friendly": "allows dogs",
            "Sports Bar": "good for watching sports",
            "Live Music": "Live Music",
            "Large Groups": "good for groups"
        }
        for atmosphere, label in atmosphere_options.items():
            if st.checkbox(atmosphere, key=f"atmos_{atmosphere}"):
                update_filter(label, True)
            else:
                update_filter(label, False)
        
        st.write("## Essential Information")
        for info in ["Accessibility", "Parking"]:
            if st.checkbox(info, key=f"info_{info}"):
                update_filter(info, True)
            else:
                update_filter(info, False)

        # Debugging: Display current filters
        # st.sidebar.write("### Current Filters:")
        # st.sidebar.write(st.session_state.filter)

# Display chat history
def display_chat_history():
    for message in st.session_state.messages: 
        if message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])
        else:
            st.chat_message("user").write(message["content"])

# Chat handler
def handle_chat():
    with st.spinner("Spooning..."):
        if "message" not in st.session_state:
            st.session_state.message = []

        for message in st.session_state.message:
            with st.chat_message(message["role"]):
                st.markdown(message['content'])

        if prompt := st.chat_input("Seeking any food suggestion?"):
            st.session_state.messages.append({"role": "user", "content": prompt + str(st.session_state.filter)})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                response = ""
                response = chat(prompt, st.session_state.session_id)['output']
                message_placeholder.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    initialize_session_state()
    setup_page_layout()
    setup_sidebar()
    display_chat_history()
    handle_chat()

if __name__ == "__main__":
    main()