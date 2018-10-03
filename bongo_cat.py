from tkinter import Tk, Label
from keyboard import is_pressed
from sys import exit
import PIL.Image
import PIL.ImageTk

start = False


def close_window():
    root.withdraw()
    exit()


# def resize():
#     window_x = root.winfo_width()
#     window_y = root.winfo_height()
#     if window_x > window_y:
#         root.geometry('{0}x{0}'.format(window_x))
#     elif window_y > window_x:
#         root.geometry('{0}x{0}'.format(window_y))
k = 'a'
start = True

root = Tk()
# root.resizealbe(width=True,height=True)
# root.geometry('640x640')
root.maxsize(width=1270, height=960)
root.minsize(width=124, height=124)
root.title('Bongo Cat')
root.protocol('WM_DELETE_WINDOW', close_window)

hit_image = PIL.Image.open("cat/down hand.png")
default_image = PIL.Image.open("cat/up hand.png")
default_img = PIL.ImageTk.PhotoImage(default_image)
image_label = Label(root, image=default_img)
image_label.image = default_img
image_label.pack()

first_iteration = True
force_update = True


def iterate():
    global first_iteration, force_update
    k_p = is_pressed(k)

    base_img = default_image

    def forceupdate():
        # base_img = default_img.resize((root.winfo_width(), root.winfo_height()), PIL.Image.ANTIALIAS)
        n_base_img = PIL.ImageTk.PhotoImage(base_img)
        image_label.configure(image=n_base_img)
        root.update()

    if first_iteration:
        first_iteration = False
        forceupdate()
        root.after(0, iterate)
        return

    if k_p:
        force_update = True

        composite_image = PIL.Image.alpha_composite(base_img, hit_image)
        composite_image.thumbnail((root.winfo_width(), root.winfo_height()), PIL.Image.ANTIALIAS)
        n_base_img = PIL.ImageTk.PhotoImage(composite_image)
    else:
        # base_img = base_img.resize((root.winfo_width(), root.winfo_height()), PIL.Image.ANTIALIAS)
        n_base_img = PIL.ImageTk.PhotoImage(base_img)

    image_label.configure(image=n_base_img)
    image_label.image = n_base_img
    root.update()
    root.after(5, iterate)


if start:
    root.after(0, iterate)
    root.mainloop()


