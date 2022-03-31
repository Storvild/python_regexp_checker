from tkinter import *
from tkinter import messagebox
import re
import json

SRE_FLAG_TEMPLATE = 1 # template mode (disable backtracking)
SRE_FLAG_IGNORECASE = 2 # case insensitive
SRE_FLAG_LOCALE = 4 # honour system locale
SRE_FLAG_MULTILINE = 8 # treat target as multiline string
SRE_FLAG_DOTALL = 16 # treat target as a single string
SRE_FLAG_UNICODE = 32 # use unicode "locale"
SRE_FLAG_VERBOSE = 64 # ignore whitespace and comments
SRE_FLAG_DEBUG = 128 # debugging
SRE_FLAG_ASCII = 256 # use ascii "locale"

EXAMPLE_TEXT = 'My 123 Test 456'
EXAMPLE_PATTERN = 'My (?P<first>\d+) T(.?)st (?P<second>\d+)'

def exec_pattern(event):
    try:
        search_res = re.search(get_pattern(), get_source(), get_ignorecase() | get_dotall() | get_multiline())
        #result = search_res.groupdict()
        #result = search_res.groups()
        result = search_res
        if result:
            set_result(result)
            add_result('groups ({}):'.format(len(result.groups())))
            add_result(result.groups())
            add_result('groupdict ({}):'.format(len(result.groupdict())))
            group_dict = json.dumps(result.groupdict(), ensure_ascii=False, indent=4)
            #group_dict = result.groupdict()
            add_result(group_dict)
            #text_result.insert(1.0, result)
        else:
            set_result('ДАННЫЕ НЕ НАЙДЕНЫ!')
            #text_result.delete(1.0, END)
            #text_result.insert(1.0, 'Данные не неайдены!')
            print(result)
    except Exception as e:
        set_result('ОШИБКА:')
        add_result(e)
        #text_result.delete(1.0, END)
        #text_result.insert(1.0, e)

    

def but_test():
    exec_pattern(None)
    #messagebox.showinfo("GUI Python", text_pattern.get(1.0, END))
    #text_source.insert(1.0, 'text')
    #text_source.delete(1.0, END)


 
root = Tk()
root.title("GUI на Python")
#root.geometry("300x250")
root.event_add('<<Paste>>', '<Control-igrave>')  # По умолчанию в русской раскладке Ctrl+м не работает
root.event_add("<<Copy>>", "<Control-ntilde>")  # По умолчанию в русской раскладке Ctrl+с не работает
root.event_add("<<Cut>>", "<Control-division>") # <<Cut>> Ctrl+с 0247 division
root.event_add("<<Undo>>", "<Control-ydiaeresis>") #<<Undo>> Ctrl+z Ctrl+я 0255 ydiaeresis
#https://ru.stackoverflow.com/questions/816947/Почему-с-rus-раскладкой-ctrv-и-ctrc-не-работает-а-с-eng-все-работаетtkinter


#message = StringVar()
frame1 = Frame(bg='yellow')
frame1.pack(fill=BOTH)

def get_source():
    return text_source.get(1.0, END).strip()

text_source = Text(frame1, height=10, bg='#EEE')
text_source.pack(side=TOP, fill=BOTH, expand=1) #anchor=SE
#scroll1 = Scrollbar(frame1, command=text_source.yview)
#scroll1.pack(side=RIGHT, expand=0.1)
#text_source.config(yscrollcommand=scroll1.set)
text_source.bind('<KeyRelease>', exec_pattern)

def get_pattern():
    return text_pattern.get(1.0, END).strip()

text_pattern = Text(height=6)
text_pattern.pack(side=TOP, fill=BOTH, expand=1)
#text_pattern.bind('<Key>', exec_pattern)
#text_pattern.bind('<KeyPress>', exec_pattern)
text_pattern.bind('<KeyRelease>', exec_pattern)
text_pattern.focus_set()

