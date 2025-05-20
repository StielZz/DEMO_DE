import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Добавить продукт", page_icon=r"Ресурсы\Комфорт.ico")
st.title("Добавить продукт")

conn = sqlite3.connect("database")
cursor = conn.cursor()

df_type = pd.read_sql('SELECT "Код", "Тип продукции" FROM Product_type', conn)
df_material = pd.read_sql('SELECT "Код", "Тип материала" FROM Material_type', conn)

type_dict = dict(zip(df_type["Тип продукции"], df_type["Код"]))
material_dict = dict(zip(df_material["Тип материала"], df_material["Код"]))

with st.form("add_product_form"):
    name = st.text_input("Наименование продукции")
    article = st.number_input("Артикул", min_value=0, step=1, format="%d")
    min_price = st.number_input("Минимальная стоимость для партнера", min_value=0.0, format="%.2f")
    selected_type = st.selectbox("Тип продукции", list(type_dict.keys()))
    selected_material = st.selectbox("Тип материала", list(material_dict.keys()))

    submitted = st.form_submit_button("Добавить")

    if submitted:
        if name and article:
            try:
                cursor.execute(
                    '''INSERT INTO Products (
                        "Наименование продукции",
                        "Артикул",
                        "Минимальная стоимость для партнера",
                        "Тип продукции",
                        "Основной материал"
                    ) VALUES (?, ?, ?, ?, ?)''',
                    (
                        name,
                        article,
                        min_price,
                        type_dict[selected_type],
                        material_dict[selected_material]
                    )
                )
                conn.commit()
                st.success(f"Продукт '{name}' добавлен успешно!")
            except Exception as e:
                st.error(f"Ошибка при добавлении: {e}")
        else:
            st.warning("Заполните обязательные поля: наименование и артикул.")