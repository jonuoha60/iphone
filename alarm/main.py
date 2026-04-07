from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk
import time
import pygame
from utils.convert import convert_to_24hr

pygame.mixer.init()
alarm_sound = pygame.mixer.Sound("../alarm/audio/alarm.mp3")

BACKGROUND_COLOR = "#F5F5F7"     
CARD_COLOR = "#FFFFFF"             
PRIMARY_COLOR = "#007AFF"           
TEXT_PRIMARY = "#000000"            
TEXT_SECONDARY = "#86868B"          
BUTTON_COLOR = "#007AFF"            
BUTTON_HOVER = "#0051D5"            

window = Tk()
window.configure(bg=BACKGROUND_COLOR)
notebook = ttk.Notebook(window)
window.geometry("600x700")
window.title("Alarm Clock")

style = ttk.Style()
style.theme_use('clam')
style.configure('TNotebook', background=BACKGROUND_COLOR, borderwidth=0)
style.configure('TNotebook.Tab', padding=[20, 10], background=BACKGROUND_COLOR)
style.map('TNotebook.Tab', background=[('selected', CARD_COLOR)])
style.configure('TCombobox', fieldbackground=CARD_COLOR, background=CARD_COLOR)

tab1 = Frame(notebook, bg=BACKGROUND_COLOR)
tab2 = Frame(notebook, bg=BACKGROUND_COLOR)
notebook.add(tab1, text="Alarm")
notebook.add(tab2, text="Timer")
notebook.pack(expand=True, fill="both")

icon = PhotoImage(file="../alarm/asset/alarm.png")
window.iconphoto(True, icon)

menubar = Menu(window)
window.config(menu=menubar)
clockMenu = Menu(menubar, tearoff=0)
clockMenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=clockMenu)

# ============= ALARM TAB =============
# Current time display
label = Label(tab1, text=time.strftime("%I:%M:%S %p"), font=("Arial", 42), 
              fg=TEXT_PRIMARY, bg=BACKGROUND_COLOR)
label.pack(pady=30)

# Current day display
now = datetime.now()
day = datetime.now().weekday()
year = datetime.now().year
hours_time = datetime.now().hour
minute_time = datetime.now().minute
seconds_time = datetime.now().second
month = datetime.now().month
ampm = datetime.now().strftime("%p")

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_label = Label(tab1, text=f"Current day: {days_of_week[day]}", font=("Arial", 13), 
                  fg=TEXT_SECONDARY, bg=BACKGROUND_COLOR)
day_label.pack(pady=10)

# Create a card-style frame for alarm settings
card_frame = Frame(tab1, bg=CARD_COLOR, highlightthickness=1, highlightbackground="#E5E5E7")
card_frame.pack(padx=20, pady=20, fill="both", expand=True)

title_label = Label(card_frame, text="Set your alarm time", font=("Arial", 14, "bold"), 
                   fg=TEXT_PRIMARY, bg=CARD_COLOR)
title_label.pack(pady=(20, 10))

# Combobox values
hours = [f"{i:02d}" for i in range(1, 13)]
minute = [f"{i:02d}" for i in range(60)]
seconds = [f"{i:02d}" for i in range(60)]
ampm_values = ["AM", "PM"]

# Day selection
day_label_input = Label(card_frame, text="Day", font=("Arial", 12), 
                       fg=TEXT_SECONDARY, bg=CARD_COLOR)
day_label_input.pack(anchor="w", padx=20, pady=(10, 5))

cb_day = ttk.Combobox(card_frame, values=days_of_week, state="readonly", font=("Arial", 11))
cb_day.current(day)
cb_day.pack(padx=20, pady=5, fill="x")


time_frame = Frame(card_frame, bg=CARD_COLOR)
time_frame.pack(padx=20, pady=15, fill="x")

# Hour
hour_label = Label(time_frame, text="Hour", font=("Arial", 12), 
                  fg=TEXT_SECONDARY, bg=CARD_COLOR)
hour_label.grid(row=0, column=0, padx=5, sticky="w")

hours_values = [f"{i:02d}" for i in range(1, 13)]
current_12hr = hours_time % 12 if hours_time % 12 != 0 else 12
cb = ttk.Combobox(time_frame, values=hours_values, state="readonly", font=("Arial", 11), width=5)
cb.current(current_12hr - 1)
cb.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# Minute
minute_label = Label(time_frame, text="Minute", font=("Arial", 12), 
                    fg=TEXT_SECONDARY, bg=CARD_COLOR)
minute_label.grid(row=0, column=1, padx=5, sticky="w")

cb2 = ttk.Combobox(time_frame, values=minute, state="readonly", font=("Arial", 11), width=5)
cb2.current(minute_time)
cb2.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Second
second_label = Label(time_frame, text="Second", font=("Arial", 12), 
                    fg=TEXT_SECONDARY, bg=CARD_COLOR)
second_label.grid(row=0, column=2, padx=5, sticky="w")

cb3 = ttk.Combobox(time_frame, values=seconds, state="readonly", font=("Arial", 11), width=5)
cb3.current(seconds_time)
cb3.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

