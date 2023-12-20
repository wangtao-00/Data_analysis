import streamlit as st
from streamlit_drawable_canvas import st_canvas
import tensorflow as tf
from PIL import Image
import numpy as np




def get_model():
    # 加载模型
    model = tf.keras.models.load_model('model.h5')
    return model


def predict(image, model):
    image = image.resize((28, 28))
    image = image.convert('L')
    image_array = np.array(image)
    image_array = image_array / 255.0
    image_array = image_array.reshape(1, 28, 28, 1)
    out = model.predict(image_array)
    response = np.argmax(out, axis=1)
    return response[0]


def app():
    st.title("手写字体识别")

    # 创建画布
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # 画笔填充颜色
        stroke_width=10,  # 画笔宽度
        stroke_color="#ffffff",  # 画笔颜色
        background_color="#000000",  # 画布背景颜色
        width=280,  # 画布宽度
        height=280,  # 画布高度
        drawing_mode="freedraw",  # 绘画模式
        key="canvas",
    )

    # 检测是否有画布数据
    if canvas_result.image_data is not None:
        st.write("画布内容:")
        # 将画布内容转换为 PIL Image
        image = Image.fromarray(canvas_result.image_data.astype('uint8'), mode='RGBA')
        image = image.convert('L')  # 转换为灰度图
        # st.image(image, caption='绘制的手写数字', use_column_width=True)

        # 预测按钮
        if st.button('预测'):
            model = get_model()  # 加载模型
            label = predict(image, model)
            st.write(f'预测结果: {label}')