frame_buttons = Frame() #bg='gray'
frame_buttons.pack(fill=Y)
but1 = Button(frame_buttons, text='RUN CHECK', command=but_test)
but1.pack(side=LEFT, expand=1)

var_multiline = BooleanVar()
cb_multiline = Checkbutton(frame_buttons, text='MULTILINE', variable=var_multiline, onvalue=SRE_FLAG_MULTILINE, offvalue=0)
cb_multiline.pack(side=RIGHT)
cb_multiline.select()

var_ignorecase = BooleanVar()
cb_ignorecase = Checkbutton(frame_buttons, text='IGNORECASE', variable=var_ignorecase, onvalue=SRE_FLAG_IGNORECASE, offvalue=0)
cb_ignorecase.pack(side=RIGHT)
cb_ignorecase.select()
#var_ignorecase.set(0)

var_dotall = BooleanVar()
cb_dotall = Checkbutton(frame_buttons, text='DOTALL', variable=var_dotall, onvalue=SRE_FLAG_DOTALL, offvalue=0)
cb_dotall.pack(side=RIGHT)
cb_dotall.select()

def get_multiline():
    if var_multiline.get():
        return re.MULTILINE
    else:
        return 0

def get_ignorecase():
    if var_ignorecase.get():
        return re.IGNORECASE
    else:
        return 0

def get_dotall():
    if var_dotall.get():
        return re.DOTALL
    else:
        return 0

def set_wordwrap():
    if var_wordwrap.get():
        text_source.config(wrap=WORD)
    else:
        text_source.config(wrap=NONE)
    #messagebox.showinfo("GUI Python", 'TEST')

var_wordwrap = BooleanVar()
cb_wordwrap = Checkbutton(frame_buttons, text='WordWrap', variable=var_wordwrap, onvalue=1, offvalue=0, command=set_wordwrap)
cb_wordwrap.pack(side=RIGHT)
cb_wordwrap.select()


def set_result(var):
    text_result.delete(1.0, END)
    text_result.insert(1.0, var)

def add_result(var):
    text_result.insert(END, '\n')
    text_result.insert(END, var)

text_result = Text(height=10, fg='black', bg='#DDD')
text_result.pack(side=TOP, fill=BOTH, expand=1)


#message = StringVar()
#message_entry = Entry(textvariable=message)
#message_entry.place(relx=.5, rely=.1, anchor="c")
#message_button = Button(text="Click Me", command=show_message)
#message_button.place(relx=.5, rely=.5, anchor="c")

# Контекстное меню
def func(event):
    root.menu.post(event.x_root, event.y_root)
    root.w = event.widget

root.menu = Menu(tearoff=0)
root.menu.add_command(label="Вырезать", accelerator="Ctrl+X",
                       command=lambda: root.w.focus_force() or root.w.event_generate("<<Cut>>"))
root.menu.add_command(label="Копировать", accelerator="Ctrl+С",
                         command=lambda: root.w.focus_force() or root.w.event_generate("<<Copy>>"))
root.menu.add_command(label="Вставить", accelerator="Ctrl+V",
                        command=lambda: root.w.focus_force() or root.w.event_generate("<<Paste>>"))
root.menu.add_command(label="Удалить", accelerator="Delete",
                        command=lambda: root.w.focus_force() or root.w.event_generate("<<Clear>>"))
root.menu.add_separator()
root.menu.add_command(label="Выделить все", accelerator="Ctrl+A",
                      command=lambda: root.w.focus_force() or root.w.event_generate("<<SelectAll>>"))
text_source.bind("<Button-3>", func)
text_pattern.bind("<Button-3>", func)
# Конец Контекстное меню

# ВСТАВКА ПРИМЕРА
text_source.insert(1.0, EXAMPLE_TEXT)
text_pattern.insert(1.0, EXAMPLE_PATTERN)
exec_pattern(None)


root.mainloop()

# Не работает вставка через Ctrl+V
# Нет контекстного меню Вставить, Скопировать
# Не работает Ctrl+F
