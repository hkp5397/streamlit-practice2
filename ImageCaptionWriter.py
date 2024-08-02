from openai import OpenAI
import streamlit as st

class ImageCaptionWriter:
    def __init__(self, openai_api_key):
        # openai.api_key = openai_api_key
        self.client = OpenAI(api_key=openai_api_key)

    def get_user_context(self):
        return st.text_area("사용자 입력 (선택 사항):", "")

    def get_writing_style(self):
        style = ["1. 일기", "2. SNS(인스타그램, 페이스북 등) 포스팅", "3. 여행기", "4. 중고 상품 판매용 설명글", "5. 음식 후기", "6. 제품 후기", "7. 장소 방문 후기"]
        selected_style = st.selectbox("글쓰기 스타일을 선택하세요:", style)
        return selected_style
    
    def get_writing_length(self):
        return st.slider("원하는 글 길이를 선택하세요:", min_value=100, max_value=1000, value=300, step=50)

    def get_temperature(self):
        return st.slider("생성된 글의 창의성 정도를 선택하세요 (0.0 - 1.0):", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    def get_user_info(self):
        age = st.number_input("사용자의 나이를 입력해주세요: ", min_value=0, max_value=120, step=1)
        gender_options = ["남성", "여성"]
        gender_choice = st.radio("사용자의 성별을 선택해주세요", gender_options)
        return age, gender_choice


    def write_story(self, image_data_list, user_context, writing_style, writing_length, temperature, age, gender):
        messages = self._create_messages(image_data_list, user_context, writing_style, age, gender)
        response = self.client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=writing_length,
            temperature=temperature
        )
        story = response.choices[0].message.content.strip()
        return story

    def _create_messages(self, image_data_list, user_context, writing_style):
        messages = [
            {"role": "system", "content": f"다음 이미지를 기반으로 {writing_style} 스타일로 글을 작성하세요:"}
        ]
        for data in image_data_list:
            messages.append({"role": "user", "content": f"이미지 경로: {data['image_path']}\n이미지에 대한 캡션: {data['caption']}\n메타데이터: {data.get('metadata', '')}"})
        if user_context:
            messages.append({"role": "user", "content": f"추가 사용자 입력: {user_context}"})
        return messages

    def generate_hashtags(self, story):
        response = self.client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "다음 글을 기반으로 해시태그를 생성하세요:"},
                {"role": "user", "content": story},
            ],
            max_tokens=50,
            temperature=0.5,
        )
        hashtags = response.choices[0].message.content.strip()
        return hashtags