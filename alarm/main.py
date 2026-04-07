from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk
import time
import pygame
from utils.convert import convert_to_24hr

pygame.mixer.init()
alarm_sound = pygame.mixer.Sound("../alarm/audio/alarm.mp3")

window = Tk()
notebook = ttk.Notebook(window)
window.geometry("500x500")
window.title("Alarm clock")
tab1 = Frame(notebook)
tab2 = Frame(notebook)
notebook.add(tab1, text="Alarm")
notebook.add(tab2, text="Timer")
notebook.pack(expand=True, fill="both")
frame = Frame(tab1)
frame.pack(side=BOTTOM, pady=20)
menubar = Menu(window)
window.config(menu=menubar)
icon = PhotoImage(file="../alarm/asset/alarm.png")
window.iconphoto(True, icon)

clockMenu = Menu(menubar, tearoff=0)
clockMenu.add_command(label="Exit", command=window.quit)

label = Label(tab1, text=time.strftime("%I:%M:%S %p"), font=("Arial", 18))
label.pack(pady=20)

label_timer = Label(tab2, text="Timer", font=("Arial", 18))
label_timer.pack(pady=20)

label2 = Label(tab1, text="Set your alarm time", font=("Arial", 14))
label2.pack(pady=5)

label_timer2 = Label(tab2, text="Set your timer duration", font=("Arial", 14))
label_timer2.pack(pady=5)

now = datetime.now()

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
hours = [f"{i:02d}" for i in range(1, 13)]  # Fixed: 1-12 for 12-hour format
minute = [f"{i:02d}" for i in range(60)]
seconds = [f"{i:02d}" for i in range(60)]
ampm_values = ["AM", "PM"]

hours_timer = [f"{i:02d}" for i in range(24)]
minute_timer = [f"{i:02d}" for i in range(60)]
seconds_timer = [f"{i:02d}" for i in range(60)]

day = datetime.now().weekday()
year = datetime.now().year
hours_time = datetime.now().hour
minute_time = datetime.now().minute
seconds_time = datetime.now().second

month = datetime.now().month
current = time.localtime().tm_hour, time.localtime().tm_min
ampm = datetime.now().strftime("%p")

day_label = Label(tab1, text=f"Current day: {days_of_week[day]}", font=("Arial", 13))
day_label.pack(pady=10)

cb_day = ttk.Combobox(tab1, values=days_of_week, state="readonly")
cb_day.current(day)
cb_day.pack(padx=20, pady=10)

cb = ttk.Combobox(tab1, values=hours, state="readonly")

current_12hr = hours_time % 12 if hours_time % 12 != 0 else 12
cb.current(current_12hr - 1)  # -1 because list is 1-12, not 0-11
cb.pack(padx=20, pady=10)

cb2 = ttk.Combobox(tab1, values=minute, state="readonly")
cb2.current(minute_time)
cb2.pack(padx=20, pady=10)

cb3 = ttk.Combobox(tab1, values=seconds, state="readonly")
cb3.current(seconds_time)
cb3.pack(padx=20, pady=10)

cb4 = ttk.Combobox(tab1, values=ampm_values, state="readonly")
cb4.current(0 if ampm == "AM" else 1)
cb4.pack(padx=20, pady=10)

cb_timer_hours = ttk.Combobox(tab2, values=hours_timer, state="readonly")
cb_timer_hours.current(0)
cb_timer_hours.pack(padx=20, pady=10)

cb_timer_minutes = ttk.Combobox(tab2, values=minute_timer, state="readonly")
cb_timer_minutes.current(0)
cb_timer_minutes.pack(padx=20, pady=10)

cb_timer_seconds = ttk.Combobox(tab2, values=seconds_timer, state="readonly")
cb_timer_seconds.current(0)
cb_timer_seconds.pack(padx=20, pady=10)

alarm_triggered = False


def stop_alarm():
    global alarm_triggered
    alarm_sound.stop()
    alarm_triggered = False
    set_alarm_button.config(state="normal")
    stop_alarm_button.config(state="disabled")
    label3.config(text="00:00:00")
    print("Alarm stopped")

def update_clock():
    global alarm_triggered
    window.after(1000, update_clock)
    current_time = time.strftime("%I:%M:%S %p")
    day = cb_day.get()
    hour = cb.get()
    minute = cb2.get()
    seconds = cb3.get()
    ampm_value = cb4.get()

    hour_24 = convert_to_24hr(hour, ampm_value)
    
    full_time = f"{hour}:{minute}:{seconds} {ampm_value}"
    label.config(text=current_time)

    target_datetime = datetime(year, month, datetime.now().day, hour_24, int(minute), int(seconds))

    # Check if alarm time has passed
    if now > target_datetime:
        label4.config(state="normal")
        set_alarm_button.config(state="disabled")
    else:
        label4.config(state="disabled")
        set_alarm_button.config(state="normal")
        label3.config(text=f"Alarm Time Set for: {day} {full_time} for {year}/{month}/{datetime.now().day}")

    # Check if it's time to trigger the alarm
    current_time_no_ampm = time.strftime("%H:%M:%S")  # 24-hour format
    target_time = f"{hour_24:02d}:{minute}:{seconds}"
    
    if current_time_no_ampm == target_time and datetime.now().weekday() == days_of_week.index(day) and not alarm_triggered:
        alarm_sound.play()
        label3.config(text="Alarm is ringing!")
        set_alarm_button.config(state="disabled")
        stop_alarm_button.config(state="normal")
        alarm_triggered = True
        print("Alarm is ringing")

def real_time():
    label.config(text=time.strftime("%I:%M:%S %p"))
    window.after(1000, real_time)

window.after(1000, real_time)

label3 = Label(tab1, text="00:00:00", font=("Arial", 14))
label3.pack(pady=10)

label_timer3 = Label(tab2, text="00:00:00", font=("Arial", 14))
label_timer3.pack(pady=10)

label4 = Label(tab1, text="The alarm needs to be in the future.", font=("Arial", 10), state="disabled")
label4.pack(pady=5)

def set_timer():
    hours = int(cb_timer_hours.get())
    minutes = int(cb_timer_minutes.get()) 
    seconds = int(cb_timer_seconds.get())
    
    if hours == 0 and minutes == 0 and seconds == 0:
        label_timer3.config(text="Please set a duration for the timer.")
        return
    else:
        label_timer3.config(text=f"Timer set for {hours:02d}:{minutes:02d}:{seconds:02d}")
        countdown_timer(hours, minutes, seconds)

    print("Timer not yet implemented")

def countdown_timer(hours, minutes, seconds):
    total_seconds = hours * 3600 + minutes * 60 + seconds

    print(f"Total seconds for timer: {total_seconds}")
    while total_seconds > 0:
        mins, secs = divmod(total_seconds, 60)
        hrs, mins = divmod(mins, 60)
        timer_format = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        label_timer3.config(text=timer_format)
        window.update()
        time.sleep(1)
        total_seconds -= 1
    label_timer3.config(text="Timer finished!")
    alarm_sound.play()
    print("Timer finished")

set_timer_button = Button(tab2, text="Set Timer", font=("Arial", 14), bg="white", command=set_timer)
set_timer_button.pack(pady=10)

set_alarm_button = Button(frame, text="Set Alarm", font=("Arial", 14), bg="white", command=update_clock)
set_alarm_button.pack(side=RIGHT)

stop_alarm_button = Button(frame, text="Stop Alarm", font=("Arial", 14), bg="white", command=stop_alarm, state="disabled")
stop_alarm_button.pack(side=RIGHT)

window.mainloop()