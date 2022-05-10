from tkinter import *
import csv, datetime, os
import matplotlib.pyplot as plt


pricelist_dir = os.listdir('data')
current_pricelist = sorted(pricelist_dir, reverse=TRUE)[0]

p = ''
def get_product(event):
    prod = productField.get()
    products.delete(0, END)
    global p
    p += event.char
    results = []
    with open(f'data/{current_pricelist}', encoding='utf-8-sig') as file:
        database = csv.reader(file)
        for row in database:
            if prod == '':
                pass
            elif prod.lower() in row[0].lower():
                results.append(row[0])
    for result in results:
        products.insert(END, result)

def get_graph():
    date = []
    price = []
    try:
        selected_item = products.selection_get()
        for tab in pricelist_dir:
            with open(f'data/{tab}', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == selected_item:
                        date.append(tab.strip('.csv'))
                        price.append(row[1].strip())
        fig, ax = plt.subplots()
        ax.plot(date, price)
        ax.set(xlabel='Date', ylabel='Price', title=f'{selected_item}')
        plt.show()
    except:
        pass

BG = 'light blue'
window = Tk()

window.title('SamBeriPriceChecker')
window.geometry('700x300')
window.resizable(width=False, height=False)

canvas = Canvas(window, width=700, height=300)
canvas.pack()

frame = Frame(window, bg=BG)
frame.place(relheight=1, relwidth=1, )
productField = Entry(frame, bg=BG, width=40)
productField.bind('<KeyRelease>', get_product)
productText = Label(frame, text='Введите название продукта', bg=BG)
products = Listbox(frame, bg=BG, selectmode=SINGLE, width=110, height=10)
scrollbar = Scrollbar(products, command=products.yview)
products.config(yscrollcommand=scrollbar.set)
getButton = Button(frame, text='Построить график', command=get_graph)

productText.pack()
productField.pack()
getButton.place(x=295, y=50)
products.place(height=200, width=680, x=10, y=90)
scrollbar.pack(side=RIGHT, fill=Y)
window.mainloop()

