# importing the necessary libraries
import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession


# project id from google cloud console
project = "gemini-explorer-430219"
vertexai.init(project=project)


# setting the generation config and initilizing the model
config = generative_models.GenerationConfig(
    temperature=0.4
)

model = GenerativeModel(
    model_name="gemini-pro",
    generation_config=config
)

chat = model.start_chat()

# defining a helper function to interact with the model, display the output and store the conversation
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

        st.session_state.messages.append({
            "role": "user",
            "content": query,
        })

        st.session_state.messages.append({
            "role": "model",
            "content": output,
        })


st.title("Gemini Explorer")

# initializing the session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# displaying the conversation
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role=message["role"],
        parts=[Part.from_text(message["content"])]
    )

    if index != 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    chat.history.append(content)


# getting the user's name and defining the initial prompt
if len(st.session_state.messages) == 0:
    name = st.text_input("What's your name?")

    if name:
        initial_prompt = f"Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive. I'm {name}. Make your responese personable to me."
        llm_function(chat, initial_prompt)
        

    

#sending the query to the model
query = st.chat_input("Gemini Explorer")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)