import streamlit as st
import home_page
import frequency_distribution_page
import pie_bar_chart_page
import decision_tree_page
import script_name
st.set_page_config(page_title="数据分析", page_icon=":tiger:", layout="wide")

PAGES = {
    "主页": home_page,
    "频率分布图": frequency_distribution_page,
    "饼状图和直方图": pie_bar_chart_page,
    "决策树":decision_tree_page,
    "🌍 学生文件上传系统":script_name,
}
# 侧边栏
st.sidebar.title('导航')
selection = st.sidebar.selectbox("去往", list(PAGES.keys()))

page = PAGES[selection]
page.app()
