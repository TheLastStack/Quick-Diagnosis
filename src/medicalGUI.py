import medical
import tkinter as tk
from math import ceil
from tkinter import *


def print_desc(result, heading, data):
    window = Tk()

    def close():
        window.destroy()

    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry("%dx%d" % (width, height))

    frame = Frame(window, relief=tk.FLAT, borderwidth=2)
    frame.pack(side=tk.TOP)

    lbl_name = Label(frame, text=heading, font=('calibre', 25, 'bold'))
    lbl_name.pack(side=tk.TOP)

    lbl_name = Label(frame, text=result, font=('calibre', 16, 'bold'))
    lbl_name.pack(side=tk.TOP)

    lbl_name = Label(frame, text=data, font=('calibre', 12))
    lbl_name.pack(side=tk.TOP)

    sub_btn = tk.Button(frame, text='Next', command=close, width=45, height=3)
    sub_btn.pack(anchor='se')

    window.mainloop()

class callback_wrapper:
    def __init__(self):
        self.patient = ""
        self.return_dict = {}
    def submit(self, window, symptoms_sev, txt_name):
        patient = str(txt_name.get())
        return_dict = {}
        for key, value in symptoms_sev.items():
            if value.get() != 0:
                return_dict[key] = value.get()
        #print(return_dict)
        self.return_dict = return_dict.copy()
        #print(patient)
        window.destroy()

def display_window(symptoms, final_submit):
    symptoms.sort()
    window = tk.Tk()
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry("%dx%d" % (width, height))
    frame = Frame(window, relief=tk.FLAT, borderwidth=2)
    frame.pack(side=tk.TOP)
    lbl_name = Label(frame, text='Enter your name', font=('calibre', 25, 'bold'))
    lbl_name.pack(side=tk.LEFT)
    name = StringVar()
    txt_name = Entry(frame, textvariable=name, width=30, font=('calibre', 18))
    txt_name.pack(side=LEFT)
    frame = Frame(window, relief=tk.FLAT, borderwidth=2)
    frame.pack(side=tk.TOP)
    lbl_info = Label(frame,
                     text='Click the button (0-5) corresponding to any symptom you are facing with, ranging from '
                          '0(no symptom) to 5(severe)', font=('calibre', 15))
    lbl_info.pack(side=TOP)
    rows = 22
    i = 0
    symptoms_sev = {}
    second_frame = {}
    third_frames = {}
    last_frame = Frame(window, relief=tk.FLAT)
    last_frame.pack(side=tk.TOP)
    for j in range(ceil(len(symptoms) / rows)):
        second_frame[j] = Frame(last_frame, relief=tk.FLAT, borderwidth=0)
        second_frame[j].pack(side=tk.LEFT)
        for t in range(rows):
            i = rows * j + t
            if i >= len(symptoms):
                continue
            symptoms_sev[symptoms[i]] = tk.IntVar()
            symptoms_sev[symptoms[i]].set(0)
            cval = j * (rows + 1) + t
            third_frames[cval] = tk.Frame(master=second_frame[j], relief=tk.FLAT, borderwidth=2)
            third_frames[cval].pack(side=tk.TOP)
            tk.Label(master=third_frames[cval], text=symptoms[i].replace('_', ' ').capitalize(), width=15).pack(side=tk.LEFT)
            tk.Radiobutton(master=third_frames[cval], text='0', variable=symptoms_sev[symptoms[i]], value='0').pack(side=tk.LEFT)
            tk.Radiobutton(master=third_frames[cval], text='1', variable=symptoms_sev[symptoms[i]], value='1').pack(side=tk.LEFT)
            tk.Radiobutton(master=third_frames[cval], text='2', variable=symptoms_sev[symptoms[i]], value='2').pack(side=tk.LEFT)
            tk.Radiobutton(master=third_frames[cval], text='3', variable=symptoms_sev[symptoms[i]], value='3').pack(side=tk.LEFT)
            tk.Radiobutton(master=third_frames[cval], text='4', variable=symptoms_sev[symptoms[i]], value='4').pack(side=tk.LEFT)
            tk.Radiobutton(master=third_frames[cval], text='5', variable=symptoms_sev[symptoms[i]], value='5').pack(side=tk.LEFT)
    sub_btn = tk.Button(second_frame[ceil(len(symptoms) / rows) - 1], text='Submit', command=lambda:final_submit.submit(window, symptoms_sev, txt_name), width=45, height=3)
    sub_btn.pack(side=tk.BOTTOM)
    window.mainloop()


if __name__ == "__main__":
    dis_symp_dict, symp_dis_dict, dis_list, symp_list = medical.DataBase_Read()
    '''
    Print debugging!
    print(dis_symp_dict)
    print(symp_dis_dict)
    print(dis_list)
    print(symp_list)
    '''
    final_submit = callback_wrapper()
    display_window(symp_list, final_submit)
    for result, heading, data in medical.check_symptoms(final_submit.patient, final_submit.return_dict, dis_symp_dict, symp_dis_dict, dis_list, symp_list):
        print_desc(result, heading, data)
