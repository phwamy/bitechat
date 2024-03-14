import streamlit as st
from bitechat_elasticsearch import chat
import uuid

def initialize_session_state():
    if 'chat_started' not in st.session_state:
        st.session_state.chat_started = False
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4()) 
    if 'filter' not in st.session_state:
        st.session_state.filter = []
    if "messages" not in st.session_state:
        st.session_state.messages = []

def setup_page_layout():
    st.set_page_config(layout="wide")
    logo_html = """<img src="https://github.com/phwamy/bitechat/blob/main/img/bitechat_logo.png?raw=true" alt="Logo" width="70" height="70">"""
    col1, col2 = st.columns([1, 8])
    with col1:
        st.markdown(logo_html, unsafe_allow_html=True)
    with col2:
        st.title("BiteChat")

def sample_chat(question):
    """
    Function for sample questions to call the chat function and display the response
    """

    st.session_state.chat_started = True

    with st.spinner("Spooning..."):
        st.session_state.messages.append({"role": "user", "content": question})
        response = chat(question, st.session_state.session_id)['output']
        st.session_state.messages.append({"role": "assistant", "content": response})

def setup_sidebar():
    def update_filter(option, is_checked):
        """
        Function to update the session state based on checkbox interactions
        """
        if is_checked:
            if option not in st.session_state.filter:
                st.session_state.filter.append(option)
        else:
            if option in st.session_state.filter:
                st.session_state.filter.remove(option)

    with st.sidebar:
        st.write("## Price")
        price_options = {"-$ Inexpensive": "price level inexpensive", "-$$ Moderate": "price level moderate", "-$$$ Expensive": "price level expensive"}
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
    if st.session_state.chat_started:
        display_sample_question()
        for message in st.session_state.messages: 
            if message["role"] == "assistant":
                st.chat_message("assistant").write(message["content"])
            else:
                st.chat_message("user").write(message["content"])

# Chat handler
def handle_chat():
    with st.spinner("Spooning..."):
        if prompt := st.chat_input("Seeking any food suggestion?"):
            st.session_state.chat_started = True
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                response = ""
                response = chat(prompt + str(st.session_state.filter), st.session_state.session_id)['output']
                message_placeholder.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})

        # for message in st.session_state.messages:
        #     with st.chat_message(message["role"]):
        #         st.markdown(message['content'])

def display_sample_question():
    if not st.session_state.chat_started:
        print(f"chat_started status in display_sample_question: {st.session_state.chat_started}")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        # st.write("How can BiteChat help you today?")
        if st.button("Looking for a dating restaurant"):
            sample_chat("I am looking for a restaurant for a date. Please recommend a few options near University of Washington with good vibe, services and food.")
        if st.button("Looking for best vegetarian Indian food"):
            sample_chat("Looking for vegetarian Indian food in Seattle. Please suggest some spots with signature vegie cuisine.")

        if st.button("Looking for a pet-friendly restaurant with parking availibility"):
            sample_chat("I am looking for a pet-friendly restaurant in Seattle with parking availibility. Please suggest some options.")

        if st.button("Looking for a good Japanese restaurant near Bellevue."):
            sample_chat("I am looking for a good Japanese restaurant near Bellevue. Please suggest some options with their popular dishes.")


def main():
    initialize_session_state()
    setup_page_layout()
    setup_sidebar()
    if not st.session_state.chat_started:
        display_sample_question()
    display_chat_history()
    handle_chat()

if __name__ == "__main__":
    main()