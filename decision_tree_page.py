import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def app():
    st.title("决策树模型")

    # 文件上传
    uploaded_file = st.file_uploader("上传 EEG Eye State 数据文件", type=["txt"])

    if uploaded_file is not None:
        # 读取数据
        data = pd.read_table(uploaded_file, sep=',')
        X = data.iloc[:, :14]
        y = data.iloc[:, 14]

        # 数据标准化
        scaler = StandardScaler()
        scaler.fit(X)
        X = scaler.transform(X)

        # 划分训练集、测试集
        traindata, testdata, traintarget, testtarget = train_test_split(X, y, test_size=0.2)
        model_dtc = DecisionTreeClassifier() # 确定决策树参数
        model_dtc.fit(traindata, traintarget) # 拟合数据

        # 预测测试集结果
        testtarget_pre = model_dtc.predict(testdata)

        # 结果展示
        st.write("预测结果准确率为：", accuracy_score(testtarget, testtarget_pre))

        # 绘制混淆矩阵
        cm = confusion_matrix(testtarget, testtarget_pre)
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt="d", ax=ax)
        plt.ylabel('实际值')
        plt.xlabel('预测值')
        st.pyplot(fig)

        # 绘制预测数值和真实值的折线图
        fig2, ax2 = plt.subplots()
        ax2.plot(testtarget.values[:20], label='实际值', marker='o')
        ax2.plot(testtarget_pre[:20], label='预测值', marker='x')
        plt.title('预测值与实际值对比')
        plt.ylabel('值')
        plt.xlabel('样本')
        plt.legend()
        st.pyplot(fig2)
