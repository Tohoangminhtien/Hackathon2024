import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import os
import io
from datetime import datetime
from chat import MultiMediaChatBot

# Dictionary of translations
TRANSLATIONS = {
    "Vietnamese": {
        "title": "Chatbot Hỗ Trợ Hình Ảnh",
        "upload_header": "Tải Lên Hình Ảnh",
        "upload_label": "Chọn hình ảnh...",
        "preview": "Xem trước",
        "chat_placeholder": "Nhập câu hỏi của bạn...",
        "clear_chat": "Xóa Lịch Sử Chat",
        "processing": "Đang xử lý...",
        "language_select": "Chọn ngôn ngữ"
    },
    "English": {
        "title": "Image-Enabled Chatbot",
        "upload_header": "Upload Image",
        "upload_label": "Choose an image...",
        "preview": "Preview",
        "chat_placeholder": "What is your question?",
        "clear_chat": "Clear Chat",
        "processing": "Processing...",
        "language_select": "Select Language"
    },
    "Korean": {
        "title": "이미지 지원 챗봇",
        "upload_header": "이미지 업로드",
        "upload_label": "이미지 선택...",
        "preview": "미리보기",
        "chat_placeholder": "질문을 입력하세요...",
        "clear_chat": "채팅 기록 삭제",
        "processing": "처리 중...",
        "language_select": "언어 선택"
    }
}


def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    if 'language' not in st.session_state:
        st.session_state.language = "English"


def save_uploaded_image(uploaded_file):
    """Save uploaded image and return the path"""
    if uploaded_file is not None:
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(uploaded_file.name)[1]
        filename = f"image_{timestamp}{file_extension}"
        filepath = os.path.join('uploads', filename)

        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return filepath
    return None


def display_message(message, is_user=True):
    """Display a message in the chat"""
    with st.chat_message("user" if is_user else "assistant"):
        if 'image' in message:
            st.image(message['image'],
                     caption=TRANSLATIONS[st.session_state.language]["preview"],
                     use_container_width=True)
        if 'text' in message:
            st.write(message['text'])


def process_user_input(user_input, image_path=None):
    """Process user input and return bot response"""
    lang = st.session_state.language

    load_dotenv('private/.env')
    open_ai_key = os.getenv("OPEN_AI_KEY")
    chat = MultiMediaChatBot(open_ai_key=open_ai_key, language=lang)

    return chat.chat(image_path, user_input)


def create_language_selector():
    """Create a container for language selection"""
    container = st.container()
    with container:
        col1, col2 = st.columns([4, 1])
        with col2:
            selected_language = st.selectbox(
                TRANSLATIONS[st.session_state.language]["language_select"],
                ["Vietnamese", "English", "Korean"],
                index=["Vietnamese", "English", "Korean"].index(
                    st.session_state.language),
                label_visibility="collapsed"
            )
            if selected_language != st.session_state.language:
                st.session_state.language = selected_language
                st.rerun()


def main():
    initialize_session_state()
    lang = st.session_state.language

    st.set_page_config(layout="wide")

    with st.sidebar:
        st.header(TRANSLATIONS[lang]["upload_header"])
        uploaded_file = st.file_uploader(
            TRANSLATIONS[lang]["upload_label"],
            type=['png', 'jpg', 'jpeg']
        )

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(
                image, caption=TRANSLATIONS[lang]["preview"], use_container_width=True)
            st.session_state.current_image = uploaded_file

    for message in st.session_state.messages:
        display_message(message, message['is_user'])

    # Create language selector
    create_language_selector()

    # Chat input
    if prompt := st.chat_input(TRANSLATIONS[lang]["chat_placeholder"]):
        image_path = None
        if st.session_state.current_image:
            image_path = save_uploaded_image(st.session_state.current_image)

            user_message = {
                'text': prompt,
                'image': image_path,
                'is_user': True
            }
            st.session_state.messages.append(user_message)
            display_message(user_message)

            st.session_state.current_image = None
        else:
            user_message = {
                'text': prompt,
                'is_user': True
            }
            st.session_state.messages.append(user_message)
            display_message(user_message)

        with st.spinner(TRANSLATIONS[lang]["processing"]):
            response = process_user_input(prompt, image_path)

        bot_message = {
            'text': response,
            'is_user': False
        }
        st.session_state.messages.append(bot_message)
        display_message(bot_message, is_user=False)

    if st.button(TRANSLATIONS[lang]["clear_chat"]):
        st.session_state.messages = []
        st.rerun()


if __name__ == "__main__":
    main()
