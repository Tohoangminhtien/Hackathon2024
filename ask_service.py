import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import os
import io
from datetime import datetime
from chat import MedicineChatBot

# Dictionary of translations
TRANSLATIONS = {
    "Vietnamese": {
        "title": "Bot Hỗ Trợ Thuốc 🏥",
        "medicine_info": "Thông tin thuốc",
        "medicine_input": "Nhập thông tin thuốc của bạn",
        "chat_placeholder": "Hỏi về thuốc của bạn...",
        "thinking": "Đang suy nghĩ...",
        "clear_chat": "Xóa lịch sử chat",
        "api_key_missing": "Vui lòng nhập OpenAI API Key!",
        "language_select": "Chọn ngôn ngữ"
    },
    "English": {
        "title": "Medicine Chat Bot 🏥",
        "medicine_info": "Medicine Information",
        "medicine_input": "Enter your medicine information",
        "chat_placeholder": "Ask about your medicine...",
        "thinking": "Thinking...",
        "clear_chat": "Clear chat history",
        "api_key_missing": "Please enter your OpenAI API Key!",
        "language_select": "Select Language"
    },
    "Korean": {
        "title": "의약품 채팅봇 🏥",
        "medicine_info": "의약품 정보",
        "medicine_input": "의약품 정보를 입력하세요",
        "chat_placeholder": "의약품에 대해 물어보세요...",
        "thinking": "생각 중...",
        "clear_chat": "채팅 기록 지우기",
        "api_key_missing": "OpenAI API 키를 입력해주세요!",
        "language_select": "언어 선택"
    }
}


def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'language' not in st.session_state:
        st.session_state.language = "English"


def main():
    initialize_session_state()
    lang = st.session_state.language

    # Language selector in container at top-right
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col2:
            selected_language = st.selectbox(
                TRANSLATIONS[lang]["language_select"],
                ["Vietnamese", "English", "Korean"],
                index=["Vietnamese", "English", "Korean"].index(
                    st.session_state.language),
                key="language_selector"
            )
            if selected_language != st.session_state.language:
                st.session_state.language = selected_language
                st.rerun()

    st.title(TRANSLATIONS[lang]["title"])

    # Sidebar for medicine context
    with st.sidebar:
        st.header(TRANSLATIONS[lang]["medicine_info"])

        # Medicine information
        medicine_data = [
            {"Name": "VACOOM Ez 40(K21;K27)", "Usage": "3/day"},
            {"Name": "Pharbacol", "Usage": "3/day"},
            {"Name": "Bromhexin Actavis 8mg", "Usage": "3/day"},
        ]

        # Display medicine info as a table
        st.table(medicine_data)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input(TRANSLATIONS[lang]["chat_placeholder"]):

        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get bot response
        load_dotenv('private/.env')
        open_ai_key = os.getenv("OPEN_AI_KEY")
        bot = MedicineChatBot(open_ai_key=open_ai_key)

        with st.chat_message("assistant"):
            with st.spinner(TRANSLATIONS[lang]["thinking"]):
                context = "VACOOM Ez 40(K21;K27)-Usage 3/day Pharbacol-Usage 3/day Bromhexin Actavis 8mg-Usage 3/day"
                response = bot.chat(
                    question=prompt, context=context, language=lang)
                st.write(response)

        # Add bot response to chat
        st.session_state.messages.append(
            {"role": "assistant", "content": response})

    # Clear chat button
    if st.button(TRANSLATIONS[lang]["clear_chat"]):
        st.session_state.messages = []
        st.rerun()


if __name__ == "__main__":
    main()
