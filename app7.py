import streamlit as st
import os
#import openai
#from dotenv import load_dotenv, find_dotenv
#_ = load_dotenv(find_dotenv()) # read local .env file
#openai.api_key  = os.environ['OPENAI_API_KEY']
#import streamlit as st
import openai 
from openai import OpenAI
import base64

#print(openai.VERSION)
#st.title("ChatGPT-like clone")
st.set_page_config(page_title="🦜🔗 Proposal Gen Writer")
st.title('🦜🔗 Proposal Gen Writer')



def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "jpg"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
    
set_bg_hack("./img/bg2.jpg")

##openai_api_key = st.sidebar.text_input('Enter OpenAI API Key')
openai_api_key = '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'
#context1 = st.sidebar.text_area('Enter context')
#st.write(context1)

temp1 = st.sidebar.slider("Enter tempeature lower the value less creativity",min_value=0.0,max_value=2.0)
st.write(temp1)
#text_input('Enter temperature')

# Set OpenAI API key from Streamlit secrets
#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
client = OpenAI(api_key=openai_api_key)
st.write("Hi, I am your proposal writing Assistant")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    st.write("model loading...")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#st.write("Hi, I am your proposal writing Assistant")

context = """ Welcome you can start  - Enter the open api key and temperature in the side bar 
                Provide the context and chat with me - \
               sample context- You are an expert proposal writing Assistant, an automated service \
               to collect the information from Proposal writer and provide proposal document with your skills\
        You first greet the proposal writer, then collects the objective of proposal \
        and then asks for client details, including domain of the client \
        and then ask for problem they want to solve \
        and then ask for what is the current data source\
        and then ask for what is your proposed solution\
        and collect the entire information summarize and provide in structured template\
        ask one question at a time.
You respond in by using a template of proposal writer,
with detailed elobation based on the inputs given, You may ask other question that require
to write proposl for the given problem statement \
As your are an expert in proposal writing you also have the knowledge of business domain understanding"""
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        #st.write("Hi, I am your proposal writing Assistant")

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append(   {'role':'system', 'content':context})
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

# Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[ 
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True, temperature=temp1
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# some change here