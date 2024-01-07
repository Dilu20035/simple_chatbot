import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import os
import openai

st.set_page_config(page_title="HDA-Medical-Chatbot", page_icon=None, layout="wide", initial_sidebar_state="expanded", menu_items=None)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand navbar-dark" style="position: fixed; top: 0; left: 0; width: 100%; display: flex; justify-content: space-between; padding: 0.4rem; background-color: rgba(76,68,182); color: white;">
    <div class="collapse navbar-collapse justify-content-center align-items-center " id="navbarNav">
        <ul class="navbar-nav ">
            <li class="nav-item active" style="margin-right: 45rem; font-size: 1.2rem;">
                <a class="nav-link " href="#"><b> Medical Diagnostic AI-Chatbot </b><span class="sr-only">(current)</span></a>
            </li>
            <li>
                <div>
                    <a href="#" target="_self"><button style="background-color: #fff; color: #443e85; padding: 0.5rem 1rem; border: none; cursor: pointer; border-radius: 1rem; margin-top: 3px;">Close</button></a>
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

api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    st.error("OpenAI API key not found. Set the environment variable 'OPENAI_API_KEY'.")
    st.stop()
else:
    openai.api_key = api_key


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


st.title('')
# Streamlit App Title
st.markdown("<h1 style='text-align: center;'>Medical Diagnostic AI-Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask Medical Related Queries With Our Chatbot And Find The Results</p>", unsafe_allow_html=True)
st.markdown("")

# Initialize conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []


# Default prompt for the medical specialist
default_prompt = "You are a medical specialist. I need your expertise to understand various medical conditions, treatments, and procedures. You are a helpful Medical Diagnostic AI Doctor. Who answers brief questions about Diseases, Symptoms, and medical findings. And You don't answer anything related to non-medical user-inputs. Can you provide information?"

# Function to call OpenAI's completion endpoint
def get_openai_response(user_input):
    medical_prompt = "As a medical specialist, I have expertise in various medical areas. Please provide more details about your query."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=medical_prompt + "\n" + user_input,
        max_tokens=150,  # Adjust the number of tokens based on your requirements
        temperature=0.6,  # Adjust the randomness of responses
        stop=["You:", "Bot:"]  # Stop generation at these markers
    )
    return response.choices[0].text.strip()

# ChatGPT Model selection
model = st.selectbox("ChatGPT Model", ("text-davinci-003",))

# Create a text input box for user input
user_input = st.text_area("Ask Medical-Related Questions:", key="user_input", placeholder="Ask Something...")

# Ask button to trigger the conversation
col1, col2 = st.columns([5, 1])
if col1.button("Ask"):
    if user_input:
        st.session_state.conversation.append({"role": "user", "content": user_input})
        
        # Generate OpenAI response
        bot_response = get_openai_response(default_prompt + "\n" + user_input)
        st.session_state.conversation.append({"role": "bot", "content": bot_response})
        
        # Display the most recent bot response in an output box
        if st.session_state.conversation and st.session_state.conversation[-1]["role"] == "bot":
            latest_bot_response = st.session_state.conversation[-1]["content"]
            bot_output = st.empty()
            bot_output.write(f"CHATBOT Says :-  {latest_bot_response}")
        
        # Display conversation history in reverse order
        for i in range(len(st.session_state.conversation) - 3, -1, -2):
            st.text_area("You:", value=st.session_state.conversation[i - 1]["content"], key=f"user_input_{i - 1}", disabled=True)
            st.text_area("Bot:", value=st.session_state.conversation[i]["content"], key=f"bot_response_{i}", disabled=True)
    else:
        st.warning("Please enter a question.")

with col2:
    if st.button("Clear"):
        user_input = st.empty()
