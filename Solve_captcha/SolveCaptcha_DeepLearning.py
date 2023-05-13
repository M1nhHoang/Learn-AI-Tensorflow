from tensorflow.keras.models import load_model
import tensorflow as tf
import keras
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, Text, filedialog
from PIL import ImageTk, Image
import os

global char_
char_ =['u', '7', '9', 'a', 'U', 'y', 'R', 'n', 'H', 'b', '6', 's', 'm', 'C', '2', 'h', 'v', 'j', 'c', 'T', 'q', 'B', 'K', 'P', 'd', 'f', 'Q', 'g', 'r', 'X', 'G', '8', 'S', 't', 'V', '3', '4', 'x', 'z', 'F', '5', 'Z', 'p', 'e', 'k']

# load the model from file
model = load_model('model_PredictCaptcha.h5')

# decode
def decode_batch_predictions(pred, char_ = char_):
    max_length = 5
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
        :, :max_length
    ]
    # Iterate over the results and get back the text
    output_text = ''
    #conver to text
    for res in results:
        res = np.array(res)
        for r in res:
            try:
                output_text += char_[int(r)]
            except:
                output_text += '_'
    return output_text

# predict
def predict(url):  
	img = Image.open(url).convert('L')
	img = img.resize((145, 50))
	img = np.array(img)
	img = img.reshape(50, 145, 1)

	new_img = tf.expand_dims(img,0)
	new_img = new_img / 255
	preds = model.predict(new_img)
	pred_texts = decode_batch_predictions(preds)
    
	return pred_texts

root = tk.Tk()

#Set the geometry
root.geometry("300x300")
root.resizable(False, False)

def Select_Url():
	selected_Ulr.configure(state='normal')
	selected_Ulr.delete(1.0, 'end')
	fileName = filedialog.askopenfilename(initialdir = os.path.dirname(__file__), title = 'Select File',
										filetypes = (('all files', '*'), ('img.jpg','*.jpg'),('img.png','*.png')))
	selected_Ulr.insert('end', fileName)
	selected_Ulr.configure(state='disabled')

def comfrim(imagefile):
	lb_predict.config(text=predict(imagefile))
	# img
	image = Image.open(imagefile)
	image = image.resize((145, 50))
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
imagebox.place(x=75, y=120)

root.mainloop()
