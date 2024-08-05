import os
import streamlit as st
from ImageProcessor import ImageProcessor
from ContentGenerator import ContentGenerator
from UserInputManager import UserInputManager
from datetime import datetime
from pathlib import Path
import io

def get_downloads_folder():
    home = Path.home()
    downloads_folder = home / "Downloads"
    return downloads_folder

def get_image_paths():
    uploaded_files = st.file_uploader("이미지를 업로드하세요", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

    if uploaded_files:
        if not os.path.exists("temp"):
            os.makedirs("temp")

    image_paths = []
    for uploaded_file in uploaded_files:
        image_path = os.path.join("temp", uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        image_paths.append(image_path)
    return image_paths

def process_images(processor, image_paths):
    image_data_list = []
    for image_path in image_paths:
        try:
            result = processor.process_image(image_path)
            image_data_list.append(result)
            print_image_info(result, image_path)
        except Exception as e:
            st.error(f"예상치 못한 오류 발생: {e} - 이미지 처리를 건너뜁니다.")
    return image_data_list

def print_image_info(result, image_path):
    st.image(image_path, caption=os.path.basename(image_path))
    st.write("메타데이터:")
    if 'metadata' in result and 'labeled_exif' in result['metadata']:
        st.write(f"  라벨링된 EXIF: {result['metadata']['labeled_exif']}")
        st.write(f"  위치 정보: {result['metadata']['location_info']}")
    else:
        st.write("  메타데이터가 없습니다.")
    st.write(f"생성된 캡션: {result['caption']}")

def save_captions(image_data_list):
    save_path = UserInputManager.get_save_info()
    if save_path:
        content = "\n".join([f"{os.path.basename(data['image_path'])}({data['image_path']})\n"
                            f"이미지에 대한 캡션: {data['caption']}\n" for data in image_data_list])
        st.download_button(
            label="캡션 저장",
            data=content,
            file_name=save_path,
            mime="text/plain"
        )
    else:
        st.error("파일 저장 경로가 유효하지 않습니다. 다시 시도해주세요.")

def generate_story(writer, image_data_list):
    user_context = UserInputManager.get_user_context()
    writing_style = UserInputManager.get_writing_style()
    writing_length = UserInputManager.get_writing_length()
    temperature = UserInputManager.get_temperature()
    user_info = UserInputManager.get_user_info()

    start_time = datetime.now()
    story, writing_tone = writer.create_story(image_data_list, user_context, writing_style, writing_length, temperature, user_info)
    end_time = datetime.now()

    st.write(f"\n모든 이미지에 대한 추가 정보 => {user_context}")
    st.write(f"\n글 생성 스타일 => {writing_style}")
    st.write(f"\n글의 문체 => {writing_tone}")
    st.write(f"\n글 생성 길이 => {writing_length}")
    st.write(f"\n글 생성 temperature 파라미터 => {temperature}")
    st.write(f"\n글 생성 시간 => {end_time - start_time}")
    st.write("\n생성된 글:")
    st.write(story)
    st.write(f"\n글자 수: {len(story)}")

    return story

def generate_hashtags(writer, story):
    if UserInputManager.confirm_action("해시태그를 생성하시겠습니까?"):
        hashtags = writer.create_hashtags(story)
        st.write("\n생성된 해시태그:")
        st.write(hashtags)
        return hashtags
    return ""

def save_results(story, hashtags, image_paths):
    if UserInputManager.confirm_action("결과를 파일에 저장하시겠습니까?"):
        save_path = UserInputManager.get_save_info()
        if save_path:
            content = create_content_for_saving(story, hashtags, image_paths)
            if content.strip():
                st.download_button(
                    label="파일 저장하기",
                    data=content,
                    file_name=save_path,
                    mime="text/plain"
                )
            else:
                st.write("저장할 내용이 없습니다. 파일 저장을 건너뜁니다.")
        else:
            st.error("파일 저장 경로가 유효하지 않습니다. 다시 시도해주세요.")

def create_content_for_saving(story, hashtags, image_paths):
    content = ""
    if story:
        content += f"글:\n{story}\n\n"
    if hashtags:
        content += f"해시태그:\n{hashtags}\n\n"
    if image_paths:
        image_info = "\n".join([f"{path}\n파일명:\n{os.path.basename(path)}" for path in image_paths])
        content += f"이미지 경로:\n{image_info}"
    return content

def main():
    st.title("이미지 처리 및 캡션 생성기")

    openai_api_key = st.text_input("OpenAI API 키를 입력하세요:", type="password")
    if not openai_api_key:
        st.warning("OpenAI API 키를 입력해주세요.")
        return

    image_paths = get_image_paths()
    if not image_paths:
        st.write("처리할 이미지가 없습니다.")
        return

    processor = ImageProcessor(openai_api_key)
    writer = ContentGenerator(openai_api_key)
    
    image_data_list = process_images(processor, image_paths)

    choice = st.radio("캡션만 저장하시겠습니까? 아니면 글을 생성하시겠습니까?", ("캡션", "글"))

    if choice == '캡션':
        save_captions(image_data_list)
    elif choice == "글":
        story = generate_story(writer, image_data_list)
        hashtags = generate_hashtags(writer, story)
        save_results(story, hashtags, image_paths)
    else:
        st.warning("잘못된 선택입니다. 프로그램을 종료합니다.")

if __name__ == "__main__":
    main()