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
    quiz = df.sample(n=30).reset_index(drop=True)
    eng_to_kor = quiz.iloc[:20]
    kor_to_eng = quiz.iloc[20:]

    st.subheader("1️⃣ 영어 → 한국어")
    eng_answers = []
    for i, row in eng_to_kor.iterrows():
        key = f"eng_{i}"
        default = st.session_state.get(key, "")
        input_value = st.text_input(f"{i+1}. {row['English']}", value=default, key=key)
        st.session_state[key] = input_value
        eng_answers.append((input_value.strip(), row['Korean'].strip()))

    st.subheader("2️⃣ 한국어 → 영어")
    kor_answers = []
    for i, row in kor_to_eng.iterrows():
        key = f"kor_{i}"
        default = st.session_state.get(key, "")
        input_value = st.text_input(f"{i+21}. {row['Korean']}", value=default, key=key)
        st.session_state[key] = input_value
        kor_answers.append((input_value.strip().lower(), row['English'].strip().lower()))

    if st.button("채점하기"):
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
                st.write(f"{i+21}. ✅ 정답")
                score += 1
            else:
                st.write(f"{i+21}. ❌ 오답 (정답: {correct})")

        st.success(f"🎉 총 점수: {score}/30")
