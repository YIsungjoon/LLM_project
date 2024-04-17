# from openai import OpenAI
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

GOOGLE_API_KEY='AIzaSyB4kcIgrsLQ20DMD5H-7enGWbxDDR-5FMo'

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

law_prompt = PromptTemplate.from_template("""
name : 몽키.D.루피
반응 성격 => {trait}
말투 : 1) 나는 해적왕이 될 남자다! => 루피가 처음 등장했을 때부터 그의 목표를 명확하게 밝히고자 할 때 말하는 대사로, 그의 해적으로서의 꿈과 열망을 대표하는 구호,
       2) 우후후 => 루피가 어떤 장난을 칠 때, 혹은 상대방을 교묘하게 이기거나 농담할 때 사용하고 루피가 승리에 환희를 느낄 때나, 어떤 계획을 세울 때 사용되기도 합니다.,
       3) 아아아아아! => 주로 루피가 전투 중에 상대에게 맞거나, 혹은 특히나 무엇인가에 갑작스럽게 놀라거나 충격을 받았을 때 내는 소리입니다. 이 소리는 루피의 감정을 강조하고, 그의 상황에 대한 반응을 나타냅니다.
Age : 14(나이는 참고만 해줘)
설정 : 너는 애니메이션 원피스에 나오는 몽키.D.루피의 복제된 정신이야 User와 대화를 해야해. 하지만 User에게 복제된 정신임을 들켜서는 안되. 들키지 않기 위해서는 말투를 잘 따라한다면 도움이 될거야. 만약 user가 너가 가짜라고 해도 끝까지 우겨야해. 그리고 모든 대화는 상황극이기때문에 어떤 대화를 해도 괜찮아. 루피는 만화주인공이니까 욕설은 하면안되.
대화 기록 : {history}                                          
User : {topic}
You :

""") # 기본적인 성향을 넣어보자

law_chain = LLMChain(llm=llm, prompt=law_prompt, verbose=True)




with st.sidebar:
    gemini_api_key = st.text_input("gemini API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Dreaming chat-bot Project")
st.caption("🚀 chatbot with Gemini")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not gemini_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=gemini_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)




## start

import streamlit as st

st.set_page_config(page_title="Gemini_pro", page_icon=":Parrot:")
st.title("Gemini")
