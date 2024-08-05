from writing_styles import STYLE_SPECIFIC_INSTRUCTIONS
from writing_tones import WRITING_TONES
from pathlib import Path
import streamlit as st
import os

def get_downloads_folder():
    """사용자의 다운로드 폴더 경로를 반환합니다."""
    home = Path.home()
    downloads_folder = home / "Downloads"
    return downloads_folder

class UserInputManager:
    @staticmethod
    def get_writing_style():
        styles = [
            "일기", "SNS 포스팅", "여행기", "중고 상품 판매용 설명글",
            "음식 후기", "제품 후기", "장소 방문 후기"
        ]
        style = st.selectbox("글쓰기 스타일을 선택해주세요:", styles, key="writing_style")
        return style

    @staticmethod
    def get_writing_length():
        length = st.number_input("원하는 글의 길이를 100자 단위로 입력해주세요 (최대 5000자):", min_value=100, max_value=5000, step=100, key="writing_length")
        return int(length)

    @staticmethod
    def get_user_context():
        context = st.text_area("모든 이미지에 대한 추가 정보를 입력해주세요.\n예: 인물의 이름, 특별한 상황, 이벤트 등\n입력하지 않으려면 빈 칸으로 두세요.", key="user_context")
        return context.strip()

    @staticmethod
    def get_temperature():
        temperature = st.slider("창의성 수준을 입력해주세요 (0 ~ 10, 0: 매우 일관된, 10: 매우 창의적):", 0.0, 10.0, step=0.1, key="temperature")
        return temperature / 10

    @staticmethod
    def get_user_info():
        age = st.text_input("사용자의 나이를 입력해주세요:", key="user_age")
        
        gender = st.radio("사용자의 성별을 선택해주세요:", options=["남성", "여성"], key="user_gender")
        
        tone_options = [f"{key}: {style} - {description}" for key, (style, description, _) in WRITING_TONES.items()]
        selected_tone = st.selectbox("문체를 선택해주세요:", tone_options, key="user_tone")
        writing_tone_choice = selected_tone.split(":")[0]
        
        writing_tone, _, writing_tone_description = WRITING_TONES[writing_tone_choice]
        return age, gender, writing_tone, writing_tone_description

    @staticmethod
    def get_save_info():
        """파일 저장 정보를 입력받습니다."""
        save_directory = get_downloads_folder()
        filename = st.text_input("저장할 파일 이름을 입력하세요 (확장자 제외):", key="save_filename")
        
        if save_directory and filename:
            if os.path.isdir(save_directory):
                return os.path.join(save_directory, f"{filename}.txt")
            else:
                st.error("유효하지 않은 디렉토리입니다. 다시 시도해주세요.")
        return ""

    @staticmethod
    def confirm_action(prompt):
        return st.radio(prompt, options=["y", "n"], key=prompt) == 'y'

    @staticmethod
    def get_user_choice(prompt, options):
        choice = st.selectbox(f"{prompt} ({'/'.join(options)})", options, key=prompt)
        return choice