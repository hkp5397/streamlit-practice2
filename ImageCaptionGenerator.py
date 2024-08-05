from openai import OpenAI
import base64
from PIL import Image
import io

class ImageCaptionGenerator:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    def generate_caption(self, image_path, metadata):
        try:
            base64_image = self._process_image(image_path)
            prompt = self._create_prompt(metadata)
            return self._get_caption_from_api(prompt, base64_image)
        except Exception as e:
            print(f"캡션 생성 중 오류 발생: {e}")
            return "캡션을 생성할 수 없습니다."
        
    def _process_image(self, image_path):
        with Image.open(image_path) as img:
            img = self._convert_to_rgb(img)
            img = self._resize_image(img)
            return self._image_to_base64(img)
        
    def _convert_to_rgb(self, img):
        if img.mode == 'RGBA':
            return img.convert('RGB')
        return img
    
    def _resize_image(self, img):
        max_size = (512, 512)  # OpenAI API 권장 최대 크기
        img.thumbnail(max_size, Image.LANCZOS)
        return img

    def _image_to_base64(self, img):
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

    def _create_prompt(self, metadata):
        return f"""이 이미지를 설명해주세요. 다음 메타데이터도 참고하세요:
        날짜/시간: {metadata['labeled_exif'].get('Date/Time', 'N/A')}
        위치: {metadata['location_info'].get('full_address', 'N/A')}
        """

    def _get_caption_from_api(self, prompt, base64_image):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # 비전 모델 사용
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