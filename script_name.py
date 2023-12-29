import streamlit as st
import leancloud
from datetime import datetime

# LeanCloud 初始化
leancloud.init("ivmG8Co42lcMuP7nBqtB7dl6-gzGzoHsz", "zbhFWSdaoMsSMTXw3E03ib3H")

# 打卡数据存储类
class PunchCard(leancloud.Object):
    pass

def app():
    # Streamlit 应用界面
    st.title('在线打卡系统')

    with st.form("my_form"):
        username = st.text_input("用户名")
        submitted = st.form_submit_button("打卡")

        if submitted:
            current_time = datetime.now()
            try:
                punch_card = PunchCard()
                punch_card.set('username', username)
                punch_card.set('time', current_time)
                punch_card.save()
                st.success("打卡成功！")
            except Exception as e:
                st.error("打卡失败：" + str(e))

    
