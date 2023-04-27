-- Подключиться к БД Northwind и сделать следующие изменения:
-- 1. Добавить ограничение на поле unit_price таблицы products (цена должна быть больше 0)
ALTER TABLE products ADD CONSTRAINT chk_products_unit_price CHECK (unit_price > 0)

-- 2. Добавить ограничение, что поле discontinued таблицы products может содержать только значения 0 или 1
ALTER TABLE products ADD CONSTRAINT chk_products_discontinued CHECK (discontinued IN (0, 1))

-- 3. Создать новую таблицу, содержащую все продукты, снятые с продажи (discontinued = 1)
SELECT * INTO discontinued_products FROM products WHERE discontinued = 1

-- 4. Удалить из products товары, снятые с продажи (discontinued = 1)
-- Для 4-го пункта может потребоваться удаление ограничения, связанного с foreign_key. Подумайте, как это можно решить, чтобы связь с таблицей order_details все же осталась.
ALTER TABLE order_details DROP CONSTRAINT fk_order_details_products;
DELETE FROM products WHERE discontinued = 1;

SELECT order_id, product_id, order_details.unit_price, quantity, discount INTO order_details_discontinued_products FROM order_details
INNER JOIN discontinued_products USING (product_id)
WHERE discontinued_products.discontinued = 1

DELETE FROM order_details WHERE product_id in (SELECT product_id from order_details_discontinued_products)

ALTER TABLE order_details ADD CONSTRAINT fk_order_details_product_id FOREIGN KEY(product_id) REFERENCES products(product_id);
ALTER TABLE order_details_discontinued_products ADD CONSTRAINT fk_discontinued_products_product_id FOREIGN KEY(product_id) REFERENCES discontinued_products(product_id)