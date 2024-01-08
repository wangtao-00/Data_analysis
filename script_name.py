import streamlit as st
import leancloud
import hashlib
import io

# LeanCloud 初始化


leancloud.init(st.secrets["ID"], st.secrets["key"])


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
                uploaded_files = st.file_uploader("上传文件", accept_multiple_files=True, key="file_uploader",
                                                  type=["pdf", "docx", "doc"])
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        try:
                            file_data = uploaded_file.getvalue()
                            lc_file = leancloud.File(uploaded_file.name, io.BytesIO(file_data))
                            lc_file.save()

                            # 保存文件记录
                            user_file = UserFile()
                            user_file.set('username', st.session_state['student_name'])
                            user_file.set('file', lc_file)
                            user_file.set('original', True)
                            user_file.save()
                            st.success(f"文件 '{uploaded_file.name}' 上传成功！")
                        except Exception as e:
                            st.error(f"文件上传失败：{e}")

            # 显示已上传的文件及下载链接
            with st.container():
                st.write("已上传的文件")
                try:
                    query = UserFile.query
                    query.equal_to('username', st.session_state['student_name'])
                    files = query.find()

                    if files:
                        for file in files:
                            with st.container():
                                st.markdown("""
                                    <style>
                                        .file-box {
                                            border: 1px solid #445175;
                                            justify-content: space-between;
                                            align-items: center;
                                            border-radius: 5px;
                                            padding: 10px;
                                            margin-bottom: 10px;
                                            background-color: #fafafa;
                                            }
                                        .file-info {
                                            flex-grow: 1;
                                            }
                                        .download-button {
                                                border: none;
                                                padding: 5px 10px;
                                                border-radius: 5px;
                                                background-color: #acdcac;
                                                color: white;
                                                text-decoration: none;
                                                cursor: pointer;
                                                font-size: 0.8em;
                                                }
                                        .download-button:hover {
                                                background-color: #acdcac;
                                                }
                                    </style>
                                """, unsafe_allow_html=True)
                                lc_file = file.get('file')
                                file_name = lc_file.name
                                file_url = lc_file.url
                                # download_link = f'<a href="{file_url}" target="_blank">下载{file_name}</a>'
                                # st.markdown(download_link, unsafe_allow_html=True)

                                # 文件信息和下载按钮
                                st.markdown(f"""
                                    <div class="file-box">
                                        <div class="file-info">
                                            <b>{file_name}</b>
                                        </div>
                                        <a class="download-button" href="{file_url}" target="_blank">下载</a>
                                    </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.write("无文件")
                except Exception as e:
                    st.error("加载文件失败")

            # 文件修改提醒
            with st.container():
                try:
                    modified_files = []  # 存储已被修改的文件名称

                    if files:
                        for file in files:
                            # 检查文件是否被修改
                            if not file.get('original'):
                                modified_files.append(file.get('file').name)

                        if modified_files:
                            st.warning("以下文件已被修改：")
                            for file_name in modified_files:
                                st.markdown(f'<div class="file-box" style="color: red;">⚠️ {file_name}</div>',
                                            unsafe_allow_html=True)
                                # st.write(f"⚠️ {file_name}")
                        else:
                            st.write("没有文件被修改。")
                except Exception as e:
                    st.error("检查文件修改状态时出错")
    # 页脚
    st.markdown('<div class="footer">版权所有 &copy; 2023 学生文件上传系统</div>', unsafe_allow_html=True)
