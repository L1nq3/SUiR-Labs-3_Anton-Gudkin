from tkinter import *
from string import ascii_uppercase
from PIL import Image, ImageTk
import pygame
import random
import time

def update_frame(ind=0):
    frame = frames[ind]
    gif_label.configure(image=frame)
    gif_label.image = frame 
    next_ind = (ind + 1) % len(frames)
    window.after(50, update_frame, next_ind) 

def closing():
    window.destroy()

def error_check(key):
    global text
    if len(key) != 3:
        text.configure(fg='red')
        ready_text.configure(text='Вы ввели неверное \nколичество символов', fg='red')
        return True
    for i in key:
        if i not in '0123456789':
            text.configure(fg='red')
            ready_text.configure(text='Ключ должен состоять \nтолько из цифр', fg='red')
            return True
    return False

def generation(key):
    global alphabet
    last_part = [random.randint(0, 35) for _ in range(5)]
    iter = 1
    res = []
    for i in range(len(last_part)):
        if last_part[i] > 25:
            last_part[i] += 75
            res.append(last_part[i])
        else:
            res.append(last_part[i])
    for i in key:
        step = int(i)
        iter += 1
        next_part = []
        if iter % 2 == 0:
            for j in range(6-iter):
                next_part.append(last_part[j] + step)
        else:
            for j in range(6-iter):
                next_part.append(last_part[j] - step)
        for x in next_part:
            res.append(x)
        last_part, next_part = next_part, []
    code = []
    for x in res:
        if x > 50:
            code.append(str((x-100)%10))
        else:
            code.append(alphabet[(x-1)%26])
    return code 

def write_key():
    global key, letters
    key = entry.get()
    if error_check(key):
        text.configure(text='Введите 3 цифры --> \n после чего нажмите кнопку \n "Сгенерировать ключ"', 
                       fg='red')

        return 0
    text.configure(text='Ключ сгенерирован', fg='green')
    ready_text.configure(text='Скопируйте ключ --->', fg='green')

    code = generation(key)

    line = 5
    i = 0

    while line >= 1:
        for _ in range(line):
            if i < 17:
                letters[i].configure(text=code[i-(5-line)], fg='green')
                i += 1
        if line > 2:
            letters[i].configure(text='-', fg='green')
            i += 1
        line -= 1
    text_box.config(state='normal')
    text_box.delete("1.0", "end")
    text_box.insert("1.0", ''.join(code))
    text_box.config(state='disabled')

    return 0


window = Tk()
window.title('Генератор ключа')
window.geometry('1250x250')
window.resizable(False, False)

alphabet = list(ascii_uppercase)

grid_frame = Frame(window, bg='white')
grid_frame.place(x=0, y=0, relwidth=0.8, relheight=1)

# ---------------------------------------------- #

gif_path = "sigma.gif"
info = Image.open(gif_path)
frames = []
for i in range(info.n_frames):
    info.seek(i)
    frame = ImageTk.PhotoImage(info.copy())
    frames.append(frame)

gif_label = Label(window)
gif_label.place(x=850, y=0)

update_frame()

# ---------------------------------------------- #

pygame.mixer.init()
pygame.mixer.music.load('music.ogg')
pygame.mixer.music.play(-1)

# ---------------------------------------------- #

bg_image = PhotoImage(file='csgo.png')
background_label = Label(grid_frame, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

step = 0
letters = []
cols = 17
key = ''

for j in range(cols):
    letter_label = Label(grid_frame,
                         text=' ',
                         font=('Consolas', 30),
                         bg='white',
                         width=2)
    letter_label.grid(row=0, column=j, padx=3, pady=3)
    letters.append(letter_label)

btn = Button(grid_frame, text='Сгенерировать ключ', bg='white', fg='black')
btn.grid(row=1, column=12, padx=5, pady=10, columnspan=4)

btn_ex = Button(grid_frame, text='Выход', bg='white', fg='black')
btn_ex.place(x=650, y=130, width=100, height=50)

entry = Entry(grid_frame, textvariable='', bg='white', fg='Black')
entry.grid(row=1, column=7, padx=3, pady=10, columnspan=5)

text_box = Text(grid_frame, height=1, width=18, bg='white', fg='Black', font=('Consolas', 18))
text_box.grid(row=2, column=7, padx=3, pady=10, columnspan=5)

ready_text = Label(grid_frame, text=' '*53, bg='white', fg='black')
ready_text.grid(row=2, column=2, ipadx=4, ipady=3, pady=10, padx=7, columnspan=5)

btn.config(command=write_key)
btn_ex.config(command=closing)

text = Label(grid_frame, text='Введите 3 цифры --> \n после чего нажмите кнопку \n "Сгенерировать ключ"', bg='white', fg='black')
text.grid(row=1, column=2, ipadx=4, ipady=3, pady=10, padx=7, columnspan=5)

window.mainloop()