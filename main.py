import mysql.connector
import datetime
import random

conn = mysql.connector.connect(
    host="127.0.0.1",# localhost
    user="root",
    password="",
    database="dmo_shop"
)

c = conn.cursor()

def print_info():
    print("-----------------------------------------------")
    print("1. Prekių atvaizdavimas")
    print("2. Naujos Prekės įkėlimas")
    print("3. Prekės redagavimas")
    print("4. Prekės šalinimas")
    print("5. Pirkti preke")
    print("6. Populiariausia preke")
    print("7. Didziausias vienos prekes pelnas")
    print("8. Statistika")
    print("9. Exit")
    print("10. Prognozuojamas pelnas viską išpardavus")
    print("11. Išeiti iš programos")
    print("-----------------------------------------------")

def print_items():
    query = "select `id`, `title`, `manufacturer_price`, `sale_price`, `quantity` from dmo_items"
    c.execute(query)
    result = c.fetchall()
    for item in result:
        print(f'id:{item[0]}, product: {item[1]}, cost: {item[2]}, buyer_cost: {item[3]}, quantity: {item[4]}')

def get_item(id):
    query = "select * from dmo_items where id = " + id
    c.execute(query)
    res = c.fetchone()
    item = dict(
        id=res[0],
        title=res[1],
        manufacturer_price=res[2],
        sale_price=res[3],
        quantity=res[4]
    )
    return item

def add_item():
    print('Prekes pavadinimas: ')
    title = input()
    print('Tiekejo kaina: ')
    m_price = input()
    print('Pardavimo kaina: ')
    s_price = input()
    print('Prekiu kiekis: ')
    quantity = input()
    query = (f"INSERT INTO `dmo_items`( `title`, `manufacturer_price`, `sale_price`, `quantity`) VALUES (%s, %s, %s, %s)")
    print(query)
    c.execute(query,(title, m_price, s_price, quantity))
    conn.commit()

def edit_item():
    print("Pasirinkite prekes id kuria redaguosite")
    id = input()
    item = get_item(id)
    print(item)
    print("Prekes pavadinimas")
    title1 = input()
    title = title1 if title1 != "" else item['title']
    print("Tiekejo kaina")
    m_price1 = input()
    m_price = m_price1 if m_price1 != "" else item['manufacturer_price']
    print("Pardavimo kaina")
    s_price1 = input()
    s_price = s_price1 if s_price1 != "" else item['sale_price']
    print("Prekiu kiekis")
    quantity1 = input()
    quantity = quantity1 if quantity1 != "" else item['quantity']
    query =  (f"UPDATE `dmo_items` SET `title`=%s,`manufacturer_price`=%s,`sale_price`=%s,`quantity`=%s WHERE `id`= %s;")
    print(query)
    c.execute(query,(title, m_price, s_price, quantity, id))
    conn.commit()

def delete_item():
    print("Pasirinkite prekes id kuria norite salinti")
    id = input()
    query = 'DELETE FROM `dmo_items` WHERE `id` = %s'
    c.execute(query, (id))
    conn.commit()

# def transaction(quantity2):
#     id = which_id()
#     item = get_item(id)
#     print('-------------------------------------------------')
#     print(item)
#     for i in range(0,100):
#         if quantity2 <= item['quantity']:
#             item['quantity'] = item['quantity'] - quantity2
#             print(item['quantity'])
#             print(F'Sekmingai isigijote {quantity2} vienetu/-us')
#             return item['quantity']
#         elif quantity2 > item['quantity']:
#             print('Tiek vienetu neturim')
#             print(f'Turime {item['quantity']} vienetu')
#             print('Kiek noretumet pirkti?')
#             many = int(input())
#             item['quantity'] = item['quantity'] - many
#             return item ['quantity']
#
# def which_id():
#     print('Kuria preke perkate?')
#     id = input()
#     # return id

