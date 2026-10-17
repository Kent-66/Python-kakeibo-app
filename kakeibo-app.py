import tkinter as tk
from datetime import date
import calendar

window = tk.Tk()
window.title("家計簿アプリ")
window.geometry("400x800")

month_frame = tk.Frame(window)
month_frame.pack()

prev_button = tk.Button(month_frame, text = "◀ 前月", command = lambda: change_month(-1))
prev_button.pack(side = "left")

month_label = tk.Label(month_frame, text = "2026年10月", width = 12)
month_label.pack(side = "left")

next_button = tk.Button(month_frame, text = "次月 ▶", command = lambda: change_month(1))
next_button.pack(side = "left")

calendar_frame = tk.Frame(window)
calendar_frame.pack()

selected_date_label = tk.Label(window, text = "日付を選択してください")
selected_date_label.pack()

expenses = []
selected_date = None

current_year = 2026
current_month = 10


#日付を選択する関数
def select_date(day):
    global selected_date
    global current_year
    global current_month

    year = current_year
    month = current_month

    selected_date = date(year, month, day)

    selected_date_label.config(text = f"選択した日付：{day}日")

    show_selected_expenses()

    show_calendar()


#選択した日付の支出一覧を表示する関数
def show_selected_expenses():
    expenses_list.delete(0, tk.END)

    for expense in expenses:
        if expense[0] == selected_date:
            expenses_list.insert(tk.END, expense)

            

def change_month(diff):
    global current_year, current_month

    current_month += diff

    if current_month > 12:
        current_month = 1
        current_year += 1
    elif current_month < 1:
        current_month = 12
        current_year -= 1

    month_label.config(text = f"{current_year}年{current_month}月")
    
    show_calendar()

#カレンダーを表示する関数
def show_calendar():
    weekdays = ["日","月","火","水","木","金","土"]

    for col, weekday in enumerate(weekdays):
        label = tk.Label(
            calendar_frame,
            text = weekday,
            width = 4
        )
        label.grid(row = 0, column = col)

    year = current_year
    month = current_month

    calendar.setfirstweekday(calendar.SUNDAY)

    cal = calendar.monthcalendar(year, month)

    for row, week in enumerate(cal):
        for col, day in enumerate(week):
            
            if day == 0:
                button = tk.Label(calendar_frame, text = "", width = 5, height = 2)   #存在しない日(0日)は空白にする
            else:
                check_date = date(year, month, day)

                total = 0

                for expense in expenses:
                    if expense[0] == check_date:
                        total += expense[1]

                has_expense = total > 0

                if has_expense:
                    text = f"{day}\n￥{total}"
                else:
                    text = str(day)

                button = tk.Button(
                    calendar_frame,
                    text = text,
                    width = 5,
                    height = 2,
                    bg = "lightblue" if selected_date == date(year, month, day) else "white",
                    command = lambda d = day: select_date(d)
                    )

            button.grid(row = row + 1, column = col)
            

label = tk.Label(window, text = "====== 家計簿 =====")
label.pack()

money_label = tk.Label(window, text = "支出額を入力して下さい")
money_label.pack()

money_entry = tk.Entry(window)
money_entry.pack()

category_label = tk.Label(window, text = "カテゴリを入力して下さい")
category_label.pack()

category_entry = tk.Entry(window)
category_entry.pack()

memo_label = tk.Label(window, text = "メモを入力して下さい")
memo_label.pack()

memo_entry = tk.Entry(window)
memo_entry.pack()

expenses_list  = tk.Listbox(window, width = 30, height = 10)
expenses_list.pack()

#支出を登録する関数
def add_expense():
    if selected_date is None:
        selected_date_label.config(text = "先にカレンダーから日付を選んでください")
        
        return
    
    money = int(money_entry.get())
    category = category_entry.get()
    memo = memo_entry.get()

    expenses.append([selected_date, money, category, memo])
    
    show_selected_expenses()
    show_calendar()

    money_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    memo_entry.delete(0, tk.END)

#支出を削除する関数
def del_expense():
    selected = expenses_list.curselection()

    if selected:
        expenses_list.delete(selected)
    else:
        select_label = tk.Label(window, text = "削除する支出を選択して下さい")
        select_label.pack()

#支出登録ボタン
add_button = tk.Button(window, text = "支出を登録", command = add_expense)
add_button.pack()

#支出削除ボタン
del_button = tk.Button(window, text = "支出を削除", command = del_expense)
del_button.pack()

show_calendar()
window.mainloop()
