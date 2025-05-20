import sqlite3
import pandas as pd

conn = sqlite3.connect('database')


df_material_type = pd.read_excel(r"Ресурсы\Material_type_import.xlsx")
df_material_type["Код"] = range(1, len(df_material_type) + 1)
material_type_dict = dict(zip(df_material_type["Тип материала"], df_material_type["Код"]))

df_product_type = pd.read_excel(r"Ресурсы\Product_type_import.xlsx")
df_product_type["Код"] = range(1, len(df_product_type) + 1)
product_type_dict = dict(zip(df_product_type["Тип продукции"], df_product_type["Код"]))

df_workshops = pd.read_excel(r"Ресурсы\Workshops_import.xlsx")
df_workshops["Код"] = range(1, len(df_workshops) + 1)
workshops_dict = dict(zip(df_workshops["Название цеха"], df_workshops["Код"]))

df_products = pd.read_excel(r"Ресурсы\Products_import.xlsx")
df_products["Код"] = range(1, len(df_products) + 1)
products_dict = dict(zip(df_products["Наименование продукции"], df_products["Код"]))
df_products["Тип продукции"] = df_products["Тип продукции"].map(product_type_dict)
df_products["Основной материал"] = df_products["Основной материал"].map(material_type_dict)

df_product_workshops = pd.read_excel(r"Ресурсы\Product_workshops_import.xlsx")
df_product_workshops["Код"] = range(1, len(df_product_workshops) + 1)
df_product_workshops['Название цеха'] = df_product_workshops['Название цеха'].map(workshops_dict)
df_product_workshops['Наименование продукции'] = df_product_workshops['Наименование продукции'].map(products_dict)


df_material_type.to_sql(name="Material_type", con=conn, if_exists="append", index=False)
df_product_type.to_sql(name="Product_type", con=conn, if_exists="append", index=False)
df_workshops.to_sql(name="Workshops", con=conn, if_exists="append", index=False)
df_products.to_sql(name="Products", con=conn, if_exists="append", index=False)
df_product_workshops.to_sql(name="Product_workshops", con=conn, if_exists="append", index=False)


with open("dump.sql", "w", encoding="utf-8") as file:
    for line in conn.iterdump():
        file.write(line + "\n")

conn.close()