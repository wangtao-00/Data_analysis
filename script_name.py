# -*- coding: utf-8 -*-
# @Time : 2023/12/29 14:13
# @Author : wangtao
# @Email : wngtaow@outlook.com
# @File :script_name.py


import streamlit as st
import datetime

def save_punch_card(name, time):
    """将打卡记录保存到文件"""
    with open("punch_card_records.txt", "a") as file:
        file.write(f"{name} - {time}\n")

# 设置网页标题
def app():
    st.title('在线打卡系统')

    # 创建一个简单的表单
    with st.form("punch_card_form"):
        name = st.text_input("请输入你的姓名")
        submit_button = st.form_submit_button("打卡")

    if submit_button:
        current_time = datetime.datetime.now()
        save_punch_card(name, current_time)
        st.write(f"{name}，你已于 {current_time} 成功打卡！")

    # 显示打卡记录
    st.subheader("打卡记录")
    try:
        with open("punch_card_records.txt", "r") as file:
            st.text(file.read())
    except FileNotFoundError:
        st.write("还没有任何打卡记录。")
