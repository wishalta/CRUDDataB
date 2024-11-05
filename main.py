import mysql.connector

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
    print("6. Daugiausiai pelno sugeneravusi prekė")
    print("7. Ataskaita periode")
    print("8. Išaldyti pinigai")
    print("9. Būsima pardaviminė vertė")
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

def buy_item():
    print('Kuria preke perkate?')
    id = input()
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
            item['quantity'] = item['quantity'] - many
            if many > item['quantity']:
                continue
            if many <= item['quantity']:
                print(f'Sekmingai isigijote {many} vienetu/-us')
                break
    query = (F"UPDATE `dmo_items` SET `quantity`= %s WHERE `id`=%s")
    print(query)
    c.execute(query, (item['quantity'], id))
    conn.commit()


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
            exit(1)