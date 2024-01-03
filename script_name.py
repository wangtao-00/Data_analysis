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
    # st.image("path_to_logo.png", width=100)
    st.title('🌍 学生文件上传系统')
    # 创建两列布局
    col1, col3,col2 = st.columns([1.2, 0.1, 2])
    
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
    with col3:
        st.markdown('`|`', unsafe_allow_html=True)  # 使用 Markdown 来模拟竖线

    # 文件上传和显示
    with col2:
        if 'logged_in' in st.session_state and st.session_state['logged_in']:
            # st.write(f"欢迎, {st.session_state['student_name']}!")
            welcome_message = f"<span style='color:blue; font-size:20px;'>欢迎, {st.session_state['student_name']}!</span>"
            st.markdown(welcome_message, unsafe_allow_html=True)
            # 文件上传逻辑
            uploaded_file = st.file_uploader("上传文件", type=["pdf", "docx"])
            if uploaded_file is not None:
                try:
                    # 读取文件内容并上传
                    file_data = uploaded_file.getvalue()
                    lc_file = leancloud.File(uploaded_file.name, io.BytesIO(file_data))
                    lc_file.save()
                    # 保存文件记录
                    user_file = UserFile()
                    user_file.set('username', st.session_state['student_name'])
                    user_file.set('file', lc_file)
                    user_file.set('original', True)
                    user_file.save()
                    st.success("文件上传成功！")
                except Exception as e:
                    st.error(f"文件上传失败：{e}")
    
            # 显示学生上传的文件的代码段
            st.subheader("已上传的文件")
            try:
                query = UserFile.query
                query.equal_to('username', st.session_state['student_name'])
                files = query.find()
                for file_record in files:
                    lc_file = file_record.get('file')
                    file_name = lc_file.name
                    file_url = lc_file.url
                    download_link = f'<a href="{file_url}" download="{file_name}">下载 {file_name}</a>'
                    st.markdown(download_link, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"加载文件列表失败：{e}")
    # 页脚
    st.markdown('<div class="footer">版权所有 &copy; 2023 学生文件上传系统</div>', unsafe_allow_html=True)

