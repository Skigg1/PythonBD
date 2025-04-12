import sqlite3

# подключение базы данных
with sqlite3.connect("BDPython/t1.db") as conn:
    cursor = conn.cursor()

    print(
        "Что бы выбрать действие введите число:\nВывести все товары - 1\nВывести список доступных категорий - 2\nДобавить товар - 3\nДобавить категорию - 4\nУдалить товар - 5\nЧто бы закрыть программу напишите Стоп"
    )
    while True:

        user_input = input()

        if user_input == "Стоп":
            break

        if user_input == "1":

            cursor.execute(
                "SELECT products.name, products.price, categories.name FROM products JOIN categories ON products.category_id = categories.id"
            )
            product = cursor.fetchall()
            for p in product:
                print(
                    f"Название товара - {p[0]}; Cтоимость - {p[1]}; Категория товара - {p[2]}"
                )

        elif user_input == "2":
            cursor.execute("SELECT name FROM categories")
            product = cursor.fetchall()
            i = 1

            for p in product:
                print(f"Категория {i} - {p[0]}")
                i += 1

        elif user_input == "3":
            name_user = input("Введите название товара: ")
            price_user = float(input("Введите стоимость: "))
            category_user = input("Введите категорию товара в виде текста: ")

            cursor.execute("SELECT id FROM categories WHERE name = ?", (category_user,))
            category_data = cursor.fetchone()

            if category_data:  # Если категория существует
                try:
                    cursor.execute(
                        "INSERT INTO products(name, price, category_id) VALUES(?, ?, ?)",
                        (
                            name_user,
                            price_user,
                            category_data[0],
                        ),
                    )
                    conn.commit()
                    print(f"Товар '{name_user}' успешно добавлен!")
                except sqlite3.Error as e:
                    print(f"Ошибка при добавлении товара: {e}")
            else:
                print(f"Ошибка: категории '{category_user}' не существует!")

        elif user_input == "4":
            name_categor = input("Введите название категории: ")

            if not name_categor:
                print("Ошибка: название категории не может быть пустым!")
                continue

            try:
                cursor.execute(
                    "INSERT INTO categories(name) VALUES(?)", (name_categor,)
                )
                conn.commit()
                print(
                    f"Категория '{name_categor}' успешно добавлена. ID: {cursor.lastrowid}"
                )
            except sqlite3.IntegrityError:
                print(f"Ошибка: категория '{name_categor}' уже существует!")
            except sqlite3.OperationalError:
                print(
                    "Ошибка: база данных заблокирована. Закройте другие программы, использующие БД."
                )
            except sqlite3.Error as e:
                print(f"Ошибка базы данных: {e}")

        elif user_input == "5":
            name_product = input("Ввдеите название товара который хотите удалить: ")

            cursor.execute("DELETE FROM products WHERE name = ?", (name_product,))

            conn.commit()

            # Проверяем, сколько строк было удалено
            if cursor.rowcount > 0:
                print(f"Товар '{name_product}' успешно удалён!")
            else:
                print("Не удалось удалить товар (неизвестная ошибка)")

        else:
            print("Такой команды не существует")
