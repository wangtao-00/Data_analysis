import streamlit as st
import home_page
import frequency_distribution_page
import pie_bar_chart_page
import decision_tree_page
import mninst
import script_name
st.set_page_config(page_title="数据分析", page_icon=":tiger:", layout="wide")

PAGES = {
    "主页": home_page,
    "频率分布图": frequency_distribution_page,
    "饼状图和直方图": pie_bar_chart_page,
    "决策树":decision_tree_page,
    "手写字体识别":mninst,
    "打卡":script_name,
}

st.sidebar.title('导航')
selection = st.sidebar.radio("去往", list(PAGES.keys()))

page = PAGES[selection]
page.app()
