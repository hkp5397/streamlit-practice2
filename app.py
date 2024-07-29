import streamlit as st
from PIL import Image

# Streamlit 애플리케이션 제목
st.title("이미지 파일 업로드")

# 파일 업로드 위젯
uploaded_file = st.file_uploader("이미지 파일을 업로드하세요.", type=["jpg", "jpeg", "png"])

# 파일이 업로드되었는지 확인
if uploaded_file is not None:
    # PIL을 사용하여 이미지 열기
    image = Image.open(uploaded_file)
    
    # 이미지 표시
    st.image(image, caption="업로드된 이미지", use_column_width=True)
    
    # 이미지 크기 출력
    st.write("이미지 크기: ", image.size)
else:
    st.write("이미지를 업로드하세요.")