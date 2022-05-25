"""
2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

ПРОШУ ВАС НЕ УДАЛЯТЬ ИСХОДНЫЙ JSON-ФАЙЛ
ПРИМЕР ТОГО, ЧТО ДОЛЖНО ПОЛУЧИТЬСЯ

{
    "orders": [
        {
            "item": "принтер", (возможные проблемы с кирилицей)
            "quantity": "10",
            "price": "6700",
            "buyer": "Ivanov I.I.",
            "date": "24.09.2017"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        }
    ]
}

вам нужно подгрузить JSON-объект
и достучаться до списка, который и нужно пополнять
а потом сохранять все в файл
"""

import json


def write_order_to_json(item, quantity, price, buyer, date):
    data = {"item": item,
        "quantity": str(quantity),
        "price": str(price),
        "buyer": buyer,
        "date": date}
    with open('orders.json', 'a+', encoding='utf-8') as f:
        if f.tell() <= 22:
            f.seek(f.truncate(f.tell() - 4))
            f.write('\n\t\t')
            json.dump(data, f, indent=12, ensure_ascii=False)
            f.write('\n\t]\n}')
        else:
            f.seek(f.truncate(f.tell() - 7))
            f.writelines('\t\t,\n\t\t')
            json.dump(data, f, indent=12, ensure_ascii=False)
            f.writelines('\n\t]\n}')


write_order_to_json('принтер', 20, 1000, 'Petrov P.P.', '20.05.2022')
write_order_to_json('принтер', 20, 1000, 'Petrov P.P.', '20.05.2022')
write_order_to_json('принтер', 20, 1000, 'Petrov P.P.', '20.05.2022')
write_order_to_json('принтер', 20, 1000, 'Petrov P.P.', '20.05.2022')
