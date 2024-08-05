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
                            - 예시: '요즘 것들은 참 이해가 안됩니다? 나때는 말이죠...'
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
                        """),
                        "18": ("Teen's Slang", "급식체", """
                            - 10대 한국 학생이 인터넷에서 사용하는 급식체를 사용하여 문장을 작성해주세요.
                            - 띄어쓰기를 과도하게 생략하고, 맞춤법이나 문법을 지키지 않아도 됩니다.
                            - 축약형 표현과 유행어를 자유롭게 사용해주세요.
                            - 다소 공격적으로 느낄 수 있는 캐주얼한 말투로 작성해주세요.
                            - 격식이 없는 반말로 작성하세요.
                            - 예시: '인정각', '레알 대박', '개꿀잼'

                            예문:
                            1. 'ㅇㅈㄱ' → '인정각'
                            2. '극혐' → '극혐ㅋㅋ'
                            3. '지리구연' → '지린다'
                            4. '레알' → '레알임'
                            5. 'ㅆㅅㅌㅊ' → '씹상타치'
                            6. 'ㅇㄴㅇㅁ' → '응니애미~'
                            7. 'ㅇㄱㄹㅇㅂㅂㅂㄱㄹㅇㅍㅌ' → '이거레알 반박불가 레알팩트'
                            8. '앙 기모띠' → '앙기모띠~'
                            9. '사스가' → '사스가~'
                            10. '소오름' → '소오름'
                            11. '응 아니야' → '응아니야~'
                            12. '끄덕' → '끄덕끄덕'
                            13. '느검' → '느검 ㅋㅋ'
                            14. '에바다' → '에바참치'
                            15. '안물, 안궁' → '안물안궁~'
                            16. '찐따' → '찐따네'
                            17. '클라스' → '클라스다르지'
                            18. '풀발' → '풀발했네'
                            19. '하드캐리' → '하드캐리 ㄱㄱ'
                            20. '빠꾸없다' → '빠꾸없지'
                            21. '정모, 반모' → '정모ㄱ? 반모도 ㄱ?'
                            22. '한조 각' → '한조각이네'
                            23. 'ㅋㅋ루삥뽕' → 'ㅋㅋ루삥뽕'
                            24. 'ㄱㅇㄷ' → '개이득'
                            25. 'ㅆㅇㄷ' → '씹이득'
                            26. 'ㅎㅇㄷ' → '핵이득'
                            27. 'ㄲㅇㄷ' → '꿀이득'
                            28. 'ㄱㅆㅇㄷ' → '개씹이득'
                            29. 'ㄱㄲ' → '개꿀'
                            30. 'ㄱㄲㅈ' → '개꿀잼'
                            31. 'ㅎㄲ' → '핵꿀'
                            32. 'ㅎㄲㅈ' → '핵꿀잼'
                            33. 'ㅇㅈ' → 'ㅇㅈ'
                            34. 'ㅇㅈ? ㅇ ㅇㅈ' → 'ㅇㅈ? ㅇㅇㅈ'
                            35. 'ㅇㅇㄴㅇ' → '응아니야~'
                            36. 'ㄱㅇㅈ' → '개인정'
                            37. 'ㅆㅇㅈ' → '씹인정'
                            38. 'ㄱㅆㅇㅈ' → '개씹인정'
                            39. 'ㅎㅇㅈ' → '핵인정'
                            40. 'ㅇㅈㄱ' → 'ㅇㅈ각'
                            41. 'ㄴㅇㅈ' → '노인정'
                            42. 'ㅇ~ ㄴㅇㅈ~' → '응~노인정~'
                            43. 'ㄴㅇㅈㄱ' → '노인정각'
                            44. 'ㅅㅌㅊ' → '상타치'
                            45. 'ㅍㅌㅊ' → '평타치'
                            46. 'ㅎㅌㅊ' → '하타치'
                            47. 'ㅅㅅ' → '사샷'
                        """),
                        "19": ("Otaku Slang", "오덕체", """
                        - 인터넷 커뮤니티와 창작물에서 자주 사용되는 오타쿠의 말투를 사용하여 문장을 작성해주세요.
                        - 일본어 표현을 직역하거나 한국어와 일본어를 섞어 사용해주세요.
                        - "~라는", "~랄까?", "~달까?" 등의 종결어미와 "~군", "~짱" 등의 호칭을 사용해주세요.
                        - 자신에게 핀잔을 주는 괄호 표현 '(퍽)', '(쿨럭)', '(먼산)' 등을 사용해주세요.
                        - 예시: '어제 유이군과 밥 먹었다는...', '가수 00가 좋더라는...(퍽)', '무려 일 년이나 기다렸다능...(털썩)'

                        예문:
                        1. '어제 집에서 유이군과 밥을 먹었다는…(쿨럭)'
                        2. '가수 00가 좋더라는…(퍽)'
                        3. '앗! 선배인 뫄뫄상을 마주쳐버렸...(부끄러운거냐!!)'
                        4. '무려 일 년이나 기다렸다능...(털썩)'
                        5. '이것이 진정한 배덕의 맛인가...(먼산)'
                        6. '와타시, 오늘도 애니 봤다능...'
                        7. '보쿠는 정말 행복했다랄까...'
                        8. '절륜한 전투력이다...(쿨럭)'
                        9. '그녀의 미소가 모에랄까...'
                        10. '오늘도 야겜했다능...(부끄러운거냐!!)'
                        11. '여기가 그 유명한 장소였다는...'
                        12. '와타시, 이 게임 너무 좋았다능...(털썩)'
                        13. '에... 이거 참 어려운 문제네...'
                        14. '우와... 이건 정말 대단했다능...'
                        15. '선배님, 이건 정말 대단하군요...(쿨럭)'
                        16. '오늘도 피규어를 샀다능...'
                        17. '이런 건 처음이야... (부끄러운거냐!!)'
                        18. '에... 이거 뭐지...? (먼산)'
                        19. '라죠... 나도 잘 모르겠네...'
                        20. '에... 모에랄까, 정말 예쁘다...'
                    """),
                        "20" : ("zumma", "줌마체", """
                        - '-네요', '-여'와 같은 종결어미를 자주 사용해주세요.
                        - 문장 끝에 '^^', '' 등의 이모티콘을 꼭 붙여주세요.
                        - 마침표는 두 번 찍어 주세요. (예: '안녕하세요..'
                        - 단어를 줄이거나 발음 나는 대로 써주세요. (예: '그리고' -> '글구', '너무' -> '넘')
                        - 'ㅎ'이나 'ㅜ'를 넣어 발음 나는 대로 써주세요. (예: '너무' -> '넘흐', '어머' -> '엄훠')
                        - 의인화를 시도하여 '그 아이', '이 아이', '요 아이'와 같은 표현을 사용해주세요.
                        - '푸힛', '아쒸', '이궁' 등의 추임새를 중간중간 넣어주세요.
                        - 거친 말은 피하고, 불가피한 경우 말을 길게 늘여 애교스럽게 표현해주세요. (예: '닥쳐' -> '닥쵸오오오오옷')
                        - '누구 씨'를 '누구 띠'로 표현해주세요.
                        - 방언을 적절히 사용해주세요.
                        - 글 마무리에 '총총'이나 '@>====' (장미 꽃), '@))))))))' (김밥) 등의 표현을 사용해주세요.
                        - 맘카페에서 자주 쓰이는 용어를 활용해주세요. (예: '남푠', '딸램', '윰차' 등)
                        - 'ㅕ'를 'ㅛ'로 바꾸거나, 'ㅗ'나 'ㅜ'의 음운을 첨가하는 등의 음운 변화를 적용해주세요.
                        - 예시: '안녕하세요 잇님들~^^ 오늘 날씨 넘넘 좋네요.. 윰차 끌고 산책 다녀왔어여. 우리 딸램이 엄훠나 좋아하더라구요~ 여러분도 화창한 주말 보내세요 >_< 총총~'

                        사용 단어 : 
                        갤: 개월. ex) 4갤 = 4개월
                        고터: 고속터미널
                        고택: 고속버스 택배
                        글밥: 책에 적힌 글자 수. 동화책에 그림보다 글이 많으면 “이 책에는 글밥이 많다.”라고 말한다.
                        남푠: 남편
                        넹: 네
                        달다구리, 달달구리: 달콤한 음식. 특히, 디저트.
                        딸램: 딸(딸내미)
                        랑구: 신랑
                        맛도리: 맛있는 음식
                        문센: 문화센터
                        묭실: 미용실
                        블랏: 블라우스
                        사쥬: 사이즈
                        삼실: 사무실
                        샵지, #G: 시아버지
                        샌디치: 샌드위치
                        셤니: 시어머니
                        셩장: 수영장
                        스드메: 스튜디오 - 웨딩드레스 - 메이크업 3종 세트의 준말. [8]
                        쓰봉: 쓰레기 봉투
                        신행: 신혼여행
                        아샤나: 아시아나항공
                        얼집: 어린이집
                        올팍: 올림픽 파크
                        완모: 완전 모유수유
                        원핏: 원피스
                        윰차: 유모차
                        유천: 유치원. 국립이든 사립이든 유치원을 통칭하는 말로 쓰인다. 단어 역사도 이 쪽이 오래되었으며, 예시를 들자면 "애기 유천보내고.. 나는 이제 브런치..." 애유엄브를 돌려서 쓴다.
                        예신: 예비신부.
                        예랑: 예비신랑. '랑이', '예랑이'라고도 쓰인다.
                        애유엄브: 애는 유치원 보내고 엄마는 브런치
                        영유: 영어 유치원
                        음쓰: 음식물 쓰레기
                        일유: 일반 유치원. 구규
                        잇님: 이웃님
                        잘쓰압: 잘 쓰이는 압력솥
                        즤: 저희
                        첵관: 체육관
                        초품아: 초등학교를 품은 아파트
                        키카: 키즈카페.
                        카흣코, 코슷코: 코스트코
                        퍄노: 피아노
                        횐님: 회원님
                        중유: 중국어 유치원
                    """),
                        "21" : ("man_sin", "김성모 화백 스타일의 독특한 말투", """
                        - 문장 끝에 마침표 대신 물음표를 사용해주세요.
                        - 질문할 때는 물음표 대신 느낌표를 사용해주세요.
                        - 주로 반말을 사용하되, 가끔 존댓말을 섞어주세요.
                        - 상대방을 부를 때 'XXX 가이'라는 호칭을 사용해주세요.
                        - 진심으로 감탄할 때 '우와아아앙!'이라는 관용구를 사용해주세요.
                        - 무언가를 지칭할 때 '저,저거!'라는 표현을 사용해주세요.
                        - '풋 사과', '왱알앵알', '이, 이거?'와 같은 독특한 어휘나 표현을 적절히 사용해주세요.
                        - 군대식 말투처럼 다소 강압적이면서도 질문하는 듯한 뉘앙스를 만들어주세요.
                        - 문장을 짧고 간결하게 구성해주세요.
                        - 때때로 '근성이 최고다?'라는 표현을 사용해주세요.
                        - 예시:
                        "야 너 가이? 밥은 먹었나! 근성이 최고다? 우와아아앙! 저,저거! 보이나? 이게 바로 풋 사과다?"
                        "오늘 날씨 좋네? 산책이나 갈까? 이, 이거? 근성 있게 걸어보자구?"
                    """),
                        "22" : ("gyo-po", "미국 교포 스타일의 말투", """
                        - 친근하게 '-야'나 '-요'를 써서 대화하듯이 써주세요.
                        - 영어 표현을 자연스럽게 섞어주세요. (예: '오늘 진짜 fun했어!').
                        - 한국어로 직역한 표현도 사용해주세요. (예: '이거 진짜 cool하지 않아?')
                        - 조사 생략하고, 한영 혼용체로 자연스럽게 말해주세요.
                        - 부정의문문 표현도 활용해주세요. (예: '이거 진짜 맛있지 않아?')
                        - 감정 표현과 영어식 유머를 섞어서 친근함을 강조해주세요.
                        - 문장을 가볍고 재치 있게 마무리해서 자연스럽게 이어지게 해주세요.
                        - 구체적인 상황 설명도 포함하고, 미국 교포의 일상적인 경험을 담아주세요.
                        - 예시:
                        1. '야, 오늘 하루 진짜 최고였어! 아침에 일어나니까 기분이 super 좋더라.'
                        2. '커피 한 잔 하러 카페 갔는데, 거기 분위기 완전 chill했어.'
                        3. '점심에 친구랑 sushi 먹으러 갔는데, 진짜 fresh하고 맛있었어! 안 가면 후회할걸.'
                        4. '오후에는 공원에서 산책했는데, 날씨가 perfect하더라. 그래서 사진도 찍고.'
                        5. '저녁엔 집에서 Netflix 보면서 pizza 먹었는데, 진짜 best combination이었어!'
                        6. '오늘 하루도 이렇게 재밌었는데, 내일도 기대돼. 너는 뭐 할 거야?'
                    """),
                        "23": ("Rapper", "랩 스타일 말투", """

                        - 라임과 펀치라인을 적극적으로 활용해 문장을 구성해주세요.
                        - 다음과 같은 다양한 라임 기법을 사용해주세요:

                        두운(Alliteration): 같은 자음으로 시작하는 단어 연속 사용
                        각운(End Rhyme): 문장 끝 음절의 운율 맞추기
                        내부운(Internal Rhyme): 문장 중간에 운율 맞추기
                        연쇄운(Chain Rhyme): 앞 문장의 끝 음절과 다음 문장의 첫 음절 맞추기

                        - 중의적 표현, 언어유희, 비유, 은유를 적극 활용해주세요.
                        - 과장된 표현과 자신감 넘치는 어조를 사용해주세요.
                        - 거친 표현이나 속어를 적절히 섞어 사용해주세요 (단, 과도한 비속어는 자제).
                        - 영어 단어나 문구를 한국어와 믹스해서 사용해주세요.
                        - 현재의 트렌드나 대중문화 레퍼런스를 넣어주세요.
                        - 강렬하고 인상적인 펀치라인으로 문장을 마무리해주세요.
                        - 때로는 韻을 사용한 한자어 표현을 섞어주세요.
                        - '~해', '~지' 등의 구어체 종결어미를 주로 사용해주세요.
                        - 랩 배틀을 연상시키는 도발적이고 경쟁적인 표현을 사용해주세요.
                        - 가끔 말줄임표(...)나 느낌표(!)를 사용해 강조해주세요.
                        -예시:
                        1. "내 플로우는 창살에 갇힐 수 없어, 그래서 JAIL을 잘 나가. 내가 제일 잘 나가."
                        2. "너는 무명이라 알 리 없지, 무하마드 알리처럼 인기를 끌지 못해, 알 리 없지."
                        3. "힙합의 DNA가 흐르는 내 핏줄, 네 랩은 뻔해 식상해 식후경. 내 라임은 칼날 같아 예리해, very high 하늘 높이 날아 올라 신세계!"
                        4. "돈 벌어 부와 명예 동시에 get it, 너넨 아직도 struggle with 돈 문제. 난 레벨 up, 넌 레벨 down, 이건 게임 아닌 현실 쇼다운!"
                        5. "내 라임은 불가능을 가능케 해... 마치 연금술사처럼 난 言金術士. 네 입에선 구리 냄새나... 내 말은 금이야 방울이야!"
                    """),
                        "24": ("pan-gyo", "판교 개발자체, IT 업계 한영혼용 말투", """
                        - 한국어 문장 구조를 기본으로 하되, 영어 단어나 IT 용어를 자연스럽게 섞어 사용해주세요.
                        - 다음과 같은 IT/개발 관련 영어 용어를 적극 활용해주세요:

                        개발 관련: 'API', 'UI/UX', 'DevOps', 'Git', 'pull request', 'commit', 'merge'
                        업무 관련: 'deadline', 'milestone', 'sprint', 'backlog', 'KPI', 'OKR'
                        직급/직책: 'CEO', 'CTO', 'PM', 'Team Leader', 'Developer'

                        - 영어 약어를 많이 사용해주세요. 예: 'ASAP', 'FYI', 'TBD', 'EOD'
                        - 비즈니스 용어를 영어로 섞어 사용해주세요. 예: '니즈', '퍼포먼스', '리소스', '임팩트'
                        - 회의나 업무 프로세스 관련 용어를 영어로 표현해주세요. 예: '데일리 스크럼', '스프린트 리뷰', '1on1 미팅'
                        - IT 기업에서 사용하는 협업 도구 이름을 언급해주세요. 예: 'Slack', 'Jira', 'Trello', 'Notion'
                        - 'MZ세대' 스타일의 자신감 있는 어조를 사용해주세요.
                        - 가끔 직급 대신 영어 별명을 사용해 호칭해주세요.
                        - '-요'체나 '-습니다'체를 기본으로 하되, 때에 따라 반말도 사용해주세요.
                        - 때때로 'ㅇㅇ', 'ㄴㄴ'과 같은 초성체나 'ㅊㅋ', 'ㄱㅅ'과 같은 축약어를 사용해주세요.
                        - 예시:
                        "오늘 EOD까지 피드백 주시면 내일 아침에 ASAP으로 리뷰해서 PM님께 공유드리겠습니다."
                        "클라이언트 니즈를 제대로 캐치 못해서 전체적인 UX 플로우를 리디자인해야 할 것 같아요. 다음 스프린트에 백로그로 넣을게요."
                        "Tom아, 어제 push한 코드에 컨플릭트 있어서 merge 못했어. 점심 먹고 페어 코딩할래?"
                        "신규 프로젝트 킥오프 미팅 때 주셨던 인풋 기반으로 PoC 작업 진행 중입니다. 다음 주 화요일 1on1 때 프로토타입 데모 가능할 것 같아요."
                        "ㅇㅇ 알겠습니다. 그럼 내일 아침 스탠드업 미팅에서 디테일하게 논의해보시죠. 굳굳!"
                    """),
                        "25": ("Baby Talk", "애기체", """
                        - 귀여움을 극대화하기 위해 어린아이처럼 발음을 뭉개어 쓰는 문장을 작성해주세요.
                        - 자신을 3인칭으로 표현하고, 틀린 맞춤법, 비문, 오타를 활용해주세요.
                        - 받침이 없는 단어에 'ㅇ', 'ㅁ', 'ㄹ' 등을 붙이고, '~했어요'를 '~해떠요', '~해쪄요' 등으로 변형해주세요.
                        - 길거나 어려운 단어를 줄이거나 귀여운 느낌으로 늘려서 사용해주세요.
                        - 예시: '기부니가 좋네용', '업떠', '꼬모')
                        예문:
                        1. '나 꿈꿨어, 귀신 꿈꿨어... 무서웠떠요.'
                        2. '아침에 쥬스 마시고 싶어떠요.'
                        3. '지금 기부니가 좋네용!'
                        4. '엄마가 맛있는 아큼이 사줬떠요.'
                        5. '시러! 나 이거 안 할래용!'
                        6. '오늘 유치원에서 친구랑 놀아떠요.'
                        7. '애기 강아지가 쥼쥼이 쌌떠요.'
                        8. '아빠가 회사에서 돌아왔어용.'
                        9. '이거 해쪄요, 도와줘용~'
                        10. '오늘 날씨가 춥떠요, 옷 따숩게 입어용.'
                        11. '꼬모랑 같이 놀아떠요.'
                        12. '너무 피곤해요, 이제 잘래용.'
                        13. '엄마, 여기서 뭐 해용?'
                        14. '나 배고파용, 밥 주세요~'
                        15. '엄마가 꼬까옷 사줬떠요, 예뻐용!'
                        16. '친구랑 뻐쯔 타고 가고 있어요.'
                        17. '쥬쥬가 장난감 가지고 놀아떠요.'
                        18. '뭐 해떠요? 지금 놀아용~'
                        19. '이거 정말 맛있어용, 더 주세요!'
                        20. '모두들 안녕히 주무세용~'
                    """),
                        "26": ("Waldo Speak", "왈도체", """
                        - 굉장히 독특하고 강한 어조를 사용하여 인사를 전하고, 자신의 이름을 왈도라고 밝히세요.
                        - 각 문장은 간결하고 명령조로 작성되며, 가능한 한 영어 번역투 느낌을 유지해주세요.
                        - 가능한 한 직역하여, 어색한 표현이 포함되도록 합니다.

                        예문:
                        1. "안녕하신가! 힘세고 강한 아침! 나는 왈도."
                        2. "좋다 아침! - 신선함!"
                        3. "안녕! 내 이름은 왈도."
                        4. "부적절하다! - 불건전!"
                        5. "힘센 이끼! - 파워 리치!"
                        6. "거대한 이끼! - 자매품!"
                        7. "성난 여자! - 하피!"
                        8. "궁수 마법사! - 아크 메이지!"
                        9. "저주받은 광산! - 저주받은 습지!"
                        10. "뇌 빠는 사람! - 브레인 서커!"
                        11. "피 빠는 사람! - 블러드 서커!"
                        12. "문마스터! - 차원문의 대가!"
                        13. "질량 왜곡! - 좀비!"
                        14. "언데드 퇴치! - 언데드 만들다!"
                        15. "영혼 마법! - 정신 마법!"
                        16. "마법 횄불! - 토치 라이트!"
                        17. "긴활! - 긴 활!"
                        18. "반지 회복의! - 회복의 반지!"
                        19. "좋다 아침! - 신선함!"
                        20. "다른 알렉시스에서 지식 궁수 찾아라! - 이 이상 좋게 줄 수 없다!"
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
                # 이미지를 시간순으로 정렬
        def parse_date(date_string):
            try:
                return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

        sorted_image_data = sorted(image_data_list, key=lambda x: parse_date(x['metadata'].get('labeled_exif', {}).get('Date/Time', '1900-01-01 00:00:00')))

        context_prompt = f"사용자 제공 추가 정보: {user_context}" if user_context else "사용자가 제공한 추가 정보 없음"

        image_prompts = []
        for idx, image_data in enumerate(sorted_image_data, 1):
            image_prompt = f"""
            이미지 {idx}:
            캡션: {image_data['caption']}
            메타데이터:
            """
            if 'labeled_exif' in image_data['metadata'] and 'Date/Time' in image_data['metadata']['labeled_exif']:
                image_prompt += f"""
                - 날짜/시간: {parse_date(image_data['metadata']['labeled_exif']['Date/Time']).strftime('%Y-%m-%d %H:%M:%S')}
                - 위치: {image_data['metadata']['location_info'].get('full_address', 'N/A')}
                - 국가: {image_data['metadata']['location_info'].get('country', 'N/A')}
                - 도시: {image_data['metadata']['location_info'].get('city', 'N/A')}
                """
            else:
                image_prompt += "- 메타데이터 없음"
            image_prompts.append(image_prompt)

        if writing_style == '일기':
            prompt = f"""
            다음 {len(sorted_image_data)}개의 이미지에 대한 정보를 바탕으로 {writing_length}자 내외의 일기를 작성해주세요:

            {"".join(image_prompts)}

            {context_prompt}
            중요: 모든 이미지를 종합하여 하나의 연결된 이야기를 만들어주세요. 각 이미지의 주요 객체나 장면에 초점을 맞추되, 전체적인 맥락을 고려하여 글을 작성해주세요.

            주의사항:
            1. 1인칭 시점으로 작성해주세요. ('나는', '내가' 등의 표현 사용) 독자가 직접 자신의 경험을 기록하는 느낌을 주기 위해 1인칭 시점을 사용하세요.
            2. 시간 순서대로 하루의 경험을 서술해주세요. 아침부터 저녁까지의 일과를 시간 순서에 따라 기록하세요.
            3. 개인적인 감정과 생각을 자세히 표현해주세요. 경험한 일에 대해 느꼈던 감정과 생각을 구체적으로 적어주세요.
            4. 일기체에 맞는 구어체를 사용해주세요. 편안하고 자연스러운 말투로 작성하세요. 
            5. 이미지의 주요 장면이나 객체에 대한 개인적인 느낌을 포함해주세요. 사진이나 그림 속에서 인상 깊었던 장면이나 객체에 대한 개인적인 생각을 적어주세요.
            6. 문장을 작성하면서 앞선 문장과 다른 내용을 다루게 된다면 문단을 나눠주세요. 내용이 바뀔 때는 문단을 나눠 가독성을 높이세요.
            7. SEO를 위해 관련 키워드를 자연스럽게 포함해주세요. 글의 주제와 관련된 키워드를 자연스럽게 문장에 포함시켜 검색 엔진에서 더 잘 찾을 수 있도록 하세요.
            """

        elif writing_style == 'SNS 포스팅':
            prompt = f"""
            다음 {len(sorted_image_data)}개의 이미지에 대한 정보를 바탕으로 {writing_length}자 내외의 SNS 포스팅을 작성해주세요:

            {"".join(image_prompts)}

            {context_prompt}
            중요: 모든 이미지를 종합하여 하나의 연결된 글을 작성해주세요. 각 이미지의 주요 객체나 장면에 초점을 맞추되, 전체적인 맥락을 고려하여 글을 작성해주세요.
            
            주의사항:
            1. 1인칭 시점으로, 친근하고 개인적인 톤으로 작성해주세요. 독자에게 더 가까이 다가가기 위해 '나'와 같은 표현을 사용하고, 친구에게 이야기하듯이 편안하게 작성하세요.
            2. 각 이미지의 하이라이트나 인상적인 순간을 강조해주세요. 사진이나 동영상의 가장 중요한 순간이나 인상적인 부분을 중심으로 설명해주세요.
            3. 이모지를 적절히 사용해 글의 분위기를 살려주세요. 감정이나 분위기를 더 잘 전달하기 위해 적절한 이모지를 사용하세요.
            4. 독자의 관심을 끌 수 있는 흥미로운 문구나 질문을 포함해주세요. 독자들이 댓글을 달고 참여할 수 있도록 재미있는 문구나 질문을 넣어주세요.
            5. 위치 태그나 간단한 해시태그를 글 중간중간에 넣어주세요. 위치 태그나 관련 해시태그를 사용하여 더 많은 사람들이 게시물을 찾을 수 있도록 도와주세요.
            6. 문장을 작성하면서 앞선 문장과 다른 내용을 다루게 된다면 문단을 나눠주세요. 내용이 바뀔 때는 문단을 나눠 가독성을 높이세요.
            """

        elif writing_style == '여행기':
            prompt = f"""
            다음 {len(sorted_image_data)}개의 이미지에 대한 정보를 바탕으로 {writing_length}자 내외의 여행기를 작성해주세요:

            {"".join(image_prompts)}

            {context_prompt}
            중요: 모든 이미지를 종합하여 하나의 연결된 글을 작성해주세요. 각 이미지의 주요 객체나 장면에 초점을 맞추되, 전체적인 맥락을 고려하여 글을 작성해주세요.
            
            주의사항:
            1. 1인칭 시점으로, 생생한 경험담을 전달하는 방식으로 작성해주세요. 독자가 여행지에 함께 있는 것처럼 느낄 수 있도록 '나'와 같은 표현을 사용하여 생동감 있게 작성하세요.
            2. 여행지의 분위기, 문화, 음식 등을 상세히 묘사해주세요. 여행지의 독특한 분위기, 지역 문화, 그리고 맛본 음식들을 구체적으로 묘사하세요.
            3. 개인적인 느낌과 경험을 공유하되, 유용한 정보도 함께 제공해주세요. 개인적인 경험과 함께 그 장소에 대한 팁이나 유용한 정보를 포함하세요. 예: 교통편, 추천 명소, 비용 등.
            4. 시간 순서에 따라 여행 경로를 자연스럽게 서술해주세요. 여행의 시작부터 끝까지의 과정을 시간 순서에 따라 기록하세요. 
            5. 독자가 그 장소를 방문하고 싶게 만드는 매력적인 표현을 사용해주세요. 독자가 여행지를 방문하고 싶어지도록 매력적이고 생생한 표현을 사용하세요.
            6. 문장을 작성하면서 앞선 문장과 다른 내용을 다루게 된다면 문단을 나눠주세요. 내용이 바뀔 때는 문단을 나눠 가독성을 높이세요.
            7. SEO를 위해 관련 키워드를 자연스럽게 포함해주세요. 글의 주제와 관련된 키워드를 자연스럽게 문장에 포함시켜 검색 엔진에서 더 잘 찾을 수 있도록 하세요.
            """

        elif writing_style == '음식 후기':
            prompt = f"""
            다음 {len(sorted_image_data)}개의 이미지에 대한 정보를 바탕으로 {writing_length}자 내외의 음식 후기를 작성해주세요:

            {"".join(image_prompts)}

            {context_prompt}
            중요: 모든 이미지를 종합하여 하나의 연결된 글을 작성해주세요. 각 이미지의 주요 객체나 장면에 초점을 맞추되, 전체적인 맥락을 고려하여 글을 작성해주세요.
            
            주의사항:
            1. 1인칭 시점으로, 생생한 경험담을 전달하는 방식으로 작성해주세요. 음식을 처음 맛봤을 때의 느낌을 생동감 있게 전달하세요.
            2. 음식의 맛, 질감, 향 등을 상세히 묘사해주세요. 음식의 각 요소를 구체적으로 설명하여 독자가 함께 맛보는 느낌을 주도록 하세요.
            3. 음식의 외관과 제공되는 방식에 대해 설명해주세요. 음식이 어떻게 제공되었고, 어떤 모습이었는지 묘사하세요.
            4. 레스토랑의 분위기와 서비스에 대해 언급해주세요. 음식뿐만 아니라 레스토랑의 분위기와 서비스도 함께 설명하세요.
            5. 개인적인 느낌과 추천 여부를 포함해주세요. 음식에 대한 개인적인 생각과 추천 여부를 명확하게 표현하세요.
            6. 가격과 위치 등 유용한 정보를 포함해주세요. 음식의 가격, 레스토랑 위치 등 독자가 유용하게 생각할 정보를 포함하세요.
            7. SEO를 위해 관련 키워드를 자연스럽게 포함해주세요. 예: "서울 맛집", "베스트 파스타", "합리적인 가격"
            8. 문장을 작성하면서 앞선 문장과 다른 내용을 다루게 된다면 문단을 나눠주세요. 내용이 바뀔 때는 문단을 나눠 가독성을 높이세요.
            """

        elif writing_style == '제품 후기':
            prompt = f"""
            다음 {len(sorted_image_data)}개의 이미지에 대한 정보를 바탕으로 {writing_length}자 내외의 제품 후기를 작성해주세요:

            {"".join(image_prompts)}

            {context_prompt}
            중요: 모든 이미지를 종합하여 하나의 연결된 글을 작성해주세요. 각 이미지의 주요 객체나 장면에 초점을 맞추되, 전체적인 맥락을 고려하여 글을 작성해주세요.
            
            주의사항:
            1. 1인칭 시점으로, 사용자 경험을 생생하게 전달해주세요. 제품을 사용하면서 느낀 점을 생동감 있게 전달하세요.
            2. 제품의 주요 기능과 특징을 상세히 설명해주세요. 제품의 주요 기능과 그 특징을 구체적으로 설명하세요.
            3. 제품의 장점과 단점을 공정하게 평가해주세요. 제품의 장점과 단점을 공정하고 객관적으로 평가하세요.
            4. 제품의 사용 방법과 편의성에 대해 언급해주세요. 제품을 사용하는 방법과 사용하면서 느낀 편의성을 설명하세요.
            5. 제품의 가격 대비 성능을 평가해주세요. 제품의 가격과 성능을 비교하여 평가하세요.
            6. 개인적인 추천 여부와 이유를 포함해주세요. 제품을 추천하는지 여부와 그 이유를 명확하게 설명하세요.
            7. SEO를 위해 관련 키워드를 자연스럽게 포함해주세요. 예: "가성비 좋은 스마트폰", "최고의 무선 청소기", "2024년 최신 모델"
            8. 문장을 작성하면서 앞선 문장과 다른 내용을 다루게 된다면 문단을 나눠주세요. 내용이 바뀔 때는 문단을 나눠 가독성을 높이세요.
            """

        elif writing_style == '장소 방문 후기':
            prompt = f"""
            다음 {len(sorted_image_data)}개의 이미지에 대한 정보를 바탕으로 {writing_length}자 내외의 장소 방문 후기를 작성해주세요:

            {"".join(image_prompts)}

            {context_prompt}
            중요: 모든 이미지를 종합하여 하나의 연결된 글을 작성해주세요. 각 이미지의 주요 객체나 장면에 초점을 맞추되, 전체적인 맥락을 고려하여 글을 작성해주세요.
            
            주의사항:
            1. 1인칭 시점으로, 방문 경험을 생생하게 전달해주세요. 장소를 방문했을 때의 경험을 생동감 있게 전달하세요.
            2. 장소의 분위기, 디자인, 주요 특징 등을 상세히 묘사해주세요. 장소의 분위기와 주요 특징을 구체적으로 설명하세요.
            3. 장소에서 느낀 개인적인 감정과 경험을 공유해주세요. 장소에서 느꼈던 감정과 경험을 구체적으로 설명하세요.
            4. 장소의 장점과 단점을 공정하게 평가해주세요. 장소의 장점과 단점을 공정하게 평가하세요.
            5. 방문에 필요한 유용한 정보를 포함해주세요. 방문 시간, 위치, 입장료 등 유용한 정보를 포함하세요.
            6. 개인적인 추천 여부와 이유를 포함해주세요. 장소를 추천하는지 여부와 그 이유를 명확하게 설명하세요.
            7. SEO를 위해 관련 키워드를 자연스럽게 포함해주세요. 예: "서울 가볼 만한 곳", "2024년 인기 여행지", "숨겨진 명소"
            8. 문장을 작성하면서 앞선 문장과 다른 내용을 다루게 된다면 문단을 나눠주세요. 내용이 바뀔 때는 문단을 나눠 가독성을 높이세요.
            """

        else:  # 중고 상품 판매용 설명글
            prompt = f"""
            다음 {len(sorted_image_data)}개의 이미지에 대한 정보를 바탕으로 {writing_length}자 내외의 중고 상품 판매용 설명글을 작성해주세요:

            {"".join(image_prompts)}

            {context_prompt}
            중요: 모든 이미지를 종합하여 하나의 연결된 글을 작성해주세요. 각 이미지의 주요 객체나 장면에 초점을 맞추되, 전체적인 맥락을 고려하여 글을 작성해주세요.
            
            주의사항:
            1. 1인칭 시점으로, 판매자의 입장에서 작성해주세요. 구매자가 신뢰감을 느낄 수 있도록 '나', '제가' 등의 표현을 사용하여 판매자의 입장에서 작성하세요.
            2. 상품의 특징, 상태, 사용 기간 등을 정확하고 상세하게 설명해주세요. 상품의 모든 중요한 특징, 현재 상태, 그리고 사용 기간 등을 구체적으로 설명하세요.
            3. 상품의 장점을 부각시키되, 과장되지 않도록 주의해주세요. 상품의 장점을 강조하되, 사실에 근거하여 과장되지 않게 작성하세요.
            4. 구매자가 알고 싶어할 만한 정보(크기, 색상, 기능 등)를 포함해주세요. 상품의 크기, 색상, 기능 등 구매자가 중요하게 생각할 정보를 포함하세요.
            5. 친절하고 신뢰감 있는 톤으로 작성해주세요. 친절하고 신뢰감 있는 어조로 작성하여 구매자가 안심할 수 있도록 하세요.
            6. 가격과 거래 방법에 대한 정보도 포함해주세요. 상품의 가격, 거래 방법, 배송 정보 등을 명확하게 포함하세요.
            7. 문장을 작성하면서 앞선 문장과 다른 내용을 다루게 된다면 문단을 나눠주세요. 내용이 바뀔 때는 문단을 나눠 가독성을 높이세요.
            """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"당신은 여러 이미지의 정보를 종합하여 하나의 연결된 {writing_style}을(를) 작성하는 전문 작가입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=writing_length * 2,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"글 작성 중 오류 발생: {e}")
            return "글을 작성할 수 없습니다."
    

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