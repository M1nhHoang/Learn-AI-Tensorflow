from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, Text, filedialog
from PIL import ImageTk, Image
import random
import os

# load the model from file
model = load_model('model_DuDoanSo.h5')

# ham` du doan
def predict(img):  
    img = img.convert('L')
    img = np.array(img)
    # img = img[:,:, 0]
    img = img.reshape(28, 28, 1)
    new_img = tf.expand_dims(img,0)
    new_img = new_img / 255
    label = np.argmax(model.predict(new_img), axis=-1)
    
    return label

def noise_removal(url):
    img = Image.open(url)
    img = img.resize((28, 28))
    pixels = img.load()

    new_img = Image.new(img.mode, img.size)
    pixels_new = new_img.load()
    # lấy mã màu kiểm tra
    # góc trái trên
    r_topLeft, b_topLeft, g_topLeft = pixels[1, 1]
    # góc phải trên
    r_topRight, b_topRight, g_topRight = pixels[1, new_img.size[1]-1]
    # góc phải dưỡi
    r_botRight, b_botRight, g_botRight = pixels[new_img.size[0]-1, new_img.size[1]-1]
    # góc trái dưỡi
    r_botLeft, b_botLeft, g_botLeft = pixels[new_img.size[0]-1, 1]
    # ở giưa
    r_middle, b_middle, g_middle = pixels[new_img.size[0]-1, 1]

    difference_color = random.randint(10,40)
    list_check = []
    row_check = []
    if r_middle - r_topLeft < difference_color or b_middle - b_topLeft < difference_color or g_middle - g_topLeft < difference_color:
        row_check.append(1)
        row_check.append(r_topLeft)
        row_check.append(b_topLeft)
        row_check.append(g_topLeft)
    else:
        row_check.append(0)
        row_check.append(r_topLeft)
        row_check.append(b_topLeft)
        row_check.append(g_topLeft)
    list_check.append(row_check)
    row_check = []
    if r_middle - r_topRight < difference_color or b_middle - b_topRight < difference_color or g_middle - g_topRight < difference_color:
        row_check.append(1)
        row_check.append(r_topRight)
        row_check.append(b_topRight)
        row_check.append(g_topRight)
    else:
        row_check.append(0)
        row_check.append(r_topRight)
        row_check.append(b_topRight)
        row_check.append(g_topRight)
    list_check.append(row_check)
    row_check = []  
    if r_middle - r_botRight < difference_color or b_middle - b_botRight < difference_color or g_middle - g_botRight < difference_color:
        row_check.append(1)
        row_check.append(r_botRight)
        row_check.append(b_botRight)
        row_check.append(g_botRight)
    else:
        row_check.append(0)
        row_check.append(r_botRight)
        row_check.append(b_botRight)
        row_check.append(g_botRight)
    list_check.append(row_check)
    row_check = []
    if r_middle - r_botLeft < difference_color or b_middle - b_botLeft < difference_color or g_middle - g_botLeft < difference_color:
        row_check.append(1)
        row_check.append(r_botLeft)
        row_check.append(b_botLeft)
        row_check.append(g_botLeft)
    else:
        row_check.append(0)   
        row_check.append(r_botLeft)
        row_check.append(b_botLeft)
        row_check.append(g_botLeft)
    list_check.append(row_check)

    count = 0
    for check_color in range(len(list_check)):
        if list_check[check_color][0] == 1:
            count += 1
    if count <= 2:
    	main_color = [list_check[check_color][1], list_check[check_color][2], list_check[check_color][3]]
    	for i in range(new_img.size[0]):
    		for j in range(new_img.size[1]):
    			r, b, g = pixels[i,j]
    			if main_color[0] - difference_color < r < main_color[0] + difference_color or main_color[1] - difference_color < g < main_color[1] + difference_color or main_color[2] - difference_color < b < main_color[2] + difference_color:
    				pixels_new[i,j] = (255, 255, 255, 0)
    			else:
    				pixels_new[i,j] = (0, 0, 0, 0)
    else:
        for check_color in range(len(list_check)):
            if list_check[check_color][0] == 1:
                main_color = [list_check[check_color][1], list_check[check_color][2], list_check[check_color][3]]
                break

        for i in range(new_img.size[0]):
            for j in range(new_img.size[1]):
                r, b, g = pixels[i,j]
                if main_color[0] - difference_color < r < main_color[0] + difference_color or main_color[1] - difference_color < g < main_color[1] + difference_color or main_color[2] - difference_color < b < main_color[2] + difference_color:
                    pixels_new[i,j] = (0, 0, 0, 0)
                else:
                    pixels_new[i,j] = (255, 255, 255, 0)

    return new_img

def get_result(url):
	# # loai bo nhieu~
	img = noise_removal(url)
	# du doan
	label = predict(img)
	# xuat
	return label

root = tk.Tk()

#Set the geometry
root.geometry("300x400")
root.resizable(False, False)

def Select_Url():
	selected_Ulr.configure(state='normal')
	selected_Ulr.delete(1.0, 'end')
	fileName = filedialog.askopenfilename(initialdir = os.path.dirname(__file__), title = 'Select File',
										filetypes = (('all files', '*'), ('img.jpg','*.jpg'),('img.png','*.png')))
	selected_Ulr.insert('end', fileName)
	selected_Ulr.configure(state='disabled')

def comfrim(imagefile):
	lb_predict.config(text=get_result(imagefile))
	# img
	image = Image.open(imagefile)
	image = image.resize((200, 200))
	new_image= ImageTk.PhotoImage(image)
	imagebox.config(image=new_image)
	imagebox.image = new_image
	
bt_slectUrl = tk.Button(root, text='Select Image', command=Select_Url)
bt_slectUrl.place(x=10, y=10)

selected_Ulr = Text(root, height = 0, width = 25)
selected_Ulr.insert('end', 'Your url') #file name default
selected_Ulr.configure(state='disabled')
selected_Ulr.place(x=90, y=15)

bt_comfrim = tk.Button(root, text='Dự đoán', command=lambda *args: comfrim(selected_Ulr.get(1.0, 'end').replace('\n','')))
bt_comfrim.pack(side='bottom', padx=10, pady=10)
# text_label
lb_predict = tk.Label(root, text="")
lb_predict.pack(padx=10, pady=60)
lb_predict.config(font=("Tahoma", 15))
# img
imagebox = tk.Label(root)
imagebox.place(x=50, y=120)

root.mainloop()


