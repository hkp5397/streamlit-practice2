# use_image_metadata_processor.py

from ImageMetadataProcessor import ImageMetadataProcessor

def main():
    image_path = input("이미지 파일의 경로를 입력하세요: ")
    processor = ImageMetadataProcessor(image_path)
    processor.process()
    processor.print_results()

if __name__ == "__main__":
    main()