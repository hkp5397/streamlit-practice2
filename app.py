# main.py

import os
from ImageProcessor import ImageProcessor
from ImageCaptionWriter import ImageCaptionWriter

def main():
    openai_api_key = input("OpenAI API 키를 입력하세요: ")
    if not openai_api_key:
        print("OpenAI API 키가 입력되지 않았습니다.")
        return

    image_paths = []
    while True:
        image_path = input("이미지 파일 경로를 입력하세요 (종료하려면 빈 줄 입력): ")
        if not image_path:
            break
        if os.path.exists(image_path):
            image_paths.append(image_path)
        else:
            print(f"파일을 찾을 수 없습니다: {image_path}")

    if not image_paths:
        print("처리할 이미지가 없습니다.")
        return

    processor = ImageProcessor(openai_api_key)
    writer = ImageCaptionWriter(openai_api_key)
    
    for image_path in image_paths:
        result = processor.process_image(image_path)
        print(f"\n이미지: {result['image_path']}")
        print("메타데이터:")
        print(f"  EXIF 데이터: {result['metadata']['exif_data']}")
        print(f"  라벨링된 EXIF: {result['metadata']['labeled_exif']}")
        print(f"  위치 정보: {result['metadata']['location_info']}")
        print(f"생성된 캡션: {result['caption']}")

        # 사용자로부터 추가 정보 입력 받기
        user_context = writer.get_user_context()

        # 이야기 작성
        story = writer.write_story(result['caption'], result['metadata'], user_context)
        print("\n생성된 글:")
        print(story)
        print(f"\n글자 수: {len(story)}")

        # 해시태그 생성
        hashtags = writer.generate_hashtags(story)
        print("\n생성된 해시태그:")
        print(hashtags)

if __name__ == "__main__":
    main()