# AM/PM
ampm_label = Label(time_frame, text="AM/PM", font=("Arial", 12), 
                  fg=TEXT_SECONDARY, bg=CARD_COLOR)
ampm_label.grid(row=0, column=3, padx=5, sticky="w")

cb4 = ttk.Combobox(time_frame, values=ampm_values, state="readonly", font=("Arial", 11), width=5)
cb4.current(0 if ampm == "AM" else 1)
cb4.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

time_frame.columnconfigure((0, 1, 2, 3), weight=1)

# Status label
label3 = Label(card_frame, text="00:00:00", font=("Arial", 12), 
              fg=PRIMARY_COLOR, bg=CARD_COLOR, wraplength=300)
label3.pack(pady=10)

label4 = Label(card_frame, text="The alarm needs to be in the future.", font=("Arial", 10), 
              fg="#FF3B30", bg=CARD_COLOR, state="disabled")
label4.pack(pady=5)

# Buttons frame
frame = Frame(tab1, bg=BACKGROUND_COLOR)
frame.pack(side=BOTTOM, pady=20)

def stop_alarm():
    global alarm_triggered
    alarm_sound.stop()
    alarm_triggered = False
    set_alarm_button.config(state="normal", bg=BUTTON_COLOR)
    stop_alarm_button.config(state="disabled", bg="#CCCCCC")
    label3.config(text="00:00:00")
    print("Alarm stopped")

alarm_triggered = False

def update_clock():
    global alarm_triggered
    window.after(1000, update_clock)
    current_time = time.strftime("%I:%M:%S %p")
    day_selected = cb_day.get()
    hour = cb.get()
    minute = cb2.get()
    seconds = cb3.get()
    ampm_value = cb4.get()

    hour_24 = convert_to_24hr(hour, ampm_value)
    full_time = f"{hour}:{minute}:{seconds} {ampm_value}"
    label.config(text=current_time)

    target_datetime = datetime(year, month, datetime.now().day, hour_24, int(minute), int(seconds))

    if now > target_datetime:
        label4.config(state="normal")
        set_alarm_button.config(state="disabled", bg="#CCCCCC")
    else:
        label4.config(state="disabled")
        set_alarm_button.config(state="normal", bg=BUTTON_COLOR)
        label3.config(text=f"Alarm set for:\n{day_selected} {full_time}\n{year}/{month}/{datetime.now().day}")

    current_time_no_ampm = time.strftime("%H:%M:%S")
    target_time = f"{hour_24:02d}:{minute}:{seconds}"
    
    if current_time_no_ampm == target_time and datetime.now().weekday() == days_of_week.index(day_selected) and not alarm_triggered:
        alarm_sound.play()
        label3.config(text="Alarm is ringing!", fg="#FF3B30")
        set_alarm_button.config(state="disabled", bg="#CCCCCC")
        stop_alarm_button.config(state="normal", bg="#FF3B30")
        alarm_triggered = True
        print("Alarm is ringing")

def real_time():
    label.config(text=time.strftime("%I:%M:%S %p"))
    window.after(1000, real_time)

window.after(1000, real_time)

set_alarm_button = Button(frame, text="Set Alarm", font=("Arial", 14, "bold"), 
                         bg=BUTTON_COLOR, fg="white", command=update_clock, 
                         padx=20, pady=10, relief=FLAT, cursor="hand2",
                         activebackground=BUTTON_HOVER, activeforeground="white")
set_alarm_button.pack(side=RIGHT, padx=5)

stop_alarm_button = Button(frame, text="Stop Alarm", font=("Arial", 14, "bold"), 
                          bg="#CCCCCC", fg="white", command=stop_alarm, 
                          padx=20, pady=10, relief=FLAT, cursor="hand2", state="disabled",
                          activebackground="#B0B0B0", activeforeground="white")
stop_alarm_button.pack(side=RIGHT, padx=5)

# ============= TIMER TAB =============
label_timer = Label(tab2, text=time.strftime("%I:%M:%S %p"), font=("Arial", 42),
                   fg=TEXT_PRIMARY, bg=BACKGROUND_COLOR)
label_timer.pack(pady=30)

label_timer2 = Label(tab2, text="Set your timer duration", font=("Arial", 14, "bold"),
                    fg=TEXT_PRIMARY, bg=BACKGROUND_COLOR)
label_timer2.pack(pady=10)


timer_card = Frame(tab2, bg=CARD_COLOR, highlightthickness=1, highlightbackground="#E5E5E7")
timer_card.pack(padx=20, pady=20, fill="both", expand=True)

# Timer inputs
hours_timer = [f"{i:02d}" for i in range(24)]
minute_timer = [f"{i:02d}" for i in range(60)]
seconds_timer = [f"{i:02d}" for i in range(60)]

timer_frame = Frame(timer_card, bg=CARD_COLOR)
timer_frame.pack(padx=20, pady=20, fill="x")

