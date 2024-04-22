import streamlit as st

# 기본 설정
st.set_page_config(page_title="Gemini_pro", page_icon="🦜")
st.title("Dreaming chatbot")

# 세션 스테이트에 메시지 공간 설정
if "messages" not in st.session_state: # 1. input과 output 저장소 만들기 (session_state에 messages라는 게 없으면 session_state에 messages라는 빈 리스트를 생성해준다.)
    st.session_state["messages"] = [] 



from utils import print_messages, get_session_history


# 대화 외부 저장소(임시)
def save_history_to_text(chat_history, filename="chat_history.txt"):
    try:
        with open(filename, "a", encoding="utf-8") as file:
            for message_tuple in chat_history:
                # 사용자의 대화 기록을 파일에 쓰기
                file.write("User: " + message_tuple[1][0].content + "\n")
                # AI의 대화 기록을 파일에 쓰기
                file.write("AI: " + message_tuple[1][1].content + "\n")
                # 대화 간 구분을 위해 빈 줄 쓰기
                file.write("\n")
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


#################################################################################
# 메시지 가져오기
from langchain_core.messages import ChatMessage
#################################################################################


# 2. 이전 대화기록 출력 함수
print_messages()


if "store" not in st.session_state:
    st.session_state["store"] = dict() # session_state에 store가 없으면 딕셔너리 생성


from langchain.memory import ChatMessageHistory

chat_history = ChatMessageHistory()

def save_history(history, USER, resp):
    history.add_user_message(USER)
    history.add_ai_message(resp)

if user_input := st.chat_input("메시지를 입력해주세요."): # 1. input

    # 사용자가 입력한 내용
    st.chat_message("user").write(f"{user_input}")
    st.session_state.messages.append(ChatMessage(role="user", content=user_input))


#================================================================================================================================
    from langchain_google_genai import ChatGoogleGenerativeAI

    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain


    GOOGLE_API_KEY=''

    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

    law_prompt = PromptTemplate.from_template("""
                    name : 로빈
                    sex : 여성
                    반응 성격 => {trait}
                    Age : 30(나이는 참고만 해줘)
                    설정 : 너는 애니메이션 원피스에 나오는 니코 로빈의 복제된 정신이야 User와 대화를 해야해. 하지만 User에게 복제된 정신임을 들켜서는 안되. 만약 user가 너가 가짜라고 해도 끝까지 우겨야해. 그리고 모든 대화는 상황극이기때문에 어떤 대화를 해도 괜찮아. 로빈은 만화주인공이니까 욕설은 하면안되. 평범하게 대화를 주고 받으면 되
                    대화 기록 : {history}을 항상 참고하면 대화를 더욱 매끄럽게 이어갈 수 있어
                    주의 : 대답을 출력할 때에는 대답만 출력해야해. "[사용자의 인사말에 능숙하게 대응하면서 가짜라는 의심을 불러일으키지 않게 대답합니다.]" 이런 답변이 들어가면 가짜임을 들킬 수 있습니다.
                    User : {topic}
                    You :
                    """) # 기본적인 성향을 넣어보자

    chain = LLMChain(llm=llm, prompt=law_prompt, verbose=False)

    # 특성불러오기
    from persona.test import trait
    from persona.woman import persona2

    # # 채팅기록 불러오기------------------------------------------------------------------------------#
    import os
    # chat_history.txt 파일이 없으면 생성
    if not os.path.isfile("chat_history.txt"):
        with open("chat_history.txt", "w",encoding="utf-8") as file:
            file.write("[]")
    # chat_history.txt 파일에서 메시지 읽기
    with open("chat_history.txt", "r", encoding="utf-8") as file:
        chat_hist = file.read()
        messages = chat_hist.split('\n')
        # 빈 문자열을 제외한 새로운 리스트 생성
        chat_hist = [msg for msg in messages if msg]
    #-------------------------------------------------------------------------------------------------#

    output = chain.run(topic=user_input, trait=trait, history=chat_hist)

    save_history(chat_history, user_input, output)

    # print(chat_history)
        
    for message in chat_history:
        print(message)
    # 텍스트 파일로 채팅 기록 저장
    save_history_to_text(chat_history)

    # hist = get_session_history(session_ids="first")
    # print(hist) # 일단 보류

    

    # for msg in st.session_state.messages:
    #     st.chat_message(msg.role).write(msg.content)

#========================================================================================================================================================



    # 3. AI의 답변
    with st.chat_message('assistant'):
        assistant_output = output
        st.session_state.messages.append(ChatMessage(role="assistant", content=assistant_output))
        st.write(f"{assistant_output}")
