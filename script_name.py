import streamlit as st
import leancloud
import hashlib
import io

# LeanCloud 初始化
leancloud.init("ivmG8Co42lcMuP7nBqtB7dl6-gzGzoHsz", "zbhFWSdaoMsSMTXw3E03ib3H")

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
    # 用户注册与登录
    menu = ["登录", "注册"]
    choice = st.radio("选择操作", menu)

    if choice == "注册":
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

    # 文件上传和显示
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
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

        # 显示学生上传的文件
        st.subheader("已上传的文件")
        try:
            query = UserFile.query
            query.equal_to('username', st.session_state['student_name'])
            files = query.find()
            for file_record in files:
                lc_file = file_record.get('file')
                file_name = lc_file.name
                file_url = lc_file.url
                last_update_time = file_record.get('update_time')
                # 检查文件是否被修改
                if 'file_times' not in st.session_state:
                    st.session_state['file_times'] = {}

                if file_name in st.session_state['file_times']:
                    if st.session_state['file_times'][file_name] != last_update_time:
                        st.warning(f"文件 '{file_name}' 已被修改.")
                        st.session_state['file_times'][file_name] = last_update_time
                else:
                    st.session_state['file_times'][file_name] = last_update_time

                st.write(f"文件：{file_name}")
                st.markdown(f"[下载]({file_url})", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"加载文件列表失败：{e}")


