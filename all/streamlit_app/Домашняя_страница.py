import streamlit as st

st.set_page_config(page_title="Главная", page_icon=r"Ресурсы\Комфорт.ico")

st.title("Главная")

col1, col2 = st.columns([1, 4])

with col1:
    st.image("Ресурсы/Комфорт.png", width=100)

with col2:
    st.page_link("pages/1_Список_продукции.py", label="-> Список продукции")
    st.page_link("pages/2_Добавить_продукт.py", label="-> Добавить продукт")
    st.page_link("pages/3_Редактировать_продукт.py", label="-> Редактировать продукт")
