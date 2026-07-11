import streamlit as st
import random
import json
import os

# データの保存ファイル
DATA_FILE = "my_words_web.json"

# 初期データ
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

# 間違えた単語の記録用
if "wrong_words" not in st.session_state:
    st.session_state.wrong_words = set()

# 現在出題中の単語
if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(list(st.session_state.words.keys()))
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.words, f, ensure_ascii=False, indent=4)

def next_question():
    st.session_state.current_word = random.choice(list(st.session_state.words.keys()))
    st.session_state.show_answer = False

# --- 画面のデザイン ---
st.set_page_config(page_title="マイ英単語帳", page_icon="📝", layout="centered")
st.title("📝 自分専用の英単語帳")

# タブ機能で画面を切り替え
tab1, tab2, tab3 = st.tabs(["🎯 クイズ", "➕ 単語を追加", "📚 単語一覧・復習"])

# --- タブ1: クイズ画面 ---
with tab1:
    st.header("単語クイズ")
    if not st.session_state.words:
        st.warning("単語帳が空っぽです。「単語を追加」タブから登録してください。")
    else:
        q_word = st.session_state.current_word
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

# --- タブ2: 単語追加画面 ---
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
        else:
            st.error("単語と意味の両方を入力してください。")

# --- タブ3: 一覧・復習画面 ---
with tab3:
    if st.session_state.wrong_words:
        st.subheader("⚠️ 今日間違えた単語（要復習）")
        for w in st.session_state.wrong_words:
            st.write(f"・**{w}** : {st.session_state.words[w]}")
    
    st.subheader("📚 登録されている単語一覧")
    for w, m in st.session_state.words.items():
        st.text(f"{w} : {m}")
