from tkinter import *
from PIL import Image, ImageDraw
from tensorflow import keras

canvas_width = 500
canvas_height = 500

cv_img = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))
draw = ImageDraw.Draw(cv_img)


def paint(event):
	x1, y1 = (event.x - 15), (event.y - 15)
	x2, y2 = (event.x + 15), (event.y + 15)
	cv.create_oval(x1, y1, x2, y2, fill="white", width=0)

	draw.ellipse([x1, y1, x2, y2], (255, 255, 255))


def predict():
	#image pre-processing

	prediction_message.configure(text="Prediction = 5")
	cv_img.save("saved_img.jpg")


def clear():
	global cv_img, draw

	cv.delete("all")
	cv_img = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))
	draw = ImageDraw.Draw(cv_img)


master = Tk()
master.title("0-9 Digit Detector")
cv = Canvas(master, width=canvas_width, height=canvas_height, bg="black")
cv.pack(expand=YES, fill=BOTH)
cv.bind("<B1-Motion>", paint)

message = Label(master, text="Press and Drag the mouse to draw")
message.pack(side=BOTTOM)

predict_button = Button(master, text= "Predict", command = predict)
predict_button.pack( side = BOTTOM )

clear_button = Button(master, text= "Clear", command = clear)
clear_button.pack( side = BOTTOM )
    
mainloop()
