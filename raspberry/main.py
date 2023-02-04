import os
import threading
import tkinter as tk
from functools import partial
from tkinter import W, LEFT

from captureFrame import capture_video
# from playVideo import vlc_player
from socketRaspberry import receiveMessageSkip, sendExcludedEmotion

root = tk.Tk()
root.title("BeCarFortable")
root.geometry("750x250+400+300")

emotion_list = ['Sad', 'Angry', 'Disgust', 'Happy', 'Fear', 'Surprise']
text = ''

def choose(choosen_emotion):
    print(
        f'Selected emotion: {choosen_emotion}')


def get_excluded_emotion(option):
    global text
    if option.get() in emotion_list:
        text = option.get()
        print("Excluded emotion: " + option.get())
        root.destroy()

def start_gui():
    root.configure(background='#189AB4')

    header = tk.Frame(root)
    header.pack(pady=8)
    Font_tuple = ("Helvetica", 20, "bold")
    tk.Label(header, text='BeCarfortable!', font=Font_tuple, background='#189AB4').pack()

    frame = tk.Frame(root, background='#75E6DA', highlightbackground="white", highlightthickness=2, bd=0, borderwidth=5)
    frame.pack(ipadx=20, ipady=15)

    option = tk.StringVar()
    option.set(" ")
    for index, emotion in enumerate(emotion_list):
        b = tk.Radiobutton(frame, text=emotion, value=emotion, var=option,
                           command=partial(choose, emotion),
                           font="Helvetica 11", background='#75E6DA')
        b.pack(side=LEFT, anchor=W)

    Font_tuple = ("Helvetica", 18, "bold")

    start_frame = tk.Frame(root)
    start_frame.pack(pady=8)
    tk.Button(start_frame, text='START', font=Font_tuple, pady=4, padx=20, border=3, fg="blue", bg="#8CDFD6",
              command=partial(get_excluded_emotion, option)).pack()
    label1 = tk.Label(root, text="Select an emotion you dont want to feel!", font='Helvetica 12 bold', pady=20,
                      background='#189AB4')
    label1.pack()
    root.mainloop()


if __name__ == '__main__':

    start_gui()

    sendExcludedEmotion(text)
    print("Starting the video...")

    isExist = os.path.exists("frames")
    if not isExist:
        os.makedirs("frames")

    t1 = threading.Thread(target=capture_video)
    t2 = threading.Thread(target=vlc_player, args=(text,))
    t3 = threading.Thread(target=receiveMessageSkip)
    t1.start()
    t2.start()
    t3.start()
