from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 현재의 대화를 기억할 수 있도록
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from utils import get_session_history

GOOGLE_API_KEY='AIzaSyB4kcIgrsLQ20DMD5H-7enGWbxDDR-5FMo'

# 모델 생성
LLM = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# 3. 프롬프트 생성
# prompt = ChatPromptTemplate.from_template("""
#                                           질문에 대하여 간결하게 답변해주세요
#                                           {Question}
#                                           """)

# 4. 프롬프트 만들기
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "질문에 대하여 간결하게 답변해 주세요."),
        #대화 기록을 변수로 사용, history가 MessageHistory의 Key가 됨
        MessagesPlaceholder(variable_name="history"),
        ("human", "{Question}") # 사용자 질문 입력
    ]
)


chain = prompt | LLM

# 대화 저장
chain_with_memory = (RunnableWithMessageHistory(
                        runnable=chain, # 실행할 Runnable 객체
                        get_session_history=get_session_history, # 세션 기록을 가져오는 함수
                        input_messages_key="Question", # 사용자 질문의 키
                        history_messages_key="history" # 기록 메시지의 키
                        )
                    )

def gemini_response(user_input):
# response = chain.invoke({"Question":user_input})
    response = chain_with_memory.invoke(

        # 사용자 질문 LLM에 입력
        {"Question": user_input},
        # 세션 ID 설정 "abc123"을 전달합니다.
        config={"configurable": {"session_id":"abc123"}}
    )
    
    return response.content