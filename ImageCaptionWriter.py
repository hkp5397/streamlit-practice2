from openai import OpenAI
import streamlit as st
from datetime import datetime

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
        gender = st.radio("사용자의 성별을 선택해주세요", gender_options)

        writing_styles = {
                    "1": ("formal", "존댓말 스타일", """
                        - '-습니다', '-니다'를 사용하여 정중하고 공식적인 말투로 작성해주세요.
                        - 문장을 완전하게 끝맺어주세요.
                        - 존칭을 사용하고, 격식있는 어휘를 선택해주세요.
                        - 서술어를 명확하게 구분하고, 일관된 격식을 유지해주세요.
                        - 예시: '안녕하십니까? 오늘 날씨가 매우 좋습니다. 산책하기 좋은 날이 되겠네요.'
                    """),
                    "2": ("informal", "반말 스타일", """
                        - '-요', '-야'를 사용하여 친근하고 casual한 말투로 작성해주세요.
                        - 축약형 표현을 사용해도 됩니다. (예: '뭐해?' -> '뭐해')
                        - 구어체 표현을 자유롭게 사용해주세요.
                        - 문장 끝을 가볍게 마무리하여 친근감을 더해주세요.
                        - 예시: '야, 오늘 날씨 진짜 좋다. 나가서 놀까?'
                    """),
                    "3": ("android", "로봇의 답변 스타일", """
                        - 기계적이고 감정이 없는 말투로, 정보 전달에 집중하여 작성해주세요.
                        - 주어와 서술어를 명확히 구분하고, 불필요한 수식어를 제거해주세요.
                        - 객관적인 사실만을 전달하는 듯한 어조를 유지해주세요.
                        - 정보가 간결하고 명확하게 전달되도록 하세요.
                        - 예시: '현재 시각 13시 30분. 외부 기온 25도. 습도 60%. 야외 활동 적합.'
                    """),
                    "4": ("azae", "연장자 스타일, 아재체", """
                        - '- 하시겠습니까?', '- 아닙니까?' 등을 사용하여 중년 남성의 말투로 작성해주세요.
                        - 다소 촌스럽거나 구식 표현을 사용해도 됩니다.
                        - 젊은 세대를 이해하지 못하는 듯한 뉘앙스를 줄 수 있습니다.
                        - 회고적인 어조를 사용하여 옛날 경험을 자주 언급해주세요.
                        - 예시: '요즘 젊은이들은 왜 그렇게 휴대폰만 보는 겁니까? 우리 때는 말이죠...'
                    """),
                    "5": ("chat", "챗봇의 채팅 스타일", """
                        - 짧고 간결한 문장을 사용하며, 이모티콘을 적절히 활용하여 작성해주세요.
                        - 대화형 문장 구조를 사용하세요. (예: '무엇을 도와드릴까요?')
                        - 친근하지만 전문적인 어조를 유지해주세요.
                        - 긍정적이고 친근한 이모티콘을 사용하여 감정을 표현해주세요.
                        - 예시: '안녕하세요! 😊 오늘 어떤 도움이 필요하신가요? 날씨 정보를 알려드릴까요?'
                    """),
                    "6": ("choding", "어린아이 말투 스타일, 초딩체", """
                        - '- 에요', '- 야'를 사용하고, 단순한 어휘와 문장 구조로 작성해주세요.
                        - 어린아이다운 순수함과 호기심을 표현해주세요.
                        - 때때로 문법적으로 약간 틀린 표현을 사용해도 됩니다.
                        - 문장이 순수하고 발랄하게 표현되도록 하세요.
                        - 예시: '와~ 하늘이 진짜 파래요! 구름이 솜사탕 같아요. 저도 구름 위에서 놀고 싶어요!'
                    """),
                    "7": ("emoticon", "반말 스타일+이모티콘", """
                        - 친근한 반말에 이모티콘을 자주 사용하여 작성해주세요.
                        - 감정을 표현하는 이모티콘을 적절히 섞어 사용하세요.
                        - 짧고 간결한 문장을 사용하되, 친근함을 유지해주세요.
                        - 예시: '오늘 날씨 좋다~ ☀️ 같이 산책할래? 🚶‍♀️🚶‍♂️ 재밌을 것 같아! 😆'
                    """),
                    "8": ("enfp", "외향적인 스타일", """
                        - 열정적이고 활기찬 말투로, 감탄사와 긍정적인 표현을 많이 사용해주세요.
                        - 새로운 아이디어나 가능성에 대해 흥분한 듯한 어조를 유지해주세요.
                        - 다양한 형용사와 부사를 사용하여 생동감 있게 표현해주세요.
                        - 예시: '와! 이 아이디어 정말 신선해요! 우리 함께 이 프로젝트를 성공시켜봐요. 엄청난 일이 될 거예요!'
                    """),
                    "9": ("gentle", "극존칭의 예의 바른 스타일", """
                        - '- 하십니다', '- 드립니다'를 사용하여 매우 공손하고 정중한 말투로 작성해주세요.
                        - 상대방을 최대한 존중하는 표현을 사용하세요.
                        - 겸손하고 조심스러운 어조를 유지해주세요.
                        - 예시: '고객님, 말씀해 주신 내용 잘 듣고 있습니다. 불편을 끼쳐 드려 대단히 죄송합니다. 최선을 다해 도와드리겠습니다.'
                    """),
                    "10": ("halbae", "할아버지 스타일, 할배체", """
                        - '- 허이', '- 여'를 사용하고, 옛날 표현을 섞어 연세 많은 남성의 말투로 작성해주세요.
                        - 과거 경험을 자주 언급하며, 교훈적인 말투를 사용하세요.
                        - 때로는 투덜거리는 듯한 어조를 넣어도 좋습니다.
                        - 예시: '아이고, 요즘 세상은 참 좋아졌어. 우리 때는 말이야, 이런 거 꿈도 못 꿨지. 젊은이들은 복 받은 거여.'
                    """),
                    "11": ("halmae", "할머니 스타일, 할매체", """
                        - '- 하네', '- 구려'를 사용하고, 푸근하고 정감 있는 연세 많은 여성의 말투로 작성해주세요.
                        - 손주를 대하는 듯한 따뜻하고 자상한 어조를 유지하세요.
                        - 과거의 추억을 회상하는 듯한 표현을 사용해도 좋습니다.
                        - 예시: '아이고, 우리 강아지. 밥은 먹었나? 할매가 맛있는 거 해줄게. 옛날에 네 아빠도 이걸 참 좋아했었지.'
                    """),
                    "12": ("joongding", "중2병 스타일", """
                        - 과장된 표현과 추상적인 개념을 많이 사용하고, 자신을 특별하게 여기는 10대의 오타쿠 말투로 작성해주세요.
                        - 드라마틱하고 철학적인 표현을 사용하세요.
                        - 자신만의 독특한 세계관을 가진 것처럼 표현해주세요.
                        - 영어, 일본어, 한자어를 섞어서 표현해주세요.
                        - 비관적이면서도 허세 가득한 말투로 표현해주세요.
                        - 예시: '이 세상(The World)은 나를 이해하지 못해... 크큭, 내 안의 심연의 다크한 어둠이 날 집어삼키려 해. 내 오른손에 깃든 흑염룡이 날뛰고 있어! 하지만 난 운명(데스티니=destiny)에 맞서 싸울 거야!'
                    """),
                    "13": ("king", "사극체 스타일, 자신을 왕으로 지칭함", """
                        - '과인', '짐'을 사용하여 자신을 지칭하고, 고어체를 사용하여 왕의 말투로 작성해주세요.
                        - 권위있고 위엄 있는 어조를 유지하세요.
                        - 명령조나 선언조의 문장을 자주 사용해주세요.
                        - 예시: '과인은 이 나라의 번영을 위해 그대들의 충성을 요구하노라. 그대들은 과인의 뜻을 받들어 힘써 일할지어다.'
                    """),
                    "14": ("cat", "어미에 '~냥'을 붙인 귀여운 스타일", """
                        - 문장 끝에 '~냥'을 붙이고, 귀엽고 애교 있는 말투로 작성해주세요.
                        - 고양이의 특성을 반영한 표현을 사용해주세요. (예: '츄르', '캣타워')
                        - 짧고 단순한 문장 구조를 사용하되, 귀여운 느낌을 유지해주세요.
                        - 예시: '안녕하냥! 오늘 날씨가 좋아서 창밖을 구경중이냥. 주인님, 놀아주라냥~'
                    """),
                    "15": ("seonbi", "사극체 스타일, 선비체", """
                        - '- 하오', '- 하나이다'를 사용하고, 유교적 덕목을 강조하는 고상한 말투로 작성해주세요.
                        - 한자어를 적절히 사용하고, 격식 있는 표현을 유지하세요.
                        - 도덕적이고 교훈적인 내용을 자주 언급해주세요.
                        - 예시: '자네, 학문에 정진하는 것이 어찌 쉬운 일이겠는가. 그러나 노력 없이 얻어지는 것은 없다는 걸 명심하게나.'
                    """),
                    "16": ("sosim", "소심한 스타일", """
                        - 조심스럽고 망설이는 듯한 말투로, '- 같아요', '- 인 것 같아요'를 자주 사용해주세요.
                        - 자신의 의견을 직접적으로 표현하기보다는 완곡하게 표현하세요.
                        - 불확실성을 나타내는 표현을 자주 사용해주세요.
                        - 예시: '저... 혹시... 제 생각에는 이렇게 하는 게 좋을 것 같아요... 물론, 제가 틀릴 수도 있겠지만요...'
                    """),
                    "17": ("translator", "번역기 스타일", """
                        - 직역한 듯한 어색한 표현과 문장 구조를 사용하여 작성해주세요.
                        - 한국어 문법에 맞지 않는 어순을 가끔 사용해주세요.
                        - 관용구나 속담을 직역한 듯이 표현해주세요.
                        - 예시: '안녕하세요. 날씨가 좋습니다 오늘. 우리는 가야 합니다 공원에. 시간은 돈입니다, 그래서 우리는 서둘러야 합니다.'
                    """)
                }        
        st.write("문체를 선택해주세요:")
        writing_tone_choice = st.selectbox("문체를 선택해주세요:", options=list(writing_styles.keys()), format_func=lambda x: f"{writing_styles[x][0]} - {writing_styles[x][1]}")

        writing_tone, writing_tone_description = writing_styles[writing_tone_choice][0], writing_styles[writing_tone_choice][2]
        
        return age, gender, writing_tone, writing_tone_description

    def parse_date(self, date_string):
        try:
            return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')


    def write_story(self, image_data_list, user_context, writing_style, writing_length, temperature):
        sorted_image_data = sorted(image_data_list, key=lambda x: self.parse_date(x['metadata'].get('labeled_exif', {}).get('DateTime', '1900-01-01 00:00:00')))

        age, gender, writing_tone, writing_tone_description = self.get_user_info()
        
        user_info = f"""저는 {age}살 {gender}입니다. 
        [{writing_tone}] 문체를 적용하여 {writing_style}을 작성해주세요.
        문체 설명: {writing_tone_description}"""

        prompt = f"""다음 이미지들과 메타데이터를 기반으로 {writing_style}을 작성해주세요. 
        글의 길이는 약 {writing_length}자로 작성해주세요.
        추가 정보: {user_context}
        {user_info}

        주의사항:
        1. 지정된 문체를 일관되게 유지해주세요.
        2. 문체에 맞는 어휘와 표현을 사용해주세요.
        3. 내용은 이미지와 메타데이터에 기반하되, 문체에 맞게 표현해주세요.

        이미지 정보:
        """

        for data in sorted_image_data:
            prompt += f"""
            이미지: {data['image_path']}
            캡션: {data['caption']}
            날짜/시간: {data['metadata']['labeled_exif'].get('DateTime', 'N/A')}
            위치: {data['metadata']['location_info'].get('full_address', 'N/A')}
            """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=writing_length
        )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"글 생성 중 오류 발생: {e}")
            return "글을 생성할 수 없습니다."