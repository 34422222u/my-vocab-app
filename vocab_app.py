import streamlit as st
import random
import json
import os

DATA_FILE = "my_words_web.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.words, f, ensure_ascii=False, indent=4)

if "words" not in st.session_state:
    st.session_state.words = load_data()
if "editing_word" not in st.session_state:
    st.session_state.editing_word = None

st.title("📝 自分専用の英単語帳")
tab1, tab2, tab3 = st.tabs(["🎯 クイズ", "➕ 単語を追加", "📚 単語一覧・編集"])

with tab1:
    st.header("単語クイズ")
    if not st.session_state.words:
        st.warning("単語がありません。")
    else:
        # 日本語➔英語をデフォルトにする
        mode = st.radio("出題モード", ["日本語 ➔ 英語", "英語 ➔ 日本語"], horizontal=True)
        
        words_list = list(st.session_state.words.items())
        q_pair = random.choice(words_list)
        
        if mode == "日本語 ➔ 英語":
            st.info(f"問題: **{q_pair[1]}**")
            if st.button("答えを表示"): st.success(f"【答え】 {q_pair[0]}")
        else:
            st.info(f"問題: **{q_pair[0]}**")
            if st.button("答えを表示"): st.success(f"【答え】 {q_pair[1]}")

with tab2:
    st.header("新しい単語を追加")
    w = st.text_input("英単語")
    m = st.text_input("意味")
    if st.button("登録"):
        st.session_state.words[w] = m
        save_data()
        st.success("登録しました！")
        st.rerun()

with tab3:
    st.subheader("📚 登録されている単語一覧")
    for w, m in list(st.session_state.words.items()):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{w}** : {m}")
        with col2:
            if st.button("✏️", key=f"edit_{w}"):
                st.session_state.editing_word = w
        with col3:
            if st.button("🗑️", key=f"del_{w}"):
                del st.session_state.words[w]
                save_data()
                st.rerun()
        
        if st.session_state.editing_word == w:
            new_w = st.text_input("単語を編集", value=w, key=f"new_w_{w}")
            new_m = st.text_input("意味を編集", value=m, key=f"new_m_{w}")
            if st.button("💾 保存", key=f"save_{w}"):
                del st.session_state.words[w]
                st.session_state.words[new_w] = new_m
                save_data()
                st.session_state.editing_word = None
                st.rerun()
