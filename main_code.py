from tkinter import Tk, Canvas, Label, Button, mainloop, BOTH, YES, BOTTOM
from PIL import Image, ImageDraw
from tensorflow import keras, autograph
import numpy as np
from skimage import transform

canvas_width = 500
canvas_height = 500

cv_img = Image.new("RGB", (canvas_width, canvas_height), (0 ,0 ,0))
draw = ImageDraw.Draw(cv_img)
model = keras.models.load_model("model.h5")


def paint(event):
	x1, y1 = (event.x - 15), (event.y - 15)
	x2, y2 = (event.x + 15), (event.y + 15)
	cv.create_oval(x1, y1, x2, y2, fill="white", width=0)

	draw.ellipse([x1, y1, x2, y2], (255, 255, 255))

@autograph.experimental.do_not_convert # IDK what this means, tensorflow warned me about something and asked me to do this, so I DID.
def predict():
	#image pre-processing
	np_img = np.asarray(cv_img)
	gray = np.dot(np_img[...,:], [0.299, 0.587, 0.114])  
	gray28x28 = transform.resize(gray, (28, 28))  
	vectorized_filter = np.vectorize(lambda v: 255 if v > 128 else v)  
	filtered = vectorized_filter(gray28x28)
	batch = np.array([filtered])
	prediction_list = model.predict(batch)
	prediction = np.where(prediction_list == 1)[1][0]
	prediction_message.configure(text=f"Prediction = {prediction}")

def clear():
	global cv_img, draw

	cv.delete("all")
	cv_img = Image.new("RGB", (canvas_width, canvas_height), (0 ,0, 0))
	draw = ImageDraw.Draw(cv_img)
	prediction_message.configure(text="Prediction = None")


master = Tk()
master.title("0-9 Digit Detector")
cv = Canvas(master, width=canvas_width, height=canvas_height, bg="black")
cv.pack(expand=YES, fill=BOTH)
cv.bind("<B1-Motion>", paint)

message = Label(master, text="Press and Drag the mouse to draw")
message.pack(side=BOTTOM)

prediction_message = Label(master, text="Prediction = None", font=("Arial", 25))
prediction_message.pack(side=BOTTOM)

predict_button = Button(master, text= "Predict", command = predict)
predict_button.pack( side = BOTTOM )

clear_button = Button(master, text= "Clear", command = clear)
clear_button.pack( side = BOTTOM )
    
mainloop()