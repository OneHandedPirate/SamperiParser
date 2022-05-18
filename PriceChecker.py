from tkinter import *
import csv, os
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
                        price.append(float(row[1].strip()))

        font = {'size': 14}
        xticks = [date[0]]
        plt.figure(figsize=(10, 6), num=f'{selected_item}')
        plt.plot(date, price)
        plt.yticks([])
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.13, top=0.92)
        plt.ylabel('Цена', fontdict=font)
        plt.xlabel('Дата', fontdict=font)
        plt.xticks(size=8, rotation=30)
        plt.annotate(price[0], (date[0], price[0]), ha='center', size=8)
        plt.annotate(price[-1], (date[-1], price[-1]), ha='center', size=8)

        for index, pr in enumerate(price):
            if int(index) == 0:
                pass
            elif pr != price[int(index)-1]:
                plt.annotate(pr, (date[int(index)], price[int(index)]), ha='center', size=8)
                xticks.append(date[int(index)])
        xticks.append(date[-1])
        plt.xticks(xticks)
        plt.title(f'{selected_item}')
        plt.show()
    except:
        pass


BG = 'white'
window = Tk()

window.title('SamBeri Price Analyzer')
window.geometry('700x300')
window.resizable(width=False, height=False)
window.iconbitmap('logo1.ico')

canvas = Canvas(window, width=700, height=300)
canvas.pack()

frame = Frame(window, bg=BG)
frame.place(relheight=1, relwidth=1, )
productField = Entry(frame, bg=BG, width=40)
productField.bind('<KeyRelease>', get_product)
productText = Label(frame, text='Введите название продукта', bg=BG)
products = Listbox(frame, bg=BG, selectmode=SINGLE, width=110, height=10)
scrollbar = Scrollbar(products, command=products.yview, width=15)
products.config(yscrollcommand=scrollbar.set)
getButton = Button(frame, text='Построить график', command=get_graph)
logo = PhotoImage(file='logo.png', format='png')
logolabel = Label(frame, image=logo)

logolabel.place(x=80, y=10)
productText.pack()
productField.pack()
getButton.place(x=295, y=50)
products.place(height=200, width=680, x=10, y=90)
scrollbar.pack(side=RIGHT, fill=Y)

window.mainloop()

