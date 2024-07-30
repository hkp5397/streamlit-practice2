from openai import OpenAI

class ImageCaptionWriter:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    def get_writing_style(self):
        print("글쓰기 스타일을 선택해주세요:")
        print("1. 일기")
        print("2. SNS(인스타그램, 페이스북 등) 포스팅")
        print("3. 여행기")
        print("4. 중고 상품 판매용 설명글")
        while True:
            choice = input("선택 (1-4): ")
            if choice in ['1', '2', '3', '4']:
                return ['일기', 'SNS 포스팅', '여행기', '중고 상품 판매용 설명글'][int(choice) - 1]
            print("잘못된 선택입니다. 다시 선택해주세요.")

    def get_writing_length(self):
        while True:
            try:
                length = int(input("원하는 글의 길이를 100자 단위로 입력해주세요 (최대 5000자): "))
                if 100 <= length <= 5000 and length % 100 == 0:
                    return length
                print("100에서 5000 사이의 100의 배수를 입력해주세요.")
            except ValueError:
                print("올바른 숫자를 입력해주세요.")

    def get_user_context(self):
        print("\n사진에 대한 추가 정보를 입력해주세요.")
        print("예: 인물의 이름, 특별한 상황, 이벤트 등")
        print("입력하지 않으려면 엔터를 눌러주세요.")
        return input("추가 정보: ").strip()

    def write_story(self, caption, metadata, user_context):
        writing_style = self.get_writing_style()
        writing_length = self.get_writing_length()

        context_prompt = f"사용자 제공 추가 정보: {user_context}" if user_context else "사용자가 제공한 추가 정보 없음"

        prompt = f"""
        다음 이미지 캡션, 메타데이터, 사용자 제공 정보를 바탕으로 {writing_length}자 내외의 {writing_style}을(를) 작성해주세요:

        이미지 캡션: {caption}

        메타데이터:
        - 날짜/시간: {metadata['labeled_exif'].get('Date/Time', 'N/A')}
        - 위치: {metadata['location_info'].get('full_address', 'N/A')}
        - 국가: {metadata['location_info'].get('country', 'N/A')}
        - 도시: {metadata['location_info'].get('city', 'N/A')}

        {context_prompt}

        중요: 이미지의 중앙에 있거나 가장 큰 객체에 초점을 맞추세요. 배경이나 부수적인 요소들은 무시하고, 주요 피사체에 대해서만 글을 작성하세요.

        글에는 다음 요소를 포함해주세요:
        1. 이미지의 주요 객체(중앙 또는 가장 큰 객체)에 대한 상세한 설명
        2. 주요 객체와 관련된 촬영 시간과 장소의 분위기
        3. 주요 객체가 전달하는 감정이나 메시지
        4. 가능하다면 주요 객체와 관련된 역사적 또는 문화적 맥락
        5. 사용자가 제공한 추가 정보를 적절히 통합

        선택된 글쓰기 스타일({writing_style})에 맞게 내용과 톤을 조정해주세요. 항상 주요 객체에 초점을 맞추고, 배경이나 부수적인 요소에 대한 언급은 최소화해주세요.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"당신은 이미지의 중심 객체나 가장 큰 객체에 초점을 맞추고 사용자 제공 정보를 통합하여 {writing_style}을(를) 작성하는 전문 작가입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=writing_length * 2  # 토큰 수는 대략 글자 수의 2배로 설정
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"글 작성 중 오류 발생: {e}")
            return "글을 작성할 수 없습니다."

    def generate_hashtags(self, story):
        prompt = f"""
        다음 {len(story)}자 길이의 글을 바탕으로 5개의 관련 해시태그를 생성해주세요:

        {story[:100]}...  # 글의 처음 100자만 표시

        해시태그는 '#' 기호로 시작하고, 각각 쉼표로 구분해주세요.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 주어진 내용에 맞는 적절한 해시태그를 생성하는 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"해시태그 생성 중 오류 발생: {e}")
            return "해시태그를 생성할 수 없습니다."