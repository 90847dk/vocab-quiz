import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="영어 단어 시험기", layout="wide")
st.title("📘 영어 단어 시험 웹사이트")
st.write("엑셀 파일을 업로드하면 랜덤 단어 시험을 볼 수 있어요!")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요 (첫 줄: 영어, 둘째 줄: 한국어)", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = ['English', 'Korean']

    st.markdown("---")
    with st.expander("📄 전체 단어 목록 보기"):
        st.dataframe(df)

    st.markdown("---")
    st.subheader("⚙️ 시험 설정")

    total_words = len(df)
    eng_count = st.slider("영어 → 한국어 문제 개수", min_value=0, max_value=total_words, value=20)
    kor_count = st.slider("한국어 → 영어 문제 개수", min_value=0, max_value=total_words - eng_count, value=10)

    if eng_count + kor_count > total_words:
        st.warning("선택한 문제 수가 전체 단어 수보다 많습니다!")
    else:
        quiz = df.sample(n=eng_count + kor_count).reset_index(drop=True)
        eng_to_kor = quiz.iloc[:eng_count]
        kor_to_eng = quiz.iloc[eng_count:]

        st.markdown("---")
        st.subheader("1️⃣ 영어 → 한국어")

        # 영어 → 한국어
eng_answers = []
for i, row in eng_to_kor.iterrows():
    key = f"eng_{i}"
    if key not in st.session_state:
        st.session_state[key] = ""
    input_value = st.text_input(f"{i+1}. {row['English']}", value=st.session_state[key], key=key)
    eng_answers.append((input_value.strip(), row['Korean'].strip()))

# 한국어 → 영어
kor_answers = []
for i, row in kor_to_eng.iterrows():
    key = f"kor_{i}"
    if key not in st.session_state:
        st.session_state[key] = ""
    input_value = st.text_input(f"{i+1+eng_count}. {row['Korean']}", value=st.session_state[key], key=key)
    kor_answers.append((input_value.strip().lower(), row['English'].strip().lower()))

        if st.button("✅ 채점하기"):
            score = 0
            st.subheader("📋 채점 결과")

            for i, (user, correct) in enumerate(eng_answers):
                if user == correct:
                    st.write(f"{i+1}. ✅ 정답")
                    score += 1
                else:
                    st.write(f"{i+1}. ❌ 오답 (정답: {correct})")

            for i, (user, correct) in enumerate(kor_answers):
                if user == correct:
                    st.write(f"{i+1+eng_count}. ✅ 정답")
                    score += 1
                else:
                    st.write(f"{i+1+eng_count}. ❌ 오답 (정답: {correct})")

            st.success(f"🎉 총 점수: {score}/{eng_count + kor_count}")
