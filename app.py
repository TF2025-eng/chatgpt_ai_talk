import streamlit as st
import openai

openai.api_key = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # ←ここに自分のAPIキーを入れてね

st.set_page_config(page_title="AI同士の対話シミュレーター", layout="centered")
st.title("🤖 AI vs AI 対話シミュレーター")

user_prompt = st.text_input("対話の議題を入力してください", "AIは人類を超えるべきか？")
turns = st.slider("対話のラリー回数", 1, 10, 5)

if st.button("💬 対話を開始"):
    with st.spinner("AI同士が対話中..."):
        history = []

        role_a = "あなたは理性的で冷静な哲学者です。相手の主張に丁寧に返答してください。"
        role_b = "あなたは挑発的で批判的な論者です。相手の主張に反論してください。"

        current_msg = user_prompt

        for i in range(turns):
            res_a = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": role_a},
                    {"role": "user", "content": current_msg}
                ]
            )
            reply_a = res_a["choices"][0]["message"]["content"]
            history.append(("哲学者", reply_a))

            res_b = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": role_b},
                    {"role": "user", "content": reply_a}
                ]
            )
            reply_b = res_b["choices"][0]["message"]["content"]
            history.append(("批判者", reply_b))

            current_msg = reply_b

        st.success("対話終了！")

        for speaker, line in history:
            st.markdown(f"**{speaker}**: {line}")