# Timer hour
timer_hour_label = Label(timer_frame, text="Hours", font=("Arial", 12),
                        fg=TEXT_SECONDARY, bg=CARD_COLOR)
timer_hour_label.grid(row=0, column=0, padx=5, sticky="w")

cb_timer_hours = ttk.Combobox(timer_frame, values=hours_timer, state="readonly", 
                             font=("Arial", 11), width=5)
cb_timer_hours.current(0)
cb_timer_hours.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# Timer minutes
timer_min_label = Label(timer_frame, text="Minutes", font=("Arial", 12),
                       fg=TEXT_SECONDARY, bg=CARD_COLOR)
timer_min_label.grid(row=0, column=1, padx=5, sticky="w")

cb_timer_minutes = ttk.Combobox(timer_frame, values=minute_timer, state="readonly",
                               font=("Arial", 11), width=5)
cb_timer_minutes.current(0)
cb_timer_minutes.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

timer_sec_label = Label(timer_frame, text="Seconds", font=("Arial", 12),
                       fg=TEXT_SECONDARY, bg=CARD_COLOR)
timer_sec_label.grid(row=0, column=2, padx=5, sticky="w")

cb_timer_seconds = ttk.Combobox(timer_frame, values=seconds_timer, state="readonly",
                               font=("Arial", 11), width=5)
cb_timer_seconds.current(0)
cb_timer_seconds.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

timer_frame.columnconfigure((0, 1, 2), weight=1)

label_timer3 = Label(timer_card, text="00:00:00", font=("Arial", 14),
                    fg=PRIMARY_COLOR, bg=CARD_COLOR)
label_timer3.pack(pady=20)

# Timer state variables
timer_running = False
timer_paused = False
remaining_seconds = 0

def set_timer():
    global timer_running, timer_paused, remaining_seconds
    
    hours = int(cb_timer_hours.get())
    minutes = int(cb_timer_minutes.get())
    seconds = int(cb_timer_seconds.get())
    
    if hours == 0 and minutes == 0 and seconds == 0:
        label_timer3.config(text="Please set a duration for the timer.", fg="#FF3B30")
        return
    
    remaining_seconds = hours * 3600 + minutes * 60 + seconds
    timer_running = True
    timer_paused = False
    label_timer3.config(text=f"Timer set for {hours:02d}:{minutes:02d}:{seconds:02d}", fg=PRIMARY_COLOR)
    set_timer_button.config(state="disabled", bg="#CCCCCC")
    stop_timer_button.config(state="normal", bg="#FF3B30")
    cb_timer_hours.config(state="disabled")
    cb_timer_minutes.config(state="disabled")
    cb_timer_seconds.config(state="disabled")
    countdown_timer()

def stop_timer():
    global timer_running, remaining_seconds
    
    timer_running = False
    alarm_sound.stop()
    label_timer3.config(text="00:00:00", fg=PRIMARY_COLOR)
    set_timer_button.config(state="normal", bg=BUTTON_COLOR)
    stop_timer_button.config(state="disabled", bg="#CCCCCC")
    cb_timer_hours.config(state="readonly")
    cb_timer_minutes.config(state="readonly")
    cb_timer_seconds.config(state="readonly")
    remaining_seconds = 0
    print("Timer stopped")

def countdown_timer():
    global timer_running, remaining_seconds
    
    if timer_running and remaining_seconds > 0:
        remaining_seconds -= 1
        mins, secs = divmod(remaining_seconds, 60)
        hrs, mins = divmod(mins, 60)
        timer_format = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        label_timer3.config(text=timer_format)
        window.after(1000, countdown_timer)
    elif timer_running and remaining_seconds == 0:
        timer_running = False
        label_timer3.config(text="Timer finished!", fg="#FF3B30")
        alarm_sound.play()
        set_timer_button.config(state="normal", bg=BUTTON_COLOR)
        stop_timer_button.config(state="disabled", bg="#CCCCCC")
        cb_timer_hours.config(state="readonly")
        cb_timer_minutes.config(state="readonly")
        cb_timer_seconds.config(state="readonly")
        print("Timer finished")

# Buttons frame for timer
timer_buttons_frame = Frame(tab2, bg=BACKGROUND_COLOR)
timer_buttons_frame.pack(side=BOTTOM, pady=20)

set_timer_button = Button(timer_buttons_frame, text="Set Timer", font=("Arial", 14, "bold"),
                         bg=BUTTON_COLOR, fg="white", command=set_timer,
                         padx=20, pady=10, relief=FLAT, cursor="hand2",
                         activebackground=BUTTON_HOVER, activeforeground="white")
set_timer_button.pack(side=LEFT, padx=5)

stop_timer_button = Button(timer_buttons_frame, text="Stop Timer", font=("Arial", 14, "bold"),
                          bg="#CCCCCC", fg="white", command=stop_timer,
                          padx=20, pady=10, relief=FLAT, cursor="hand2", state="disabled",
                          activebackground="#B0B0B0", activeforeground="white")
stop_timer_button.pack(side=LEFT, padx=5)

window.mainloop()