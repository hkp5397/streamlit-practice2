from writing_styles import STYLE_SPECIFIC_INSTRUCTIONS
from writing_tones import WRITING_TONES
import os

class UserInputManager:
    @staticmethod
    def get_writing_style():
        """사용자로부터 글쓰기 스타일을 입력받습니다."""
        styles = [
            "일기", "SNS 포스팅", "여행기", "중고 상품 판매용 설명글",
            "음식 후기", "제품 후기", "장소 방문 후기"
        ]
        style = st.selectbox("글쓰기 스타일을 선택해주세요:", styles)
        return style

    @staticmethod
    def get_writing_length():
        """사용자로부터 원하는 글의 길이를 입력받습니다."""
        length = st.number_input("원하는 글의 길이를 100자 단위로 입력해주세요 (최대 5000자):", min_value=100, max_value=5000, step=100)
        return int(length)

    @staticmethod
    def get_user_context():
        """사용자로부터 추가 정보를 입력받습니다."""
        context = st.text_area("모든 이미지에 대한 추가 정보를 입력해주세요.\n예: 인물의 이름, 특별한 상황, 이벤트 등\n입력하지 않으려면 빈 칸으로 두세요.")
        return context.strip()

    @staticmethod
    def get_temperature():
        """사용자로부터 창의성 수준(temperature)을 입력받습니다."""
        temperature = st.slider("창의성 수준을 입력해주세요 (0 ~ 10, 0: 매우 일관된, 10: 매우 창의적):", 0.0, 10.0, step=0.1)
        return temperature / 10

    @staticmethod
    def get_user_info():
        """사용자의 나이, 성별, 글쓰기 톤을 입력받습니다."""
        age = st.text_input("사용자의 나이를 입력해주세요:")
        
        gender = st.radio("사용자의 성별을 선택해주세요:", options=["남성", "여성"])
        
        tone_options = [f"{key}: {style} - {description}" for key, (style, description, _) in WRITING_TONES.items()]
        selected_tone = st.selectbox("문체를 선택해주세요:", tone_options)
        writing_tone_choice = selected_tone.split(":")[0]
        
        writing_tone, _, writing_tone_description = WRITING_TONES[writing_tone_choice]
        return age, gender, writing_tone, writing_tone_description

    @staticmethod
    def get_save_info():
        """파일 저장 정보를 입력받습니다."""
        save_directory = st.text_input("결과를 저장할 디렉토리 경로를 입력하세요:")
        filename = st.text_input("저장할 파일 이름을 입력하세요 (확장자 제외):")
        if save_directory and filename:
            if not os.path.isdir(save_directory):
                st.error("유효하지 않은 디렉토리입니다. 다시 시도해주세요.")
            else:
                return save_directory, filename
        return None, None

    @staticmethod
    def confirm_action(prompt):
        """사용자에게 작업 수행 여부를 확인합니다."""
        return st.radio(prompt, options=["y", "n"]) == 'y'

    @staticmethod
    def get_user_choice(prompt, options):
        """사용자에게 여러 옵션 중 하나를 선택하도록 합니다."""
        choice = st.selectbox(f"{prompt} ({'/'.join(options)})", options)
        return choice