from tkinter import *
from fantasy import *
from tkinter import messagebox

players = new_team
Players = new_team_
def batsman_check():
    count = 0
    for i in batsman:
        if players[i].get() != 'Off':
            count += 1
    if count < 5:
        messagebox.showerror('Error' , 'Select ' + str(5 - count) + ' more batsman')
    elif count > 5:
        messagebox.showerror('Error' , 'Deselect the ' + str(count - 5) + ' extra batsman')

def all_rounder_check():
    count = 0
    for i in all_rounders:
        if players[i].get() != 'Off':
            count += 1
    if count < 2:
        messagebox.showerror('Error' , 'Select ' + str(2 - count) + ' more all rounder')
    elif count > 2:
        messagebox.showerror('Error' , 'Deselect the ' + str(count - 2) + ' extra all rounder')

def bowler_check():
    count = 0
    for i in bowlers:
        if players[i].get() != 'Off':
            count += 1
    if count < 4:
        messagebox.showerror('Error' , 'Select ' + str(4 - count) + ' more bowler')
    elif count > 4:
        messagebox.showerror('Error' , 'Deselect the ' + str(count - 4) + ' extra bowler')

def point_calculation():
    window_2 = Toplevel(root)
    window_2.geometry('400x400')
    window_2.title('Your Score')
    frame = Frame(window_2)
    frame.pack()   
    score = 0
    k = 2
    for j in Players:
        if(j!='Off'):

            
            if(players[j].get()!='Off'):
                score += Players[players[j].get()]
                player_name = Label(frame,text=j,font = ('consolas' ,12))
                player_name.grid(sticky = NW , row = k , column = 1)
                points = Label(frame,text=str(Players[players[j].get()]),font = ('consolas' ,12 ))
                points.grid(sticky = NW , row = k , column = 2)
                k += 1

    line = Label(frame , text = '___')
    line.grid( sticky=NW , column=2)
    total_line = Label(frame , text = score , font = ('consolas' ,12))
    total_line.grid(sticky = NW ,column = 2)

root = Tk() 
root.geometry("540x600") 



label = Label(root , text = "select 5 out of 10 batsman...." ,font = ('consolas' ,10 ,'bold') )
label.grid()
j = 0
for i in batsman:
    players[i] = StringVar()
    button = Checkbutton(root , text = i, font = ('consolas' ,12) , variable = players[i] ,onvalue = i , offvalue = 'Off' )
    button.deselect()
    button.grid(sticky = NW , row = j//2 + 1 , column = j % 2)
    j += 1

Button(root, text="Done",command = batsman_check).grid()

label = Label(root , text = "select 2 out of 4 all rounders...." ,font = ('consolas' ,10 ,'bold') )
label.grid()
j += 4
for i in all_rounders:
    players[i] = StringVar()
    button = Checkbutton(root , text = i, font = ('consolas' ,12) , variable = players[i] ,onvalue = i , offvalue = 'Off' )
    button.deselect()
    button.grid(sticky = NW , row = j//2 + 1 , column = j % 2)
    j += 1

Button(root, text="Done",command = all_rounder_check).grid()

label = Label(root , text = "select 4 out of 8 bowlers...." ,font = ('consolas' ,10 ,'bold') )
label.grid()
j += 4
for i in bowlers:
    players[i] = StringVar()
    button = Checkbutton(root , text = i, font = ('consolas' ,12) , variable = players[i] ,onvalue = i , offvalue = 'Off' )
    button.deselect()
    button.grid(sticky = NW , row = j//2 + 1 , column = j % 2)
    j += 1

Button(root, text="Done",command = bowler_check).grid()

Button(root, text="Your Points",command = point_calculation).grid()

mainloop()