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
    print("5. Populiariausia prekė")
    print("6. Daugiausiai pelno sugeneravusi prekė")
    print("7. Ataskaita periode")
    print("8. Išaldyti pinigai")
    print("9. Būsima pardaviminė vertė")
    print("10. Prognozuojamas pelnas viską išpardavus")
    print("11. Išeiti iš programos")
    print("-----------------------------------------------")

def print_items():
    query = "select * from items"
    c.execute(query)
    result = c.fetchall()
    print(result)

def get_item(id):
    query = "select * from items where id = " + id
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


while True:
    print_info()
    opt = input()

    match opt:
        case '1':
            print_items()
        case '2':
            add_item()
        case '3':
            exit(1)