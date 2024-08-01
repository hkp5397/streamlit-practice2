from openai import OpenAI
import base64

class ImageCaptionGenerator:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    def generate_caption(self, image_path, metadata):
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            prompt = f"""이 이미지를 설명해주세요. 다음 메타데이터도 참고하세요:
            날짜/시간: {metadata['labeled_exif'].get('Date/Time', 'N/A')}
            위치: {metadata['location_info'].get('full_address', 'N/A')}
            """

            response = self.client.chat.completions.create(
                model="gpt-4",  # 모델명 변경
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ],
                    }
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"캡션 생성 중 오류 발생: {e}")
            return "캡션을 생성할 수 없습니다."