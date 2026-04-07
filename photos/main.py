import os
from tkinter import *
import numpy as np
import cv2
from datetime import datetime
from PIL import Image, ImageTk


BACKGROUND_COLOR = "#F5F5F7"      
CARD_COLOR = "#FFFFFF"             
PRIMARY_COLOR = "#007AFF"           
TEXT_PRIMARY = "#000000"            
TEXT_SECONDARY = "#86868B"         
BUTTON_COLOR = "#007AFF"            
BUTTON_HOVER = "#0051D5"            
SUCCESS_COLOR = "#34C759"            
ERROR_COLOR = "#FF3B30"              

window = Tk()
window.configure(bg=BACKGROUND_COLOR)
window.title("Camera")
window.geometry('700x750')

# Title
title_label = Label(window, text="Camera", font=("Arial", 28, "bold"), 
                   fg=TEXT_PRIMARY, bg=BACKGROUND_COLOR)
title_label.pack(pady=20)

camera_card = Frame(window, bg=CARD_COLOR, highlightthickness=1, highlightbackground="#E5E5E7")
camera_card.pack(padx=20, pady=10, fill="both", expand=True)

canvas = Canvas(camera_card, width=640, height=480, bg="#000000", highlightthickness=0)
canvas.pack(padx=10, pady=10)

status_label = Label(window, text="Camera is off", font=("Arial", 12), 
                    fg=TEXT_SECONDARY, bg=BACKGROUND_COLOR)
status_label.pack(pady=5)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


now = datetime.now()
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(file_path, exist_ok=True)

#  to track state
camera_active = False
current_frame = None

def display_video():
    global camera_active, current_frame
    
    if camera_active:
        ret, frame = cap.read()
        if ret:
            current_frame = frame.copy()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image then to ImageTk
            img = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=img)
            
            canvas.image = photo 
            canvas.create_image(0, 0, image=photo, anchor=NW)
        
        window.after(33, display_video)

def turn_on_camera():
    global camera_active
    camera_active = True
    status_label.config(text="Camera is on", fg=SUCCESS_COLOR)
    show_image_button.config(state="disabled", bg="#CCCCCC")
    remove_image_button.config(state="normal", bg=ERROR_COLOR)
    capture_image_button.config(state="normal", bg=BUTTON_COLOR)
    display_video()

def turn_off_camera():
    global camera_active
    camera_active = False
    canvas.delete("all")
    canvas.create_text(320, 240, text="Camera is off", font=("Arial", 14), 
                      fill=TEXT_SECONDARY)
    status_label.config(text="Camera is off", fg=TEXT_SECONDARY)
    show_image_button.config(state="normal", bg=BUTTON_COLOR)
    remove_image_button.config(state="disabled", bg="#CCCCCC")
    capture_image_button.config(state="disabled", bg="#CCCCCC")

def capture_image():
    global current_frame
    
    if current_frame is not None:
        now = datetime.now()
        file_name = now.strftime("%Y-%m-%d-%H-%M-%S")
        file_full_path = os.path.join(file_path, f"{file_name}.jpg")
        
        cv2.imwrite(file_full_path, current_frame)
        
        # Show success message
        status_label.config(text=f"✓ Image saved: {file_name}.jpg", fg=SUCCESS_COLOR)
        print(f"Image saved to: {file_full_path}")
    else:
        status_label.config(text="No frame to capture", fg=ERROR_COLOR)

buttons_frame = Frame(window, bg=BACKGROUND_COLOR)
buttons_frame.pack(side=BOTTOM, pady=20)

show_image_button = Button(buttons_frame, text="Turn on Camera", font=("Arial", 13, "bold"), 
                          bg=BUTTON_COLOR, fg="white", command=turn_on_camera, 
                          padx=15, pady=10, relief=FLAT, cursor="hand2",
                          activebackground=BUTTON_HOVER, activeforeground="white")
show_image_button.pack(side=LEFT, padx=5)

capture_image_button = Button(buttons_frame, text="Capture Image", font=("Arial", 13, "bold"), 
                             bg=SUCCESS_COLOR, fg="white", command=capture_image, 
                             padx=15, pady=10, relief=FLAT, cursor="hand2", 
                             state="disabled",
                             activebackground="#30B050", activeforeground="white")
capture_image_button.pack(side=LEFT, padx=5)

remove_image_button = Button(buttons_frame, text="Turn off Camera", font=("Arial", 13, "bold"), 
                            bg="#CCCCCC", fg="white", command=turn_off_camera, 
                            padx=15, pady=10, relief=FLAT, cursor="hand2", 
                            state="disabled",
                            activebackground="#B0B0B0", activeforeground="white")
remove_image_button.pack(side=LEFT, padx=5)

canvas.create_text(320, 240, text="Camera is off", font=("Arial", 14), 
                  fill=TEXT_SECONDARY)

def on_closing():
    global camera_active
    camera_active = False
    cap.release()
    cv2.destroyAllWindows()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()