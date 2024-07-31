# main.py

import os
import streamlit as st
from ImageProcessor import ImageProcessor
from ImageCaptionWriter import ImageCaptionWriter

def main():
    st.title("이미지 캡션 작성기")

    openai_api_key = st.text_input("OpenAI API 키를 입력하세요:")
    if not openai_api_key:
        st.warning("OpenAI API 키를 입력해주세요.")
        return

    uploaded_files = st.file_uploader("이미지 파일을 업로드하세요 (여러 개 가능):", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

    if not uploaded_files:
        st.warning("처리할 이미지를 업로드해주세요.")
        return

    processor = ImageProcessor(openai_api_key)
    writer = ImageCaptionWriter(openai_api_key)

    for uploaded_file in uploaded_files:
        image_path = os.path.join("/tmp", uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        result = processor.process_image(image_path)
        st.image(image_path, caption=result['caption'])
        st.write("메타데이터:")
        st.json({
            "EXIF 데이터": result['metadata']['exif_data'],
            "라벨링된 EXIF": result['metadata']['labeled_exif'],
            "위치 정보": result['metadata']['location_info']
        })
        
    # 사용자로부터 모든 이미지에 대한 추가 정보 입력 받기
    user_context = st.text_area("이미지들에 대한 추가 정보를 입력하세요:")
    
    # 모든 이미지 정보를 종합하여 하나의 이야기 작성
    if st.button("이야기 생성"):
        story = writer.write_story(image_data_list, user_context)
        st.subheader("생성된 글:")
        st.write(story)
        st.write(f"글자 수: {len(story)}")

        hashtags = writer.generate_hashtags(story)
        st.write("생성된 해시태그:")
        st.write(hashtags)

if __name__ == "__main__":
    main()