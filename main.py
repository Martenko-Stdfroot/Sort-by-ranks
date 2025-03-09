import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import random

# Функция для создания базы данных и таблицы
def create_database():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rank INTEGER NOT NULL,
            price TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Функция для заполнения базы данных начальными данными
def populate_database():
    initial_data = [
        ("яблоки", 1, "80–120 ₽ за кг", "базовый"),
        ("масло", 2, "150–200 ₽ за пачку (200 г)", "средний"),
        ("молоко", 1, "50–70 ₽ за литр", "базовый"),
        ("хлеб", 1, "30–50 ₽ за буханку", "базовый"),
        ("радиодетали", 3, "100–1000 ₽ за штуку", "высокий"),
        ("кофе", 3, "300–500 ₽ за упаковку (250 г)", "высокий"),
        ("мыло", 2, "50–100 ₽ за кусок", "средний"),
        ("машина", 4, "от 500 000 ₽", "роскошь")
    ]

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO products (name, rank, price, category) VALUES (?, ?, ?, ?)', initial_data)
    conn.commit()
    conn.close()

# Функция для получения данных из базы данных
def get_products(filter_rank=None):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    if filter_rank:
        cursor.execute('SELECT * FROM products WHERE rank = ?', (filter_rank,))
    else:
        cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

# Функция для добавления продукта
def add_product(name, rank, price, category):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, rank, price, category) VALUES (?, ?, ?, ?)', (name, rank, price, category))
    conn.commit()
    conn.close()
    update_product_list()

