import streamlit as st


# 챗메시지 모두 출력해주기
# def print_messages():
#     if "messages" in st.session_state and len(st.session_state["messages"]) > 0: # 만약 messages에 값이 있다면 챗메시지에 출력하시오.
#         for role, message in st.session_state["messages"]:
#             st.chat_message(role).write(message)

# 챗메시지 모두 출력해주기(랭체인 라이브러리 사용)
def print_messages():
    if "messages" in st.session_state and len(st.session_state["messages"]) > 0: # 만약 messages에 값이 있다면 챗메시지에 출력하시오.
        for lang_message in st.session_state["messages"]:
            st.chat_message(lang_message.role).write(lang_message.content)



# 4. 세션 ID를 기반으로 세션 기록을 가져오는 함수
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

def get_session_history(session_ids: str) -> BaseChatMessageHistory:

    if session_ids not in st.session_state["store"]: # 세션 ID가 store에 없으면
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        st.session_state["store"][session_ids] = ChatMessageHistory()
    return st.session_state["store"][session_ids] # 해당 세션 ID에 대한 세션 기록 반환



# 답변이 스트리밍되도록 하는 코드
from langchain_core.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)