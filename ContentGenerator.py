from openai import OpenAI
from datetime import datetime
from writing_styles import STYLE_SPECIFIC_INSTRUCTIONS

class ContentGenerator:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    def create_story(self, image_data_list, user_context, writing_style, writing_length, temperature, user_info):
        # 이미지 데이터 정렬
        sorted_image_data = self._sort_image_data(image_data_list)
        
        # 프롬프트 생성
        prompt = self._create_story_prompt(sorted_image_data, user_context, writing_style, writing_length, user_info)

        # OpenAI API를 사용하여 스토리 생성
        try:
            response = self._generate_openai_response(prompt, writing_length, temperature)
            return response.choices[0].message.content, user_info[2]  # writing_tone 반환
        except Exception as e:
            print(f"스토리 생성 중 오류 발생: {e}")
            return "스토리를 생성할 수 없습니다.", None

    def create_hashtags(self, story):
        # 해시태그 생성을 위한 프롬프트 작성
        prompt = self._create_hashtag_prompt(story)

        try:
            response = self._generate_openai_response(prompt, 100, 0.2)
            return response.choices[0].message.content
        except Exception as e:
            print(f"해시태그 생성 중 오류 발생: {e}")
            return "해시태그를 생성할 수 없습니다."

    def _sort_image_data(self, image_data_list):
        # 이미지 데이터를 날짜순으로 정렬
        return sorted(image_data_list, key=lambda x: self._parse_date(x['metadata'].get('labeled_exif', {}).get('DateTime', '1900-01-01 00:00:00')))

    def _parse_date(self, date_string):
        # 날짜 문자열을 datetime 객체로 변환
        try:
            return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

    def _create_story_prompt(self, sorted_image_data, user_context, writing_style, writing_length, user_info):
        # 스토리 생성을 위한 프롬프트 작성
        context_prompt = f"사용자 제공 추가 정보: {user_context}" if user_context else "사용자가 제공한 추가 정보 없음"
        age, gender, writing_tone, writing_tone_description = user_info
        
        user_info_prompt = f"""저는 {age}세 {gender}입니다. 아래 지시사항에 따라 글을 작성하세요:
            1. [{writing_tone}] 문체를 사용하세요.
            2. {writing_style} 형식으로 글을 작성하세요.
            3. 문체 특징: {writing_tone_description}
            이 특징들을 고려하여 자연스럽고 일관된 글을 작성해주세요."""

        prompt = f"""다음 정보를 바탕으로 {writing_style}을 작성해주세요:
            1. 컨텍스트: {context_prompt}
            2. 글 길이: 약 {writing_length}자
            3. 추가 정보: {user_context}
            4. 작성자 정보:
            {user_info_prompt}

            주요 지침:
            1. 제공된 이미지와 메타데이터를 기반으로 내용을 구성하세요.
            2. {writing_tone} 문체를 일관되게 유지하며, 적절한 어휘와 표현을 사용하세요.
            3. 이미지와 메타데이터의 정보를 문체에 맞게 자연스럽게 표현하세요.
            4. 전체적으로 통일성 있는 하나의 글로 작성하세요.

            이미지 정보:
            """

        for idx, image_data in enumerate(sorted_image_data, 1):
            prompt += self._create_image_prompt(idx, image_data)

        prompt += f"""{STYLE_SPECIFIC_INSTRUCTIONS[writing_style]}

        중요: 모든 이미지를 종합하여 하나의 연결된 글을 작성해주세요. 각 이미지의 주요 객체나 장면에 초점을 맞추되, 전체적인 맥락을 고려하여 글을 작성해주세요.
        """
        return prompt

    def _create_image_prompt(self, idx, image_data):
        # 개별 이미지에 대한 프롬프트 생성
        image_prompt = f"""
        이미지 {idx}:
        캡션: {image_data['caption']}
        메타데이터:
        """
        if 'labeled_exif' in image_data['metadata'] and 'Date/Time' in image_data['metadata']['labeled_exif']:
            image_prompt += f"""
            - 날짜/시간: {self._parse_date(image_data['metadata']['labeled_exif']['Date/Time']).strftime('%Y-%m-%d %H:%M:%S')}
            - 위치: {image_data['metadata']['location_info'].get('full_address', 'N/A')}
            - 국가: {image_data['metadata']['location_info'].get('country', 'N/A')}
            - 도시: {image_data['metadata']['location_info'].get('city', 'N/A')}
            """
        else:
            image_prompt += "- 메타데이터 없음"
        return image_prompt

    def _create_hashtag_prompt(self, story):
        # 해시태그 생성을 위한 프롬프트 작성
        return f"""
        다음 {len(story)}자 길이의 글을 바탕으로 5개의 관련 해시태그를 생성해주세요:

        {story[:100]}...  # 글의 처음 100자만 표시

        해시태그는 '#' 기호로 시작하고, 각각 쉼표로 구분해주세요.
        """

    def _generate_openai_response(self, prompt, max_tokens, temperature):
        # OpenAI API를 사용하여 응답 생성
        return self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 여러 이미지의 정보를 종합하여 하나의 연결된 글을 작성하는 전문 작가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )