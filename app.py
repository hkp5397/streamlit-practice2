import streamlit as st
from PIL import Image

# Streamlit 애플리케이션 제목
st.title("이미지 파일 업로드")

# 업로드된 이미지 파일을 저장할 리스트
uploaded_images = []

# 파일 업로드 위젯
uploaded_file = st.file_uploader("이미지 파일을 업로드하세요.", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# 파일이 업로드되었는지 확인
if uploaded_file is not None:
    for file in uploaded_file:
        # PIL을 사용하여 이미지 열기
        image = Image.open(file)
        
        # 리스트에 이미지 추가
        uploaded_images.append(image)
    
    # 업로드된 모든 이미지 표시
    for idx, image in enumerate(uploaded_images):
        st.image(image, caption=f"업로드된 이미지 {idx + 1}", use_column_width=True)
        st.write(f"이미지 {idx + 1} 크기: {image.size}")
else:
    st.write("이미지를 업로드하세요.")