import streamlit as st
import leancloud
import hashlib
import io

# LeanCloud 初始化
leancloud.init("ivmG8Co42lcMuP7nBqtB7dl6-gzGzoHsz", "zbhFWSdaoMsSMTXw3E03ib3H")

# 自定义样式
def custom_css():
    st.markdown("""
        <style>
            .main { background-color: #adfadf; }
            .stButton>button { width: 100%; }
            .stTextInput>div>div>input { padding: 10px; }
            .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #f1f1f1; text-align: center; padding: 10px; }
        </style>
        """, unsafe_allow_html=True)


# 学生用户类
class Student(leancloud.Object):
    pass

# 文件存储类
class UserFile(leancloud.Object):
    pass

# 密码加密
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 注册学生
def register_student(username, password):
    new_student = Student()
    new_student.set('username', username)
    new_student.set('password', hash_password(password))
    new_student.save()

# 验证学生
def verify_student(username, password):
    query = Student.query
    query.equal_to('username', username)
    try:
        student = query.first()
        return student.get('password') == hash_password(password)
    except leancloud.LeanCloudError:
        return False

# 学生文件上传系统
def app():
    # custom_css()  # 应用自定义样式

    # 页眉
    st.title('🌍 学生文件上传系统')
    # 创建两列布局
    col1, col_spacer, col2 = st.columns([1.8, 0.1, 2])
    
    # 用户注册与登录
    with col1:
        menu = ["登录", "注册"]
        choice = st.radio("选择操作", menu)
    
        if choice == "注册":
            st.session_state['logged_in'] = False
            new_username = st.text_input("用户名", key='new_username')
            new_password = st.text_input("密码", type='password', key='new_password')
            if st.button("注册"):
                register_student(new_username, new_password)
                st.success("注册成功！")
    
        elif choice == "登录":
            username = st.text_input("用户名", key='username')
            password = st.text_input("密码", type='password', key='password')
            if st.button("登录"):
                if verify_student(username, password):
                    st.success('登录成功')
                    st.session_state['logged_in'] = True
                    st.session_state['student_name'] = username
                    
                else:
                    st.error("用户名或密码错误")
    # 在两列之间添加竖线
    with col_spacer:
        st.markdown(
        """
        <style>
        .divider {
            border-left: 1px solid  #c0c0c0;
            height: 500px;
        }
        </style>
        <div class="divider"></div>
        """,
        unsafe_allow_html=True
    )


    with col2:  # 右侧列内容
        if 'logged_in' in st.session_state and st.session_state['logged_in']:
            # 显示学生信息
            with st.container():
                st.write(f"欢迎, {st.session_state['student_name']}!")
    
            # 文件上传区域
            with st.container():
                uploaded_file_hw1 = st.file_uploader("上传文件", key="file_uploader_hw1", type=["pdf", "docx"])
                if uploaded_file_hw1 is not None:
                    try:
                        file_data_hw1 = uploaded_file_hw1.getvalue()
                        lc_file_hw1 = leancloud.File(uploaded_file_hw1.name, io.BytesIO(file_data_hw1))
                        lc_file_hw1.save()
                        
                        # 保存文件记录
                        user_file_hw1 = UserFile()
                        user_file_hw1.set('username', st.session_state['student_name'])
                        user_file_hw1.set('file', lc_file_hw1)
                        user_file_hw1.set('homework', "hw1")
                        user_file_hw1.set('original', True)
                        user_file_hw1.save()
                        st.success("文件上传成功！")
                    except Exception as e:
                        st.error(f"文件上传失败：{e}")
    
            # 显示已上传的文件及下载链接
            with st.container():
                try:
                    query_hw1 = UserFile.query
                    query_hw1.equal_to('username', st.session_state['student_name'])
                    query_hw1.equal_to('homework', "hw1")
                    file_hw1 = query_hw1.first()
                    if file_hw1:
                        lc_file_hw1 = file_hw1.get('file')
                        file_name_hw1 = lc_file_hw1.name
                        file_url_hw1 = lc_file_hw1.url
                        st.write(f"文件：{file_name_hw1}")
                        st.markdown(f"[下载文件]({file_url_hw1})", unsafe_allow_html=True)
                    else:
                        st.write("无文件")
                except Exception as e:
                    st.error("加载文件文件失败")
    
            # 文件修改提示
            with st.container():
                try:
                    if files_hw1:
                        for file_hw1 in files_hw1:
                            if not file_hw1.get('original'):
                                st.warning("文件已被修改")
                except Exception as e:
                    st.error("检查文件状态失败")
    # 页脚
    st.markdown('<div class="footer">版权所有 &copy; 2023 学生文件上传系统</div>', unsafe_allow_html=True)

