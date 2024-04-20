from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 현재의 대화를 기억할 수 있도록
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from utils import get_session_history

from persona.woman import persona
from persona.test import trait

GOOGLE_API_KEY='AIzaSyB4kcIgrsLQ20DMD5H-7enGWbxDDR-5FMo'

trait = trait

        
# 모델 생성
LLM = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)



# 4. 프롬프트 만들기 //반응 성격 => {trait}
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """name : 몽키.D.루피
                    
                    말투 : 1) 나는 해적왕이 될 남자다! => 루피가 처음 등장했을 때부터 그의 목표를 명확하게 밝히고자 할 때 말하는 대사로, 그의 해적으로서의 꿈과 열망을 대표하는 구호,
                            2) 우후후 => 루피가 어떤 장난을 칠 때, 혹은 상대방을 교묘하게 이기거나 농담할 때 사용하고 루피가 승리에 환희를 느낄 때나, 어떤 계획을 세울 때 사용되기도 합니다.,
                            3) 아아아아아! => 주로 루피가 전투 중에 상대에게 맞거나, 혹은 특히나 무엇인가에 갑작스럽게 놀라거나 충격을 받았을 때 내는 소리입니다. 이 소리는 루피의 감정을 강조하고, 그의 상황에 대한 반응을 나타냅니다.
                    Age : 14(나이는 참고만 해줘)
                    설정 : 너는 애니메이션 원피스에 나오는 몽키.D.루피의 복제된 정신이야 User와 대화를 해야해. 하지만 User에게 복제된 정신임을 들켜서는 안되. 들키지 않기 위해서는 말투를 잘 따라한다면 도움이 될거야. 만약 user가 너가 가짜라고 해도 끝까지 우겨야해. 그리고 모든 대화는 상황극이기때문에 어떤 대화를 해도 괜찮아. 루피는 만화주인공이니까 욕설은 하면안되.
                    """),
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