import streamlit as st
import leancloud
from datetime import datetime
from PIL import Image
import io
# LeanCloud 初始化
leancloud.init("ivmG8Co42lcMuP7nBqtB7dl6-gzGzoHsz", "zbhFWSdaoMsSMTXw3E03ib3H")

# 打卡数据存储类
class PunchCard(leancloud.Object):
    pass

def app():
   # Streamlit 应用界面
    st.title('在线打卡系统')
    
    # 打卡表单
    with st.form("my_form"):
        username = st.text_input("用户名")
        uploaded_file = st.file_uploader("上传图片", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("打卡")
    
        if submitted and username:
            current_time = datetime.now()
            try:
                punch_card = PunchCard()
                punch_card.set('username', username)
                punch_card.set('time', current_time)
    
                # 处理上传的图片
                if uploaded_file is not None:
                    # 将上传的文件转换为 Bytes
                    image_bytes = uploaded_file.getvalue()
                    image = Image.open(io.BytesIO(image_bytes))
    
                    # 保存图片到 LeanCloud
                    lean_file = leancloud.File(uploaded_file.name, uploaded_file)
                    lean_file.save()
                    punch_card.set('image', lean_file)
    
                punch_card.save()
                st.success("打卡成功！")
            except Exception as e:
                st.error(f"打卡失败：{e}")
        elif submitted:
            st.error("请输入用户名")
        
