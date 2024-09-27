import streamlit as st
from gpt import UXwriter
import pandas as pd
import json
def boolean_to_emoji(value):
    return '✅' if value else '❌'


st.title("✍🏻 UX writer")
st.write(
    "SqueezeBits의 UX writer입니다."
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    writer = UXwriter(openai_api_key)

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
            st.table(df)

        with st.spinner('Generating...'):
            result = writer.edit(txt_input, score)

            st.info(result)