import os
from tkinter import Tk, Canvas, Entry, Label, Button

from PIL import Image, ImageTk

start_y = 0
rect_start_y1 = 0
rect_start_y2 = 0

current_image_index = 0
image_dir = "./pics"
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(("jpg"))]


# 获取鼠标位置，防止rect中心线向鼠标吸附
def on_press(event):
    global start_y, rect_start_y1, rect_start_y2

    start_y = event.y
    rect_start_y1 = canvas.coords(rect)[1]
    rect_start_y2 = canvas.coords(rect)[3]


def on_drag(event):
    global start_y

    # 用于自定义选取框高度
    try:
        box_height = int(height_entry.get())
    except ValueError:
        box_height = 500

    dy = event.y - start_y

    new_y1 = rect_start_y1 + dy
    new_y2 = rect_start_y2 + dy

    # 防止选取框被拖到图片外
    if new_y1 >= 0 and new_y2 <= image.height:
        canvas.coords(rect, 0, new_y1, image.width, new_y2)


# 更新cover_crt_label标签内容，显示中心线y坐标
def on_release(event):
    global cover_crt_label

    x1, y1, x2, y2 = canvas.coords(rect)
    y_center = (y1 + y2) / 2
    cover_crt_label.config(text=f"cover_crt={y_center}")


def load_next_image():
    global current_image_index, photo, image, rect, image_canvas

    x1, y1, x2, y2 = canvas.coords(rect)
    y_center = (y1 + y2) / 2
    rename(y_center, image_files[current_image_index])

    current_image_index += 1
    if current_image_index >= len(image_files):
        current_image_index = 0

    try:
        image_path = os.path.join(image_dir, image_files[current_image_index])
        image = Image.open(image_path)
    except FileNotFoundError:
        canvas.delete("all")
        cover_crt_label.config(text="图片已全部处理完毕")
        return

    photo = ImageTk.PhotoImage(image)

    canvas.itemconfig(image_canvas, image=photo)
    canvas.coords(rect, 0, 50, image.width, 500)
    canvas.config(width=image.width, height=image.height)

    cover_crt_label.config(text=f"cover_crt={y_center}")


def rename(y_center, current_image):
    current_path = os.path.join(image_dir, current_image)
    filename, file_extension = os.path.splitext(current_image)
    new_name = f"{filename}_cover_crt-{int(y_center)}{file_extension}"
    new_path = os.path.join(image_dir, new_name)
    os.rename(current_path, new_path)


root = Tk()
root.title("cover_crt图片编辑")
height_label = Label(root, text="选取框高度:")
height_label.pack()
height_entry = Entry(root)
height_entry.pack()
height_entry.insert(0, "500")
cover_crt_label = Label(root, text="cover_crt=")
cover_crt_label.pack()
next_button = Button(root, text="重命名并下一张", command=load_next_image)
next_button.pack()
canvas = Canvas(root)
canvas.pack()

image_path = os.path.join(image_dir, image_files[current_image_index])
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)
image_canvas = canvas.create_image(0, 0, image=photo, anchor="nw")
canvas.config(width=image.width, height=image.height)
rect = canvas.create_rectangle(0, 50, image.width, 500, outline="red", width=5)
x1, y1, x2, y2 = canvas.coords(rect)
y_center = (y1 + y2) / 2
cover_crt_label.config(text=f"cover_crt={y_center}")


canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<ButtonRelease-1>", on_release)

root.mainloop()
