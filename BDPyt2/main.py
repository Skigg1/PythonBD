import sqlite3

with sqlite3.connect("BDPyt2/t1.db") as conn:
    cursor = conn.cursor()

    print(
        "Что бы выбрать действие введите число:\nВывести таблицу покупателей - 1.1\nДобавить клиента - 1.2\nУдалить покупателя - 1.3\nВывести таблицу товаров - 2.1\nДобавить товар - 2.2\nУдалить товар - 2.3\nВывести таблицу заказов - 3.1\nДобавить заказ - 3.2\nУдалить заказ - 3.3\nВывести таблицу с полной информацией о заказе - 4.1\nДобавить товары в заказ - 4.2\nУдалить товары из заказ - 4.3\nЧто бы закрыть программу напишите Стоп"
    )
    while True:

        user_input = input()

        if user_input == "Стоп":
            break

        if user_input == "1.1":

            cursor.execute("SELECT byers.name, byers.email FROM byers")

            byers = cursor.fetchall()
            for p in byers:
                print(f"Имя покупателя - {p[0]}; Эллектронная почта - {p[1]}")

        elif user_input == "1.2":

            name_user = input("Введите имя пользователя: ")
            email_user = input("Введите email пользователя: ")

            try:
                cursor.execute(
                    "INSERT INTO byers(name, email) VALUES(?, ?)",
                    (
                        name_user,
                        email_user,
                    ),
                )
                conn.commit()
                print(f"Покупатель '{name_user}' успешно добавлен!")
            except sqlite3.Error as e:
                print(f"Ошибка при добавлении товара: {e}")

        elif user_input == "1.3":
            name_user = input("Введите имя пользователя которого хотите удалить: ")

            if not name_user:
                print("Ошибка: Имя пользователя не может быть пустым")
                continue

            cursor.execute("DELETE FROM byers WHERE name = ?", (name_user,))

            conn.commit()

            # Проверяем, сколько строк было удалено
            if cursor.rowcount > 0:
                print(f"Пользователь '{name_user}' успешно удалён!")
            else:
                print("Не удалось удалить пользователя (неизвестная ошибка)")

        elif user_input == "2.1":

            cursor.execute("SELECT products.name, products.price FROM products")

            products = cursor.fetchall()
            for p in products:
                print(f"Название товара - {p[0]}; Цена - {p[1]}")

        elif user_input == "2.2":

            name_product = input("Введите название товара: ")
            price_product = input("Введите цену: ")

            try:
                cursor.execute(
                    "INSERT INTO products(name, price) VALUES(?, ?)",
                    (
                        name_product,
                        price_product,
                    ),
                )
                conn.commit()
                print(f"Товвар '{name_product}' успешно добавлен!")
            except sqlite3.Error as e:
                print(f"Ошибка при добавлении товара: {e}")

        elif user_input == "2.3":
            name_product = input("Введите название товара которого хотите удалить: ")

            if not name_product:
                print("Ошибка: Название товара не может быть пустым")
                continue

            cursor.execute("DELETE FROM products WHERE name = ?", (name_product,))

            conn.commit()

            # Проверяем, сколько строк было удалено
            if cursor.rowcount > 0:
                print(f"Товар '{name_product}' успешно удалён!")
            else:
                print("Не удалось удалить товар (неизвестная ошибка)")

        elif user_input == "3.1":

            cursor.execute(
                "SELECT orders.id, byers.name, orders.date FROM orders JOIN byers ON orders.byers_id = byers.id"
            )

            products = cursor.fetchall()
            for p in products:
                print(
                    f"Номер заказа - {p[0]}; Имя покупателя - {p[1]}; Дата покупки - {p[2]};"
                )

        elif user_input == "3.2":

            buyer_name = input("Введите имя покупателя: ")
            date = input("Введите дату заказа (например, 24.04.2025): ")

            cursor.execute("SELECT id FROM byers WHERE name = ?", (buyer_name,))
            buyer_true = cursor.fetchone()

            if buyer_true:  # Если покупатель существует
                try:
                    cursor.execute(
                        "INSERT INTO orders(byers_id, date) VALUES(?, ?)",
                        (
                            buyer_true[0],  # ID покупателя
                            date,
                        ),
                    )
                    conn.commit()
                    print(f"Заказ для '{buyer_name}' успешно добавлен!")
                except sqlite3.Error as e:
                    print(f"Ошибка при добавлении заказа: {e}")
            else:
                print(f"Ошибка: покупателя '{buyer_name}' не существует!")

        elif user_input == "3.3":
            number_order = input("Введите номер заказа который хотите удалить: ")

            if not number_order:
                print("Ошибка: Номер заказа не может быть пустым")
                continue

            cursor.execute("DELETE FROM orders WHERE id = ?", (number_order,))

            conn.commit()

            # Проверяем, сколько строк было удалено
            if cursor.rowcount > 0:
                print(f"Заказ '№{number_order}' успешно удалён!")
            else:
                print("Не удалось удалить товар (неизвестная ошибка)")

        elif user_input == "4.1":
            # SQL-запрос для вывода полной информации о заказах
            query = """
            SELECT 
                b.name AS buyer_name,
                o.id AS order_id,
                o.date AS order_date,
                GROUP_CONCAT(p.name, ', ') AS products,
                SUM(p.price) AS total_price
            FROM 
                orders o
            JOIN 
                byers b ON o.byers_id = b.id
            JOIN 
                order_products op ON o.id = op.order_id
            JOIN 
                products p ON op.products_id = p.id
            GROUP BY 
                o.id, b.name, o.date
            ORDER BY 
                o.id;
            """

            try:
                cursor.execute(query)
                results = cursor.fetchall()

                if not results:
                    print("Нет данных о заказах")
                else:
                    print("\nПолная информация о заказах:")
                    print("=" * 80)
                    print(
                        "{:<15} | {:<10} | {:<12} | {:<30} | {:<10}".format(
                            "Имя покупателя", "Номер заказа", "Дата", "Товары", "Сумма"
                        )
                    )
                    print("-" * 80)

                    for row in results:
                        print(
                            "{:<15} | {:<10} | {:<12} | {:<30} | {:<10}".format(
                                row[0], row[1], row[2], row[3], row[4]
                            )
                        )

            except sqlite3.Error as e:
                print(f"Ошибка при получении данных о заказах: {e}")

        elif user_input == "4.2":

            order_number = input("Введите номер заказа: ")
            product_number = ""

            while True:
                product_number = input(
                    'Введите название товара, что бы закончить ввод напишите "Стоп": '
                )

                if product_number.lower() == "Cтоп":
                    break

                try:
                    cursor.execute(
                        "INSERT INTO order_products(order_id, products_id) VALUES(?, ?)",
                        (
                            order_number,
                            product_number,
                        ),
                    )
                    conn.commit()

                except sqlite3.Error as e:
                    print(f"Ошибка при добавлении товара: {e}")

            print(f"Товвары успешно добавлены!")

        elif user_input == "4.3":

            order_number = input("Введите номер заказа для удаления товаров: ")
            product_number = ""

            while True:
                product_number = input(
                    "Введите название товара для удаления (для завершения введите 'Стоп'): "
                )
                if product_number.lower() == "стоп":
                    break

                try:
                    # Удаляем конкретный товар из указанного заказа
                    cursor.execute(
                        "DELETE FROM order_products WHERE order_id = ? AND products_id = ?",
                        (order_number, product_number),
                    )
                    conn.commit()

                    if cursor.rowcount > 0:
                        print(
                            f"Товар '{product_number}' удален из заказа {order_number}"
                        )
                    else:
                        print(
                            f"Товар '{product_number}' не найден в заказе {order_number}"
                        )

                except sqlite3.Error as e:
                    print(f"Ошибка при удалении товара: {e}")

            print("Операция удаления завершена!")
