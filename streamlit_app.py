import streamlit as st
from ux_writer import UXwriter
import pandas as pd
import json

def boolean_to_emoji(value):
    return '✅' if value else '❌'


st.title("✍🏻 UX writer")
st.write(
    "SqueezeBits의 UX writer입니다."
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
option = st.selectbox(
    "UX 라이팅 매뉴얼을 선택하세요",
    ["select", "Toss", "Squeezebits"],
    index=0
)
is_English = st.toggle("Only English")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")

elif option == "select":
    st.info("Please select your manual to continue.", icon="🧾")

else:
    if option == "Toss":
        from toss import TOSS
        writer = UXwriter(openai_api_key, TOSS, is_English)
    else:
        from sqzb import SQZB
        writer = UXwriter(openai_api_key, SQZB, is_English)

    # Text input
    txt_input = st.text_area('Enter your text', '', height=200)

    submitted = st.button('Check')

    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            score = writer.get_score(txt_input)
            
            score_data = json.loads(score)
            core_values = score_data["Core_Values"]
            emoji_values = {k: boolean_to_emoji(v) for k, v in core_values.items()}

            df = pd.DataFrame([emoji_values])
            df.index = ['']

            split_dfs = [df.iloc[:, i:i+5] for i in range(0, df.shape[1], 5)]
            for split_df in split_dfs:
                st.dataframe(split_df, use_container_width=True)

        with st.spinner('Generating...'):
            result = writer.edit(txt_input, score)

            st.info(result)