def random_date(s, e):
    return s + datetime.timedelta(
        seconds=random.randint(0, int((e - s).total_seconds())),
    )


def buy_item():
    print('Kuria preke perkate?')
    id = input()
    # global id
    item = get_item(id)
    print(item)
    print('Kiek perkate vienetu?')
    many = int(input())
    for i in range(0,100):
        if many <= item['quantity']:
            item['quantity'] = item['quantity'] - many
            print(item['quantity'])
            print(F'Sekmingai isigijote {many} vienetu/-us')
            # return item['quantity']
            break
        elif many > item['quantity']:
            print('Tiek vienetu neturim')
            print(f'Turime {item['quantity']} vienetu')
            print('Kiek noretumet pirkti?')
            many = int(input())
            if many > item['quantity']:
                continue
            if many <= item['quantity']:
                item['quantity'] = item['quantity'] - many
                print(f'Sekmingai isigijote {many} vienetu/-us')
                break
    query = (F"UPDATE `dmo_items` SET `quantity`= %s WHERE `id`=%s")
    print(query)
    c.execute(query, (item['quantity'], id))
    conn.commit()
                                                                                                        # transaction(id) tokiu budu galima ji permetineti per funkcijas
    get_item(id)
    item_id = item['id']
    buy_amount = many
    manufacturer_price = item['manufacturer_price']
    sale_price = item['sale_price']
    start = datetime.datetime(2022, 1, 1)
    end = datetime.datetime(2024, 12, 31)
    created_at = random_date(start, end)
    query = ('INSERT INTO `dmo_payments`(`item_id`, `quantity`, `manufacturer_price`, `sale_price`, `created_at`) VALUES (%s, %s, %s, %s, %s)')
    print(query)
    c.execute(query,(item_id, buy_amount, manufacturer_price, sale_price, created_at))
    conn.commit()
    return many


def favorite_item():
    query = (' SELECT item_id, SUM(quantity) AS total_quantity '
             'FROM dmo_payments GROUP BY item_id ORDER BY total_quantity DESC Limit 1; ')
    c.execute(query)
    result = c.fetchone()
    if result:
        item_id, total_quantity = result
        print(f"The most sold item is item_id: {item_id} with a total quantity of {total_quantity} sold.")
    else:
        print("No sales data found.")


def biggest_income_from_one_item():
    query = (' SELECT item_id, SUM(quantity) AS total_quantity, manufacturer_price AS low_cost, sale_price AS high_cost '
             'FROM dmo_payments GROUP BY item_id')
    c.execute(query)
    result = c.fetchall()
    max_profit = 0
    item_of_this_profit = None
    for one in result:
        profit = float((one[3] - one[2]) * one[1])
        # print(f'id:{one[0]}, grynas pelnas:{profit}$')
        if profit > max_profit:
            max_profit = profit
            item_of_this_profit = one[0]
        else:
            continue
    print(f'Item: {item_of_this_profit}, generated income of {max_profit} dollars')

# income = sale_price - manufacturer_price * quantity
# sort by income

def statistics():
    query = (' SELECT item_id, SUM(quantity) AS total_quantity, manufacturer_price, sale_price, created_at '
             'FROM dmo_payments GROUP BY item_id')
    c.execute(query)
    result = c.fetchall()
    data = []
    for item in result:
        answer1 = item[4]
        data.append(answer1)
    print(answer1)

# pasirenkame metus, ir atvaizduojame pamėnesiui pardavimų statistika: kiek prekių parduota, kiek gauta pajamų, koks pelnas?

while True:
    print_info()
    opt = input()

    match opt:
        case '1':
            print_items()
        case '2':
            add_item()
        case '3':
            edit_item()
        case '4':
            delete_item()
        case '5':
            buy_item()
        case '6':
            favorite_item()
        case '7':
            biggest_income_from_one_item()
        case '8':
            statistics()
        case '9':
            exit(1)