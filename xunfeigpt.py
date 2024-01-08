import streamlit as st
from streamlit_chat import message

import SparkApi
# 设置 API 信息
appid = "5cd53875"
api_secret = "ZjJlNWVkZjMyZjcwNjJiZjAzMjNlOGQz"
api_key = "dc4971bf2c19bcb5a81f3f46dc795bd8"
domain = "generalv3"
Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"

# 初始化 Streamlit 状态
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

def add_to_conversation(role, content):
    st.session_state['conversation'].append({"role": role, "content": content})

def call_spark_api(conversation):
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, conversation)
    return SparkApi.answer

def app():
    st.title("智能问答助手")

    # 创建两栏布局
    col1, col2 = st.columns([1, 1.5])  # 比例为1:1.5，可根据需要调整

    # 第一栏：应用介绍和说明
    with col1:
        st.markdown("#### 智能机器人")
        st.markdown("我可以回答您的任何问题！")
        st.markdown("---")
        st.markdown("#### 使用说明")
        st.markdown("在右侧输入框中输入您的问题，然后查看机器人的回答。")

    # 第二栏：用户输入和对话历史
    with col2:
        user_input = st.text_input("请输入您的问题:", key='input')
        send_button = st.button("发送")
        new_chat_button = st.button("新聊天")

        if send_button and user_input:
            add_to_conversation("user", user_input)
            answer = call_spark_api(st.session_state['conversation'])
            add_to_conversation("assistant", answer)
            # st.session_state['input'] = ''  # 清空输入框

        if new_chat_button:
            st.session_state['conversation'] = []  # 清空对话历史

        # 渲染对话
        for chat in reversed(st.session_state['conversation']):
            if chat["role"] == "assistant":
                message(chat["content"])
            else:
                message(chat["content"], is_user=True)


