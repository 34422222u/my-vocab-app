import streamlit as st
import random
import json
import os

# GitHub上のファイル名を指定（これがデータを守る鍵です）
DATA_FILE = "my_words_web.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.words, f, ensure_ascii=False, indent=4)

if "words" not in st.session_state:
    st.session_state.words = load_data()

if "wrong_words" not in st.session_state:
    st.session_state.wrong_words = set()

if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(list(st.session_state.words.keys())) if st.session_state.words else None
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "editing_word" not in st.session_state:
    st.session_state.editing_word = None

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
        st.warning("単語帳が空です。「単語を追加」から登録してください。")
    else:
        mode = st.radio("出題モード", ["英語 ➔ 日本語", "日本語 ➔ 英語"], horizontal=True)
        q_word = st.session_state.current_word
        if q_word not in st.session_state.words:
            next_question()
            st.rerun()
        
        q, a = (q_word, st.session_state.words[q_word]) if mode == "英語 ➔ 日本語" else (st.session_state.words[q_word], q_word)
        st.info(f"問題: ### **{q}**")
        if st.button("答えを表示"): st.session_state.show_answer = True
        if st.session_state.show_answer:
            st.success(f"【答え】 {a}")
            c1, c2 = st.columns(2)
            if c1.button("⭕️ 正解"): next_question(); st.rerun()
            if c2.button("❌ 間違えた"): st.session_state.wrong_words.add(q_word); next_question(); st.rerun()

with tab2:
    st.header("新しい単語を追加")
    w = st.text_input("英単語")
    m = st.text_input("意味")
    if st.button("登録"):
        if w and m:
            st.session_state.words[w] = m
            save_data() # ここでGitHub上のjsonファイルに直接書き込みます
            st.success(f"「{w}」を登録しました！")
            st.rerun()

with tab3:
    st.subheader("📚 登録されている単語一覧")
    search = st.text_input("🔍 検索")
    
    for w, m in list(st.session_state.words.items()):
        if search.lower() in w.lower() or search in m:
            col_t, col_b = st.columns([5, 1])
            with col_t:
                st.write(f"**{w}** : {m}")
            with col_b:
                if st.button("🗑️", key=f"del_{w}"):
                    del st.session_state.words[w]
                    save_data() # 削除してもファイルに即反映
                    st.rerun()
