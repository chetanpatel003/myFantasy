import requests
import bs4
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from functools import partial

def fun(stats):
    arr = [30, 8, 8, 8, 8, 8]
    text = ''
    for i in range(6):
        text += stats[i]
        text += ' ' * (arr[i] - len(stats[i]))
    return text

def live_score(url):
    res = requests.get(url)
    bs = bs4.BeautifulSoup(res.text, 'html.parser')

    scores = bs.select('.cb-col .cb-col-67 .cb-scrs-wrp')
    if not scores:
        messagebox.showinfo('', "Match not started yet...." )
    else:
        window_3 = Toplevel()
        window_3.geometry('500x500')
        frame = Frame(window_3)
        frame.pack()

        # print(scores[0])
        data = scores[0].getText().split('    ')
        # print(data)
        if len(data) > 1:
            data_1 = data[1].split('   ')

            first_line = Label( frame, text=data[0], font=['calibri', 15, 'underline'], foreground='gray' )
            first_line.pack()

            second_line = Label(frame, text=data_1[0], font=('calibri', 17, 'bold'))
            second_line.pack()

            if len(data_1) == 4:
                crr_line = data_1[1].split("\xa0")
                crr_line_1 = data_1[2].split("\xa0")
                crr_line.extend(crr_line_1)

                rates = '  '
                for text in crr_line:
                    rates += text
                    rates += '  '
                crr = Label(frame, text=rates, font=('calibri', 10))
                crr.pack()

                third_line = Label(frame, text=data_1[3], font=('calibri', 12), foreground='red')
                third_line.pack()
            else:
                crr_line = data_1[1].split("\xa0")
                rates = '  '
                for text in crr_line:
                    rates += text
                    rates += '  '
                crr = Label(frame, text=rates, font=('calibri', 10))
                crr.pack()

                third_line = Label(frame, text=data_1[2], font=('calibri', 12), foreground='red')
                third_line.pack()
        else:

            data_1 = data[0].split('   ')
            # print(data_1)
            innings_line = Label(frame, text="First Innings...", font=('calibri', 15, 'underline'), foreground='gray')
            innings_line.pack()

            first_line = Label(frame, text=data_1[1], font=('calibri', 17, 'bold'))
            first_line.pack()

            crr_line = data_1[2].split("\xa0")
            rates = ''
            for text in crr_line:
                if text != ' ':
                    rates += text
            crr = Label(frame, text=rates, font=('calibri', 10))
            crr.pack()

            second_line = Label(frame, text=data_1[3], font=('calibri', 12), foreground='red')
            second_line.pack()

        display = 'Batsman                       R       B       4s      6s      SR      '
        empty_line = Label(frame)
        empty_line.pack()
        empty_line = Label(frame)
        empty_line.pack()
        first_line = Label(frame, text=display, font=('consolas', 10, 'bold'), background='gray')
        first_line.pack()
        # print(url)
        new_url = url.split('-')

        for i in range(len(new_url)):
            if new_url[i] == 'cricket':
                break
        new_url[i + 1] = new_url[i + 1].split('/')
        new_url[i + 1][0] = 'scorecard'
        new_url[i + 1] = '/'.join(new_url[i + 1])
        new_url = '-'.join(new_url)

        # print(new_url)
        res = requests.get(new_url)
        bs_new = bs4.BeautifulSoup(res.text, 'html.parser')

        batting_stats = bs_new.find_all('div', class_="cb-col cb-col-100 cb-scrd-itms")

        for i in batting_stats:
            l = i.getText().split('    ')
            # print(l)
            if len(l) == 2:
                data = [l[0]]
                data.extend(l[1].split('  '))
                # print(data)
                if data[1] == 'batting':
                    stats = [data[0].strip()]
                    stats.extend(data[2].split(' '))
                    text = fun(stats)
                    batsman = Label(frame, text=text, font=('consolas', 10))
                    batsman.pack()
            else:
                break

        display = 'Bowler                         O       M       R       W       ECO     '
        empty_line = Label(frame)
        empty_line.pack()
        first_line = Label(frame, text=display, font=('consolas', 10, 'bold'), background='gray')
        first_line.pack()

        bowlers = bs.find_all('div', class_="cb-col cb-col-50")
        bls = []
        for i in bowlers:
            bls.append(i.getText())
        current_bowlers = bls[4:]

        bowling_stats = bs_new.find_all('div', class_="cb-col cb-col-100 cb-scrd-itms")
        for i in bowling_stats:
            l = i.getText().strip().split('   ')
            if len(l) == 2 and l[0] in current_bowlers:
                data = l[1].split(' ')
                if len(data) == 7:
                    stats = [l[0]]
                    eco = data[-1]
                    stats.extend(data[:4])
                    stats.append(eco)
                    text = fun(stats)
                    bowlers = Label(frame, text=text, font=('consolas', 10))
                    bowlers.pack()

        empty_line = Label(frame)
        empty_line.pack()

        comments = bs.find_all('p')
        # print(comments)
        live_comment = comments[3].getText()
        commentry = Message(frame, text=live_comment, font=('consolas', 12), foreground='blue', aspect='300')
        commentry.pack()


        reload_btn = Button(frame, text="RELOAD", style='W.TButton',
                            command=lambda: [window_3.destroy(), live_score(url)])
        reload_btn.pack()
        window_3.mainloop()


def live_matches(url):
    res = requests.get(url)
    bs = bs4.BeautifulSoup(res.text, 'html.parser')
    links = bs.find_all('a', class_='cb-lv-scrs-well cb-lv-scrs-well-live')

    window_2 = Toplevel(window)
    window_2.geometry('500x500')
    window_2.title('Matches')
    matches = []
    href_links = []
    if links == []:
        messagebox.showinfo(' ', "Oops...\nNo live match available")
    else:
        for i in links:
            link = i.get('href')
            href_links.append(link)
            match = i.get('title')
            matches.append(match)
            btn = Button(window_2, text=match, style='W.TButton' ,
                         command=partial(live_score, 'https://www.cricbuzz.com' + link))
            btn.pack()


window = Tk()
window.geometry('300x80')
window.title("Live Matches")
style = Style()
style.configure('W.TButton', font=
('calibri', 12, 'bold'))

init_btn = Button(window, text='Available Matches', style='W.TButton')
init_btn.bind('<Button>', lambda x: live_matches('https://www.cricbuzz.com/cricket-match/live-scores'))
init_btn.place(relx=0.5, rely=0.2, anchor=CENTER)
window.mainloop()
