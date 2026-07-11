import streamlit as st
import random
import json
import os

DATA_FILE = "my_words_web.json"

if "words" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            st.session_state.words = json.load(f)
    else:
        st.session_state.words = {
            "vulnerable": "脆弱な、傷つきやすい",
            "indispensable": "不可欠な",
            "ambiguous": "曖昧な",
            "alleviate": "軽減する"
        }

if "wrong_words" not in st.session_state:
    st.session_state.wrong_words = set()

if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(list(st.session_state.words.keys()))
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.words, f, ensure_ascii=False, indent=4)

def next_question():
    if st.session_state.words:
        st.session_state.current_word = random.choice(list(st.session_state.words.keys()))
    else:
        st.session_state.current_word = None
    st.session_state.show_answer = False

st.set_page_config(page_title="マイ英単語帳", page_icon="📝", layout="centered")
st.title("📝 自分専用の英単語帳")

tab1, tab2, tab3 = st.tabs(["🎯 クイズ", "➕ 単語を追加", "📚 単語一覧・復習"])

with tab1:
    st.header("単語クイズ")
    if not st.session_state.words:
        st.warning("単語帳が空っぽです。「単語を追加」タブから登録してください。")
    else:
        q_word = st.session_state.current_word
        if q_word not in st.session_state.words:
            next_question()
            st.rerun()
            
        st.info(f"この単語の意味は？\n\n### **{q_word}**")
        
        if st.button("答えを表示する", type="primary"):
            st.session_state.show_answer = True
            
        if st.session_state.show_answer:
            st.success(f"【答え】 {st.session_state.words[q_word]}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⭕️ 正解！"):
                    next_question()
                    st.rerun()
            with col2:
                if st.button("❌ 間違えた..."):
                    st.session_state.wrong_words.add(q_word)
                    next_question()
                    st.rerun()

with tab2:
    st.header("新しい単語を追加")
    new_word = st.text_input("英単語を入力")
    new_meaning = st.text_input("意味を入力")
    if st.button("単語帳に登録"):
        if new_word and new_meaning:
            st.session_state.words[new_word] = new_meaning
            save_data()
            st.success(f"「{new_word}」を追加しました！")
            next_question()
            st.rerun()
        else:
            st.error("単語と意味の両方を入力してください。")

with tab3:
    if st.session_state.wrong_words:
        st.subheader("⚠️ 今日間違えた単語（要復習）")
        for w in list(st.session_state.wrong_words):
            if w in st.session_state.words:
                st.write(f"・**{w}** : {st.session_state.words[w]}")
            else:
                st.session_state.wrong_words.discard(w)
    
    st.subheader("📚 登録されている単語一覧")
    
    if not st.session_state.words:
        st.caption("登録されている単語はありません。")
    else:
        for w, m in list(st.session_state.words.items()):
            col1, col2, col3 = st.columns([3, 3, 1])
            with col1:
                st.write(f"**{w}**")
            with col2:
                st.write(m)
            with col3:
                if st.button("削除", key=f"delete_{w}"):
                    del st.session_state.words[w]
                    if w in st.session_state.wrong_words:
                        st.session_state.wrong_words.remove(w)
                    save_data()
                    next_question()
                    st.rerun()
