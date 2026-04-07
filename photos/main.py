import os
from tkinter import *
import numpy as np
import cv2
from datetime import datetime
from PIL import Image, ImageTk

window = Tk()
window.title("Photo")
window.geometry('500x500')
frame = Frame(window)
frame.pack(side=BOTTOM, pady=20)

cap = cv2.VideoCapture(0)

now = datetime.now()
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
now = datetime.now()
file_name = now.strftime("%Y-%m-%d-%H-%M-%S")


def display_video():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 3. Convert to PIL Image then to ImageTk
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)
        
        canvas.image = photo 
        canvas.create_image(0, 0, image=photo, anchor=NW)
        show_image_button.config(state="disabled")
        remove_image_button.config(state="normal")

    if cv2.waitKey(1) == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
    
    window.after(33, display_video)

def disable_video():
    cap.release() 
    

def capture_image():
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(f'{file_path}/{file_name}.jpg', frame)
        label3 = Label(window, text="Image Taken!", font=("Arial", 14))
        label3.pack(padx=10)




canvas = Canvas(window, width=640, height=480)
canvas.pack(padx=10)


show_image_button = Button(frame, text="Turn on Camera", font=("Arial", 14), bg="white", command=display_video)
show_image_button.pack(pady=10)

remove_image_button = Button(frame, text="Turn off Camera", font=("Arial", 14), bg="white", command=disable_video, state="disabled")
remove_image_button.pack(pady=10)

capture_image_button = Button(frame, text="Capture Image", font=("Arial", 14), bg="white", command=capture_image)
capture_image_button.pack(pady=10)
    


window.mainloop()
