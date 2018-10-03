from tkinter import Tk, Label
import PIL.ImageTk
import PIL.Image
from keyboard import is_pressed
from sys import exit

version = 'v0.0.1'

start = False
drag = False
drag_id = ''


def close_window():
    root.withdraw()
    exit()  # Ensures python window exits


def resize():
    window_x = root.winfo_width()
    window_y = root.winfo_height()
    if window_x > window_y:
        root.geometry('{0}x{0}'.format(window_x))
    elif window_y > window_x:
        root.geometry('{0}x{0}'.format(window_y))


def dragging(event):
    global drag_id
    global drag
    if drag_id == '':
        pass
    else:
        root.after_cancel(drag_id)
        drag = True
    drag_id = root.after(100, stop_drag)


def stop_drag():
    global drag_id
    global drag
    drag = False
    drag_id = ''


root = Tk()
root.resizable(width=True, height=True)
root.geometry('640x640')
root.maxsize(width=640, height=640)  # Max size is the original image size
root.minsize(width=124, height=124)
root.title('bongo cat' + version)
root.protocol('WM_DELETE_WINDOW', close_window)

k1 = 's'
k2 = 'a'
start = True

# preload all images
hit_images = {
    1: PIL.Image.open("cat/test.png"),
    2: PIL.Image.open("cat/KeyTapHand2.png")
}

# default hand position when start
default_images = PIL.Image.open("cat/up hand.png")
default_img = PIL.ImageTk.PhotoImage(default_images)
image_label = Label(root, image=default_img)
image_label.image = default_img
image_label.pack()

w_size = root.winfo_width, root.winfo_height
w_size_prev = w_size
k1_p_prev = False
k2_p_prev = False
first_iteration = True
force_update = True
last_hit = 1


def iterate():
    global k1_p_prev, k2_p_prev, last_hit, drag, w_size_prev, w_size, first_iteration, force_update
    if drag:
        root.after(5, iterate)
        return

    k1_p = is_pressed(k1)
    k2_p = is_pressed(k2)

    base_img = default_images

    def forceUpdate():
        base_img = default_images.resize((root.winfo_width(), root.winfo_height()), PIL.Image.ANTIALIAS)
        n_base_img = PIL.ImageTk.PhotoImage(base_img)
        image_label.configure(image=n_base_img)
        image_label.image = n_base_img
        root.update()

    if first_iteration:
        first_iteration = False
        forceUpdate()
        root.after(0, iterate)
        return

    resize()

    if k1_p == k1_p_prev and k2_p == k2_p_prev:
        root.after(5, iterate)
        return

    if k1_p or k2_p:
        force_update = True
        if (k1_p and not k1_p_prev) or (not k2_p and k2_p_prev):
            final_hit = 1
        elif (k2_p and not k2_p_prev) or (not k1_p and k1_p_prev):
            final_hit = 2
        else:
            final_hit = last_hit

        last_hit = final_hit
        final_hit_img = hit_images[final_hit]
        composite_image = PIL.Image.alpha_composite(base_img, final_hit_img)
        composite_image.thumbnail((root.winfo_width(), root.winfo_height()), PIL.Image.ANTIALIAS)
        n_base_img = PIL.ImageTk.PhotoImage(composite_image)
    else:
        base_img = base_img.resize((root.winfo_width(), root.winfo_height()), PIL.Image.ANTIALIAS)
        n_base_img = PIL.ImageTk.PhotoImage(base_img)

    k1_p_prev = k1_p
    k2_p_prev = k2_p

    image_label.configure(image=n_base_img)
    image_label.image = n_base_img
    root.update()
    root.after(5, iterate)


if start:
    root.bind('<Configure>', dragging)
    root.after(0, iterate)
    root.mainloop()
