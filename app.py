import streamlit as st
from PIL import Image
from ImageMetadataProcessor import ImageMetadataProcessor

# Streamlit 애플리케이션 제목
st.title("이미지 파일 메타데이터 추출")

# 파일 업로드 위젯
uploaded_files = st.file_uploader("이미지 파일을 업로드하세요.", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)

        # 임시 파일로 저장하여 ImageMetadataProcessor에 전달
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 메타데이터 처리기 생성 및 처리
        processor = ImageMetadataProcessor(uploaded_file.name)
        processor.process()

        # 결과 출력
        st.write("추출된 EXIF 데이터:", processor.exif_data)
        st.write("라벨링된 EXIF 데이터:", processor.labeled_exif)
        if processor.location_info:
            st.write("위치 정보:", processor.location_info)
        else:
            st.write("위치 정보를 가져올 수 없습니다.")