from tkinter import *
from pygame import mixer

# ---------------------------- CONSTANTS ------------------------------- #
SOUND_FILE = 'beep-07a.wav'

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#2D8D91"
YELLOW = "#D8D1CF"
DARK_GREEN = "#11322E"
FONT_NAME = "Courier"

TOP_TEXT = 'NinjaTim3r'
WORK_TEXT = 'W0rk!'
SHORT_BREAK_TEXT = 'Str3tch'
LONG_BREAK_TEXT = 'Br34k'
PAUSED_TEXT = 'Paused'

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

loop_reps = 0
timer = None
paused = False
remaining_sec = 0
text_before_pause = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global loop_reps
    global paused
    global remaining_sec
    global text_before_pause

    loop_reps = 0
    paused = False
    remaining_sec = 0
    text_before_pause = None

    window.after_cancel(timer)
    ninjatimer_text.config(text=TOP_TEXT, fg=GREEN)
    canvas.itemconfig(timer_count, text="00:00")
    start_button.config(text="Start", state="normal")
    pause_button.config(text="Pause", state="disabled")
    reset_button.config(state="disabled")

# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    start_button.config(state="disabled")
    pause_button.config(state="normal")
    reset_button.config(state="normal")

    global loop_reps
    loop_reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if loop_reps % 8 == 0:
        ninjatimer_text.config(text=LONG_BREAK_TEXT, fg=RED)
        countdown(long_break_sec)
    elif loop_reps % 2 == 0:
        ninjatimer_text.config(text=SHORT_BREAK_TEXT, fg=PINK)
        countdown(short_break_sec)
    else:
        ninjatimer_text.config(text=WORK_TEXT, fg=GREEN)
        countdown(work_sec)

def pause_timer():
    global text_before_pause
    global paused
    paused = True

    if pause_button.cget('text') == "Pause":
        text_before_pause = ninjatimer_text.cget('text')
        pause_button.config(text="Continue")
        ninjatimer_text.config(text=PAUSED_TEXT, fg=PINK)
    else:
        pause_button.config(text="Pause")
        paused = False
        if text_before_pause == WORK_TEXT:
            ninjatimer_text.config(text=WORK_TEXT, fg=GREEN)
        elif text_before_pause == SHORT_BREAK_TEXT:
            ninjatimer_text.config(text=SHORT_BREAK_TEXT, fg=PINK)
        else:
            ninjatimer_text.config(text=LONG_BREAK_TEXT, fg=RED)
        countdown(remaining_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def countdown(session_time):
    if session_time > 0:
        global timer
        if not paused:
            minutes = int(session_time / 60)
            second = int(session_time % 60)
            countdown_text = f"{format(minutes, '02d')}:{format(second, '02d')}"
            canvas.itemconfig(timer_count, text=countdown_text)
            timer = window.after(1000, countdown, session_time - 1)
            print(f"session time: {session_time}")

            if session_time <= 5:
                beep_sound.play()
        else:
            global remaining_sec
            remaining_sec = session_time
    else:
        start_timer()

# ---------------------------- UI SETUP ------------------------------- #

mixer.init()
beep_sound = mixer.Sound(SOUND_FILE)

window = Tk()
window.title("Ninja Tim3r")
window.config(padx=100, pady=50, bg=YELLOW)
canvas = Canvas(width=335, height=240, bg=YELLOW, highlightthickness=0)
ninja_img = PhotoImage(file="ninja-study.png")
canvas.create_image(170,112, image=ninja_img)
timer_count = canvas.create_text(285, 100, text="00:00", fill=DARK_GREEN, font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

ninjatimer_text = Label(text=TOP_TEXT, font=(FONT_NAME, 50, "bold"))
ninjatimer_text.config(fg=GREEN, bg=YELLOW)
ninjatimer_text.grid(row=0, column=1)

start_button = Button(text="Start", command=start_timer, highlightbackground=YELLOW)
start_button.config(padx=3, pady=3)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", command=reset_timer, highlightbackground=YELLOW)
reset_button.config(padx=3, pady=3, state="disabled")
reset_button.grid(row=2, column=2)

pause_button = Button(text="Pause", command=pause_timer, highlightbackground=YELLOW)
pause_button.config(padx=3, pady=3, state="disabled")
pause_button.grid(row=2, column=1)

window.mainloop()