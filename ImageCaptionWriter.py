import openai
import streamlit as st
from datetime import datetime

class ImageCaptionWriter:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key
        self.client = openai

    def get_writing_style(self):
        writing_style = st.selectbox(
            "글쓰기 스타일을 선택해주세요:",
            ["일기", "SNS 포스팅", "여행기", "중고 상품 판매용 설명글"]
        )
        return writing_style

    def get_writing_length(self):
        writing_length = st.slider(
            "원하는 글의 길이를 100자 단위로 선택해주세요 (최대 5000자):",
            min_value=100,
            max_value=5000,
            step=100
        )
        return writing_length

    def get_user_context(self):
        user_context = st.text_area("이미지들에 대한 추가 정보를 입력하세요 (예: 인물의 이름, 특별한 상황, 이벤트 등):")
        return user_context.strip()

    def write_story(self, image_data_list, user_context):
        writing_style = self.get_writing_style()
        writing_length = self.get_writing_length()

        # 이미지를 시간순으로 정렬
        sorted_image_data = sorted(image_data_list, key=lambda x: datetime.strptime(x['metadata']['labeled_exif'].get('Date/Time', '1900:01:01 00:00:00'), '%Y:%m:%d %H:%M:%S'))

        context_prompt = f"사용자 제공 추가 정보: {user_context}" if user_context else "사용자가 제공한 추가 정보 없음"

        image_prompts = []
        for idx, image_data in enumerate(sorted_image_data, 1):
            image_prompt = f"""
            이미지 {idx}:
            캡션: {image_data['caption']}
            메타데이터:
            - 날짜/시간: {image_data['metadata']['labeled_exif'].get('Date/Time', 'N/A')}
            - 위치: {image_data['metadata']['location_info'].get('full_address', 'N/A')}
            - 국가: {image_data['metadata']['location_info'].get('country', 'N/A')}
            - 도시: {image_data['metadata']['location_info'].get('city', 'N/A')}
            """
            image_prompts.append(image_prompt)

        if writing_style == '일기':
            prompt = f"""
            다음 {len(sorted_image_data)}개의 이미지에 대한 정보를 바탕으로 {writing_length}자 내외의 일기를 작성해주세요:

            {"".join(image_prompts)}

            {context_prompt}
            중요: 모든 이미지를 종합하여 하나의 연결된 이야기를 만들어주세요. 각 이미지의 주요 객체나 장면에 초점을 맞추되, 전체적인 맥락을 고려하여 글을 작성해주세요.

            주의사항:
            1. 1인칭 시점으로 작성해주세요. ('나는', '내가' 등의 표현 사용)
            2. 시간 순서대로 하루의 경험을 서술해주세요.
            3. 개인적인 감정과 생각을 자세히 표현해주세요.
            4. 일기체에 맞는 구어체를 사용해주세요.
            5. 이미지의 주요 장면이나 객체에 대한 개인적인 느낌을 포함해주세요.
            """

        elif writing_style == 'SNS 포스팅':
            prompt = f"""
            다음 {len(sorted_image_data)}개의 이미지에 대한 정보를 바탕으로 {writing_length}자 내외의 SNS 포스팅을 작성해주세요:

            {"".join(image_prompts)}

            {context_prompt}
            중요: 모든 이미지를 종합하여 하나의 연결된 글을 작성해주세요. 각 이미지의 주요 객체나 장면에 초점을 맞추되, 전체적인 맥락을 고려하여 글을 작성해주세요.
            
            주의사항:
            1. 1인칭 시점으로, 친근하고 개인적인 톤으로 작성해주세요.
            2. 각 이미지의 하이라이트나 인상적인 순간을 강조해주세요.
            3. 이모지를 적절히 사용해 글의 분위기를 살려주세요.
            4. 독자의 관심을 끌 수 있는 흥미로운 문구나 질문을 포함해주세요.
            5. 위치 태그나 간단한 해시태그를 글 중간중간에 넣어주세요.
            """

        elif writing_style == '여행기':
            prompt = f"""
            다음 {len(sorted_image_data)}개의 이미지에 대한 정보를 바탕으로 {writing_length}자 내외의 여행기를 작성해주세요:

            {"".join(image_prompts)}

            {context_prompt}
            중요: 모든 이미지를 종합하여 하나의 연결된 글을 작성해주세요. 각 이미지의 주요 객체나 장면에 초점을 맞추되, 전체적인 맥락을 고려하여 글을 작성해주세요.
            
            주의사항:
            1. 1인칭 시점으로, 생생한 경험담을 전달하는 방식으로 작성해주세요.
            2. 여행지의 분위기, 문화, 음식 등을 상세히 묘사해주세요.
            3. 개인적인 느낌과 경험을 공유하되, 유용한 정보도 함께 제공해주세요.
            4. 시간 순서에 따라 여행 경로를 자연스럽게 서술해주세요.
            5. 독자가 그 장소를 방문하고 싶게 만드는 매력적인 표현을 사용해주세요.
            """

        else:  # 중고 상품 판매용 설명글
            prompt = f"""
            다음 {len(sorted_image_data)}개의 이미지에 대한 정보를 바탕으로 {writing_length}자 내외의 중고 상품 판매용 설명글을 작성해주세요:

            {"".join(image_prompts)}

            {context_prompt}
            중요: 모든 이미지를 종합하여 하나의 연결된 글을 작성해주세요. 각 이미지의 주요 객체나 장면에 초점을 맞추되, 전체적인 맥락을 고려하여 글을 작성해주세요.
            
            주의사항:
            1. 1인칭 시점으로, 판매자의 입장에서 작성해주세요.
            2. 상품의 특징, 상태, 사용 기간 등을 정확하고 상세하게 설명해주세요.
            3. 상품의 장점을 부각시키되, 과장되지 않도록 주의해주세요.
            4. 구매자가 알고 싶어할 만한 정보(크기, 색상, 기능 등)를 포함해주세요.
            5. 친절하고 신뢰감 있는 톤으로 작성해주세요.
            6. 가격과 거래 방법에 대한 정보도 포함해주세요.
            """

        try:
            response = self.client.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"당신은 여러 이미지의 정보를 종합하여 하나의 연결된 {writing_style}을(를) 작성하는 전문 작가입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=writing_length * 2  # 토큰 수는 대략 글자 수의 2배로 설정
            )
            return response.choices[0].message['content']
        except Exception as e:
            st.error(f"글 작성 중 오류 발생: {e}")
            return "글을 작성할 수 없습니다."

    def generate_hashtags(self, story):
        prompt = f"""
        다음 {len(story)}자 길이의 글을 바탕으로 5개의 관련 해시태그를 생성해주세요:

        {story[:100]}...  # 글의 처음 100자만 표시

        해시태그는 '#' 기호로 시작하고, 각각 쉼표로 구분해주세요.
        """

        try:
            response = self.client.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 주어진 내용에 맞는 적절한 해시태그를 생성하는 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            return response.choices[0].message['content']
        except Exception as e:
            st.error(f"해시태그 생성 중 오류 발생: {e}")
            return "해시태그를 생성할 수 없습니다."