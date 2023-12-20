import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def app():
    # 饼状图和直方图页面的内容
    st.title("饼状图和直方图")

    # 文件上传
    uploaded_file = st.file_uploader("选择文件（ldeaths.csv）", type=["csv"], key="visualization")

    if uploaded_file is not None:
        # 读取数据
        data = pd.read_csv(uploaded_file, encoding='GBK')

        # 绘制饼图
        fig1, ax1 = plt.subplots()
        ax1.pie(data['死亡人数'], labels=data['月份'], autopct='%1.2f%%')
        plt.title('The distribution of monthly deaths from bronchitis, emphysema, and asthma in the UK in 1974 (pie chart)')
        st.pyplot(fig1)

        # 绘制条形图
        fig2, ax2 = plt.subplots()
        ax2.bar(data['月份'], data['死亡人数'])
        plt.title('Distribution of monthly deaths from bronchitis, emphysema, and asthma in the UK in 1974 (bar chart)')
        plt.xlabel('Month')
        plt.ylabel('Number of deaths/person ')
        st.pyplot(fig2)
