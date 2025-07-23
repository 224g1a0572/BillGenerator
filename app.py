from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

menu = {
    "Starters": [
        ("Paneer Tikka", 150, "Grilled paneer cubes", "panner.jpg"),
        ("Veg Manchurian", 130, "Crispy veggie balls", "manchurian.jpg"),
        ("Spring Rolls", 100, "Crispy rolls with veggies", "springroll.jpg"),
        ("Soup", 80, "Hot & sour soup", "soup.jfif")
    ],
    "North Indian": [
        ("Butter Chicken", 250, "Creamy chicken curry", "butterchicken.jpg"),
        ("Dal Makhani", 150, "Black lentils in butter", "dalmakhani.jfif"),
        ("Chole Bhature", 120, "Spicy chickpeas with fried bread", "chole.jfif"),
        ("Naan", 30, "Tandoori flatbread", "naan.jfif")
    ],
    "South Indian": [
        ("Idli", 40, "Steamed rice cakes", "idli.jfif"),
        ("Masala Dosa", 60, "Dosa with potato filling", "dosa.jfif"),
        ("Vada", 35, "Fried savory donut", "vada.jfif"),
        ("Uttapam", 50, "Veg pancake", "utappam.jfif")
    ],
    "Desserts": [
        ("Gulab Jamun", 50, "Fried sweet balls", "gulabjamun.jfif"),
        ("Rasgulla", 45, "Syrupy cottage balls", "rasgulla.jfif"),
        ("Ice Cream", 60, "Vanilla scoop", "icecream.jfif"),
        ("Brownie", 70, "Chocolate cake", "brownie.jfif")
    ],
    "Sweets": [
        ("Ladoo", 40, "Boondi ladoo", "ladoo.jfif"),
        ("Barfi", 45, "Milk sweet", "barfi.jfif"),
        ("Halwa", 50, "Carrot halwa", "halwa.jfif"),
        ("Kaju Katli", 60, "Cashew sweet", "kaju.jfif")
    ],
    "Ice Cream": [
        ("Vanilla", 40, "Classic vanilla", "vanilla.webp"),
        ("Strawberry", 45, "Strawberry delight", "strawberry.jpg"),
        ("Chocolate", 50, "Choco swirl", "chocolate.jfif"),
        ("Butterscotch", 55, "Nutty delight", "butterscotch.jfif")
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu', methods=['POST'])
def menu_page():
    customer_name = request.form['customer_name']
    phone = request.form['phone']
    table_no = request.form['table_no']
    return render_template('menu.html', menu=menu, customer_name=customer_name, phone=phone, table_no=table_no)

@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    customer_name = request.form['customer_name']
    phone = request.form['phone']
    table_no = request.form['table_no']
    
    selected_items = []
    total = 0

    for category, items in menu.items():
        for item in items:
            name, price, desc, img = item
            if request.form.get(name):
                qty = int(request.form.get(f"{name}_qty", 1))
                amount = price * qty
                selected_items.append((name, price, qty, amount))
                total += amount

    gst = round(total * 0.05, 2)
    grand_total = total + gst

    # Save to database
    conn = sqlite3.connect('bill.db')
    c = conn.cursor()
    for item in selected_items:
        c.execute("INSERT INTO bills (customer_name, phone, table_no, item, price, qty, amount) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                  (customer_name, phone, table_no, item[0], item[1], item[2], item[3]))
    conn.commit()
    conn.close()

    return render_template('bill.html', customer_name=customer_name, phone=phone, table_no=table_no,
                           items=selected_items, total=total, gst=gst, grand_total=grand_total)

if __name__ == '__main__':
     port = int(os.environ.get("PORT", 10000))
     app.run(host="0.0.0.0", port=port)
