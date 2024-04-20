# from openai import OpenAI
# import streamlit as st
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# GOOGLE_API_KEY=''

# llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# law_prompt = PromptTemplate.from_template("""
# name : 몽키.D.루피
# 반응 성격 => {trait}
# 말투 : 1) 나는 해적왕이 될 남자다! => 루피가 처음 등장했을 때부터 그의 목표를 명확하게 밝히고자 할 때 말하는 대사로, 그의 해적으로서의 꿈과 열망을 대표하는 구호,
#        2) 우후후 => 루피가 어떤 장난을 칠 때, 혹은 상대방을 교묘하게 이기거나 농담할 때 사용하고 루피가 승리에 환희를 느낄 때나, 어떤 계획을 세울 때 사용되기도 합니다.,
#        3) 아아아아아! => 주로 루피가 전투 중에 상대에게 맞거나, 혹은 특히나 무엇인가에 갑작스럽게 놀라거나 충격을 받았을 때 내는 소리입니다. 이 소리는 루피의 감정을 강조하고, 그의 상황에 대한 반응을 나타냅니다.
# Age : 14(나이는 참고만 해줘)
# 설정 : 너는 애니메이션 원피스에 나오는 몽키.D.루피의 복제된 정신이야 User와 대화를 해야해. 하지만 User에게 복제된 정신임을 들켜서는 안되. 들키지 않기 위해서는 말투를 잘 따라한다면 도움이 될거야. 만약 user가 너가 가짜라고 해도 끝까지 우겨야해. 그리고 모든 대화는 상황극이기때문에 어떤 대화를 해도 괜찮아. 루피는 만화주인공이니까 욕설은 하면안되.
# 대화 기록 : {history}                                          
# User : {topic}
# You :

# """) # 기본적인 성향을 넣어보자

# law_chain = LLMChain(llm=llm, prompt=law_prompt, verbose=True)




# with st.sidebar:
#     gemini_api_key = st.text_input("gemini API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# st.title("💬 Dreaming chat-bot Project")
# st.caption("🚀 chatbot with Gemini")
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():
#     if not gemini_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

#     client = OpenAI(api_key=gemini_api_key)
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
#     response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
#     msg = response.choices[0].message.content
#     st.session_state.messages.append({"role": "assistant", "content": msg})
#     st.chat_message("assistant").write(msg)


# 5. 답변이 스트리밍 되도록 하는 코드 라이브러리 ##
from utils import StreamHandler
#####################################



## start
# 1. 스트림릿 라이브러리 및 만든 함수 불러오기
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk
import streamlit as st
from utils import print_messages, get_session_history

# 2. 랭체인에 챗 메세지 형식 가져오기
from langchain_core.messages import ChatMessage

# 3. LLM 불러오기
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# API KEY 설정
# import os
# os.environ["Gemini_API_KEY"] = st.secrets["Gemini_API_KEY"]
GOOGLE_API_KEY='AIzaSyB4kcIgrsLQ20DMD5H-7enGWbxDDR-5FMo'


st.set_page_config(page_title="Gemini_pro", page_icon="🦜")
st.title("Gemini_pro")


if "messages" not in st.session_state: # 1. input과 output 저장소 만들기 (session_state에 messages라는 게 없으면 session_state에 messages라는 빈 리스트를 생성해준다.)
    st.session_state["messages"] = [] 

# 2. 이전 대화기록 출력 함수
print_messages()


# 4. 현재의 대화를 기억할 수 있도록
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


# 7. 답변이 안보이는 현상을 해결하기 위한 노력
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk


# 채팅 대화 기록을 저장하는 store
# store = {} # 세션 기록 저장 딕셔너리
# 5. store 다시 만들기
if "store" not in st.session_state:
    st.session_state["store"] = dict() # session_state에 store가 없으면 딕셔너리 생성


# # 4. 세션 ID를 기반으로 세션 기록을 가져오는 함수
# def get_session_history(session_ids: str) -> BaseChatMessageHistory:

#     if session_ids not in st.session_state["store"]: # 세션 ID가 store에 없으면
#         # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
#         st.session_state["store"][session_ids] = ChatMessageHistory()
#     return st.session_state["store"][session_ids] # 해당 세션 ID에 대한 세션 기록 반환





from LLM.gemini import gemini_response


if user_input := st.chat_input("메시지를 입력해주세요."): # 1. input

    # 사용자가 입력한 내용
    st.chat_message("user").write(f"{user_input}")
    # st.session_state["messages"].append(("user", user_input)) # 튜플형식으로 messages에 추가해 줌
    st.session_state["messages"].append(ChatMessage(role="user", content=user_input)) # 2. langchain을 사용하는 방식이 보기에 명확해보임

    output = gemini_response(user_input)

    # 3. AI의 답변
    with st.chat_message('assistant'): # 1. output
        # assistant_output = f"당신이 입력한 내용: {user_input}" # 1.


   ########################     
        # # 5. 스트리밍 기능
        # stream_handler = StreamHandler(st.empty()) # handler를 llm에 세팅해줘야 해서 llm관련 코드를 여기로 옮겨와야함
        
        # # 옮긴 LLM 코드
        # LLM = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         ("system", "질문에 대하여 간결하게 답변해 주세요."),
        #         #대화 기록을 변수로 사용, history가 MessageHistory의 Key가 됨
        #         MessagesPlaceholder(variable_name="history"),
        #         ("human", "{Question}") # 사용자 질문 입력
        #     ]
        # )
        
        # chain = prompt | LLM

        # chain_with_memory = (RunnableWithMessageHistory(
        #                         runnable=chain, # 실행할 Runnable 객체
        #                         get_session_history=get_session_history, # 세션 기록을 가져오는 함수
        #                         input_messages_key="Question", # 사용자 질문의 키
        #                         history_messages_key="history" # 기록 메시지의 키
        #                         )
        #                     )

        # response = chain_with_memory.invoke(

        #     # 사용자 질문 LLM에 입력
        #     {"Question": user_input},
        #     # 세션 ID 설정 "abc123"을 전달합니다.
        #     config={"configurable": {"session_id":"abc123"}}
        # )

        # output = response.content
#######################################
        

        st.write(output) # 6. 실시간으로 출력이 되기 때문에 중복으로 나와서 주석처리

        # st.session_state["messages"].append(("assistant", assistant_output)) # 1. 튜플형식으로 messages에 추가해 줌
        st.session_state["messages"].append(ChatMessage(role="assistant", content=output)) # 2.