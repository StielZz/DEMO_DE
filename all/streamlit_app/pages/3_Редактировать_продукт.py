import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Редактировать продукт", page_icon=r"Ресурсы\Комфорт.ico")
st.title("Редактировать продукт")

conn = sqlite3.connect("database")
cursor = conn.cursor()

products_df = pd.read_sql("""
    SELECT 
        p."Код", 
        p."Наименование продукции", 
        p."Артикул", 
        p."Минимальная стоимость для партнера", 
        pt."Тип продукции", 
        mt."Тип материала"
    FROM Products p
    INNER JOIN Product_type pt ON p."Тип продукции" = pt."Код"
    INNER JOIN Material_type mt ON p."Основной материал" = mt."Код"
""", conn)

product_names = products_df["Наименование продукции"].tolist()
selected_name = st.selectbox("Выберите продукт для редактирования", product_names)

if selected_name:
    product_data = products_df[products_df["Наименование продукции"] == selected_name].iloc[0]

    type_dict = pd.read_sql('SELECT "Код", "Тип продукции" FROM Product_type', conn).set_index("Тип продукции")["Код"].to_dict()
    material_dict = pd.read_sql('SELECT "Код", "Тип материала" FROM Material_type', conn).set_index("Тип материала")["Код"].to_dict()

    with st.form("edit_product_form"):
        new_name = st.text_input("Наименование продукции", value=product_data["Наименование продукции"])
        new_article = st.number_input("Артикул", value=int(product_data["Артикул"]), step=1)
        new_price = st.number_input("Минимальная стоимость для партнера", min_value=0.0, format="%.2f", value=float(product_data["Минимальная стоимость для партнера"]))
        new_type = st.selectbox("Тип продукции", options=list(type_dict.keys()), index=list(type_dict.keys()).index(product_data["Тип продукции"]))
        new_material = st.selectbox("Тип материала", options=list(material_dict.keys()), index=list(material_dict.keys()).index(product_data["Тип материала"]))

        submitted = st.form_submit_button("Сохранить изменения")

        if submitted:
            try:
                cursor.execute("""
                    UPDATE Products SET 
                        "Наименование продукции" = ?, 
                        "Артикул" = ?, 
                        "Минимальная стоимость для партнера" = ?, 
                        "Тип продукции" = ?, 
                        "Основной материал" = ?
                    WHERE "Код" = ?
                """, (
                    new_name,
                    new_article,
                    new_price,
                    type_dict[new_type],
                    material_dict[new_material],
                    int(product_data["Код"])
                ))
                rows_affected = cursor.rowcount
                conn.commit()
                st.success(f"Продукт успешно обновлён! Затронуто строк: {rows_affected}")
            except Exception as e:
                st.error(f"Ошибка при обновлении: {e}")

conn.close()
