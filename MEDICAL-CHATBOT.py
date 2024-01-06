import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import os
from dotenv import load_dotenv
import openai

st.set_page_config(page_title="HDA-Medical-Chatbot", page_icon=None, layout="centered", initial_sidebar_state="expanded", menu_items=None)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand navbar-dark" style="position: fixed; top: 0; left: 0; width: 100%; display: flex; justify-content: space-between; padding: 0.4rem; background-color: rgba(76,68,182,0.808); color: white;">
    <div class="collapse navbar-collapse justify-content-center align-items-center " id="navbarNav">
        <ul class="navbar-nav ">
            <li class="nav-item active" style="margin-right: 45rem; font-size: 1.2rem;">
                <a class="nav-link " href="#"><b> Medical Chatbot </b><span class="sr-only">(current)</span></a>
            </li>
            <li>
                <div>
                    <a href="https://chat.openai.com/c/12b8e7b5-491e-4353-b86b-af4e62c02fc6" target="_self"><button style="background-color: #fff; color: #443e85; padding: 0.5rem 1rem; border: none; cursor: pointer; border-radius: 1rem; margin-top: 3px;">Close</button></a>
                </div>
            </li>
        </ul>
    </div>
</nav>


""", unsafe_allow_html=True)

#<li class="nav-item">
#                <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
#            </li>

    

# Set the theme colors
st.markdown(
    """
    <style>
    :root {
        --primary-color: #B21F33;
        --background-color: 002b36;
        --secondary-background-color: #586e75;
        --text-color: #fafafa;
        --font: sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)        


reduce_header_height_style = """
    <style>
        div.block-container {padding-top:0rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)




hide_st_style = """
            <style>
            #MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()





lottie_coding = load_lottieurl("https://lottie.host/e8cca356-1ed3-4d6d-a263-377ffdbfae98/L1n9J2mGso.json")  # replace link to local lottie file


with st.sidebar:   
    selected = option_menu('',['MEDICAL-CHATBOT'],
                          icons=['person'],
                          default_index=0,
                          
                          )
    st_lottie(
                           lottie_coding,
                           speed=1,
                           reverse=False,
                           loop=True,
                           quality="low", # medium ; high
                           height="250px",
                           width="250px",
                           key=None,
                           )
        


code = """
"https://multiplediseasedetector.streamlit.app/"
"""

# Display the code in the sidebar using markdown
st.sidebar.markdown("```python\n{}\n```".format(code))

# Execute the code and display its output in the sidebar
with st.sidebar:
    exec(code)


def get_initial_message():
    messages = [
        {"role": "system", "content": "You are a helpful Medical Diagnostic AI Doctor. Who answers brief questions about Diseases, Symptoms, and medical findings."},
        {"role": "user", "content": "I want to know about my disease"},
        {"role": "assistant", "content": "That's awesome, what do you want to know about medical conditions?"}
    ]
    return messages

def get_chatgpt_response(messages, model="davinci"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

def update_and_display_response(query, model):
    messages = st.session_state.get('messages', [])
    messages = update_chat(messages, "user", query)
    response = get_chatgpt_response(messages, model)
    messages = update_chat(messages, "assistant", response)
    st.session_state['past'] = st.session_state.get('past', []) + [query]
    st.session_state['generated'] = st.session_state.get('generated', []) + [response]
    st.session_state['messages'] = messages

st.title("Medical Chatbot")
st.subheader("Ask Medical-Related Questions:")

model = st.selectbox("ChatGPT Model", ("davinci",))

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

query = st.text_input("Ask a medical question: ", key="input", value="What are the symptoms of a common cold?")

if st.button("Ask"):
    if query:
        with st.spinner("Generating response..."):
            update_and_display_response(query, model)

past_messages = st.session_state.get('past', [])
generated_responses = st.session_state.get('generated', [])

for i in range(len(past_messages) - 1, -1, -1):
    st.text(f"User: {past_messages[i]}")
    st.text(f"Assistant: {generated_responses[i]}")
