

CREATE TABLE "Material_type" (
    "Код" INTEGER PRIMARY KEY,
    "Тип материала" TEXT,
    "Процент потерь сырья" REAL
);


CREATE TABLE "Product_type" (
    "Код" INTEGER PRIMARY KEY,
    "Тип продукции" TEXT,
    "Коэффициент типа продукции" REAL
);


CREATE TABLE "Workshops" (
    "Код" INTEGER PRIMARY KEY,
  	"Название цеха" INTEGER,
  	"Тип цеха" TEXT,
  	"Количество человек для производства " INTEGER
);

CREATE TABLE "Products" (
    "Код" INTEGER PRIMARY KEY,
    "Тип продукции" INTEGER,
    "Наименование продукции" TEXT,
    "Артикул" INTEGER,
    "Минимальная стоимость для партнера" INTEGER,
    "Основной материал" TEXT,
    CONSTRAINT Products_Material_type_FK FOREIGN KEY ("Основной материал") REFERENCES Material_type(Код),
    CONSTRAINT Products_Product_type_FK FOREIGN KEY ("Тип продукции") REFERENCES Product_type(Код)
);

CREATE TABLE "Product_workshops" (
    "Код" INTEGER PRIMARY KEY,
    "Наименование продукции" INTEGER,
    "Название цеха" INTEGER,
    "Время изготовления, ч" REAL,
    CONSTRAINT Product_workshops_Workshops_FK FOREIGN KEY ("Название цеха") REFERENCES Workshops(Код),
    CONSTRAINT Product_workshops_Products_FK FOREIGN KEY ("Наименование продукции") REFERENCES Products(Код)
);


SELECT
    p."Наименование продукции",
    sum(pw."Время изготовления, ч")
FROM
    Product_workshops pw
INNER JOIN Products p ON
    pw."Наименование продукции" = p."Код"
GROUP BY
    p."Наименование продукции"



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






