import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Список продукции", page_icon=r"Ресурсы\Комфорт.ico")
st.title("Список продукции")

conn = sqlite3.connect("database")

df = pd.read_sql("""
    SELECT
        pt."Тип продукции",
        p."Наименование продукции",        
        p."Артикул",
        p."Минимальная стоимость для партнера",
        mt."Тип материала",
        p."Код"
    FROM Products p
    INNER JOIN Product_type pt ON p."Тип продукции" = pt."Код"
    INNER JOIN Material_type mt ON p."Основной материал" = mt."Код"
""", conn)

def get_production_times(conn):
    query = """
        SELECT
            p."Код" AS product_code,
            SUM(pw."Время изготовления, ч") AS total_time
        FROM Product_workshops pw
        INNER JOIN Products p ON pw."Наименование продукции" = p."Код"
        GROUP BY p."Код"
    """
    return pd.read_sql(query, conn)

# Объединяем таблицы продуктов и времени изготовления по коду продукта, 
# заполняем пропуски нулями если таковые есть и переименовываем столбец для удобства отображения и удаляем ненужные коды
df_time = get_production_times(conn)
df_final = df.merge(df_time, left_on="Код", right_on="product_code", how="left")
df_final["total_time"] = df_final["total_time"].fillna(0)
df_final = df_final.rename(columns={"total_time": "Время изготовления, ч"})
st.dataframe(df_final.drop(columns=["product_code", "Код"]), hide_index=True)

st.page_link("Домашняя_страница.py", label="-> Назад на главную")