import logging
from typing import Dict, Any
from ImageMetadataProcessor import ImageMetadataProcessor
from ImageCaptionGenerator import ImageCaptionGenerator

class ImageProcessor:
    # ImageProcessor 클래스 초기화
    # :param openai_api_key : OpenAI API 키
    def __init__(self, openai_api_key: str):
        self.metadata_processor = ImageMetadataProcessor()
        self.caption_generator = ImageCaptionGenerator(openai_api_key)
        self.logger = self._setup_logger()


    # 이미지 처리 및 메타데이터, 캡션 생성
    # :param image_path: 처리할 이미지의 경로
    # :return: 이미지 경로, 메타데이터, 캡션을 포함한 딕셔너리
    def process_image(self, image_path: str) -> Dict[str, Any]:
        try:
            self.logger.info(f"이미지 처리 시작: {image_path}")
            metadata = self._process_metadata(image_path)
            caption = self._generate_caption(image_path, metadata)
            return self._construct_result(image_path, metadata, caption)
        except Exception as e:
            self.logger.error(f"이미지 {image_path} 처리 중 오류 발생: {str(e)}")
            raise

        
    # 이미지의 메타데이터를 추출
    # :param image_path: 메타데이터를 추출할 이미지의 경로
    # :return: 추출된 메타데이터
    def _process_metadata(self, image_path: str) -> Dict[str, Any]:
        self.logger.info(f"{image_path}에서 메타데이터 추출 중")
        return self.metadata_processor.process(image_path)
        
    # 이미지에 대한 캡션을 생성합니다.       
    # :param image_path: 캡션을 생성할 이미지의 경로
    # :param metadata: 이미지의 메타데이터
    # :return: 생성된 캡션
    def _generate_caption(self, image_path: str, metadata: Dict[str, Any]) -> str:
        self.logger.info(f"{image_path}에 대한 캡션 생성 중")
        return self.caption_generator.generate_caption(image_path, metadata)
        
    # 처리 결과 구성
    #:param image_path: 처리된 이미지의 경로
    #:param metadata: 추출된 메타데이터
    #:param caption: 생성된 캡션
    #:return: 처리 결과를 포함한 딕셔너리
    def _construct_result(self, image_path: str, metadata: Dict[str, Any], caption: str) -> Dict[str, Any]:

        return {
            'image_path': image_path,
            'metadata': metadata,
            'caption': caption
        }

    # 로깅 설정 초기화
    # :return: 설정된 로거 객체
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger