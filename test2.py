import tkinter

window=tkinter.Tk()
window.title("YUN DAE HEE")
window.geometry("640x480+100+100")
window.resizable(False, False)

def flash():
    checkbutton1.flash()
    print(CheckVariety_2.get())
    if CheckVariety_2.get():
        print('relly')

CheckVariety_1=tkinter.BooleanVar()
CheckVariety_2=tkinter.BooleanVar()

checkbutton1=tkinter.Checkbutton(window, text="O", variable=CheckVariety_1, activebackground="blue")
checkbutton2=tkinter.Checkbutton(window, text="△", variable=CheckVariety_2)
checkbutton3=tkinter.Checkbutton(window, text="X", variable=CheckVariety_2, command=flash)

checkbutton1.pack()
checkbutton2.pack()
checkbutton3.pack()

window.mainloop()