# Функция для удаления продукта
def delete_product(product_id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    update_product_list()

# Функция для обновления списка продуктов
def update_product_list(filter_rank=None):
    for row in tree.get_children():
        tree.delete(row)
    products = get_products(filter_rank)
    for product in products:
        tree.insert("", "end", values=product)

# Функция для обновления цен (моковые данные)
def update_prices():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, price FROM products')
    products = cursor.fetchall()

    for product in products:
        product_id, old_price = product
        new_price = f"{random.randint(50, 500)}–{random.randint(600, 1000)} ₽"
        cursor.execute('UPDATE products SET price = ? WHERE id = ?', (new_price, product_id))

    conn.commit()
    conn.close()
    update_product_list()

# Функция для обработки нажатия кнопки "Добавить"
def on_add():
    name = entry_name.get()
    rank = entry_rank.get()
    price = entry_price.get()
    category = entry_category.get()

    if name and rank and price and category:
        add_product(name, rank, price, category)
        entry_name.delete(0, tk.END)
        entry_rank.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_category.delete(0, tk.END)
    else:
        messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")

# Функция для обработки нажатия кнопки "Удалить"
def on_delete():
    selected_item = tree.selection()
    if selected_item:
        product_id = tree.item(selected_item)['values'][0]
        delete_product(product_id)
    else:
        messagebox.showwarning("Ошибка", "Выберите продукт для удаления!")

# Функция для обработки фильтрации по рангу
def on_filter():
    selected_rank = combo_filter.get()
    if selected_rank == "Все":
        update_product_list()
    else:
        update_product_list(int(selected_rank))

# Функция для открытия/закрытия боковой панели
def toggle_sidebar():
    if sidebar.winfo_ismapped():
        sidebar.grid_forget()
    else:
        sidebar.grid(row=0, column=0, rowspan=10, sticky="ns")

# Функция для отображения окна помощи с прокруткой
def show_help():
    help_window = tk.Toplevel(root)
    help_window.title("Помощь")
    help_window.geometry("400x300")  # Размер окна помощи

    # Текст помощи
    help_text = (
        "Это помощь по программе сортировки\n\n"
        "1. Название - это ввод. Здесь вы можете указать название продукта.\n"
        "2. Ранг - это степень дороговизны и сложности продукта. Есть четыре вида:\n"
        "   - 1 (Базовый): перечень необходимых предметов.\n"
        "   - 2 (Средний): перечень не особо важных и не особо сложных продуктов.\n"
        "   - 3 (Высокий): перечень сложных и дорогих продуктов (например, радиодетали).\n"
        "   - 4 (Роскошь): самый высокий уровень, означающий сложность и дороговизну продукта (например, машины).\n"
        "   В ранги вы вносите по своему усмотрению уровень продукта.\n"
        "3. Цена - это стоимость продукта. Указывайте её на своё усмотрение.\n"
        "4. Категория - здесь вы указываете название ранга (см. пункт 2).\n\n"
        "Удачи!\nMartenko Stdfroot. 2025 год."
    )

    # Добавляем Text и Scrollbar
    text_area = tk.Text(help_window, wrap="word", font=("Arial", 8))
    text_area.insert("1.0", help_text)
    text_area.config(state="disabled")  # Запрещаем редактирование

    scrollbar = ttk.Scrollbar(help_window, orient="vertical", command=text_area.yview)
    text_area.configure(yscrollcommand=scrollbar.set)

    # Размещаем элементы
    text_area.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Создаём базу данных и заполняем её данными
create_database()
populate_database()

# Создаём графический интерфейс
root = tk.Tk()
root.title("Управление продуктами")
root.geometry("210x100")  # Устанавливаем размер окна для экрана 210x100

# Уменьшаем шрифты для компактности
font = ("Arial", 6)

# Боковая панель с функциями
sidebar = tk.Frame(root, bg="lightgray", width=50)
sidebar.grid(row=0, column=0, rowspan=10, sticky="ns")

# Кнопки на боковой панели
btn_help = tk.Button(sidebar, text="Помощь", font=font, command=show_help)
btn_help.pack(pady=2)

btn_about = tk.Button(sidebar, text="О программе", font=font, command=lambda: messagebox.showinfo("О программе", about_text))
btn_about.pack(pady=2)

# Текст справки
about_text = (
    "Программа для сортировки продуктов по рангам\n"
    "Сделана во время моего обучения программированию на Python\n"
    "Думаю, вам понравится или где-то пригодится\n"
    "На этом всё, и снова. Удачи!\n"
    "Martenko Stdfroot. 2025 год."
)

# Кнопка для скрытия/показа боковой панели
btn_toggle_sidebar = tk.Button(root, text="Меню", font=font, command=toggle_sidebar)
btn_toggle_sidebar.grid(row=0, column=1, sticky="w", padx=2, pady=2)

# Поля для ввода данных
tk.Label(root, text="Название:", font=font).grid(row=1, column=1, sticky="w", padx=2, pady=1)
entry_name = tk.Entry(root, font=font, width=10)
entry_name.grid(row=2, column=1, columnspan=2, sticky="we", padx=2, pady=1)

tk.Label(root, text="Ранг:", font=font).grid(row=3, column=1, sticky="w", padx=2, pady=1)
entry_rank = tk.Entry(root, font=font, width=3)
entry_rank.grid(row=4, column=1, sticky="we", padx=2, pady=1)

tk.Label(root, text="Цена:", font=font).grid(row=3, column=2, sticky="w", padx=2, pady=1)
entry_price = tk.Entry(root, font=font, width=7)
entry_price.grid(row=4, column=2, sticky="we", padx=2, pady=1)

tk.Label(root, text="Категория:", font=font).grid(row=5, column=1, sticky="w", padx=2, pady=1)
entry_category = tk.Entry(root, font=font, width=10)
entry_category.grid(row=6, column=1, columnspan=2, sticky="we", padx=2, pady=1)

# Кнопка "Добавить"
btn_add = tk.Button(root, text="Добавить", font=font, command=on_add)
btn_add.grid(row=7, column=1, sticky="we", padx=2, pady=1)

# Кнопка "Удалить"
btn_delete = tk.Button(root, text="Удалить", font=font, command=on_delete)
btn_delete.grid(row=7, column=2, sticky="we", padx=2, pady=1)

# Выпадающий список для фильтрации по рангам
tk.Label(root, text="Фильтр:", font=font).grid(row=8, column=1, sticky="w", padx=2, pady=1)
combo_filter = ttk.Combobox(root, values=["Все", 1, 2, 3, 4], font=font, width=3)
combo_filter.current(0)
combo_filter.grid(row=8, column=2, sticky="we", padx=2, pady=1)

# Кнопка "Применить фильтр"
btn_filter = tk.Button(root, text="Фильтр", font=font, command=on_filter)
btn_filter.grid(row=9, column=1, sticky="we", padx=2, pady=1)

# Кнопка "Обновить цены"
btn_update_prices = tk.Button(root, text="Цены", font=font, command=update_prices)
btn_update_prices.grid(row=9, column=2, sticky="we", padx=2, pady=1)

# Таблица для отображения продуктов
columns = ("id", "name", "rank", "price", "category")
tree = ttk.Treeview(root, columns=columns, show="headings", height=2)
tree.heading("id", text="ID")
tree.heading("name", text="Название")
tree.heading("rank", text="Ранг")
tree.heading("price", text="Цена")
tree.heading("category", text="Категория")
tree.grid(row=11, column=1, columnspan=2, sticky="nsew", padx=2, pady=1)

# Добавляем Scrollbar для таблицы
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=11, column=3, sticky="ns")

# Обновляем список продуктов
update_product_list()

# Запуск приложения
root.mainloop()
      
