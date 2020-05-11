# Зачем использовать "Paint", если Питон позволяет быстро написать свой собственный "Paint" с блэ..
# С теми функциями, что нам нужны))

from tkinter import *
import os
from tensorflow.keras.preprocessing import image
import numpy as np
#from PIL import Image, ImageTk, ImageGrab  # For Windows & OSx
import pyscreenshot as ImageGrab # For Linux
from tkinter import messagebox as mb
from PIL import ImageDraw
from PIL import Image as IMG

from os.path import dirname, join
current_dir = dirname(__file__)
file_path = join(current_dir, "mnist_number.h5")
from tensorflow.keras.models import load_model
model = load_model(file_path)
 
class Paint(Frame):
    
    '''
    Это маленькая программка, всего с одной возможностью и двумя кнопочками.
    Но интересная! =)))
    Вы можете нарисовать любую римскую цифру и моя нейросеть попробует ее распознать.
    Рекомендуем писать единичку палочкой и все цифры без наклона.
    Этим правилам следует западная культура написания цифр, 
    а именно на ней нейроночка и училась.
    Также убедитесь, что ваши цифры нарисованы без разрывов.
    
    Если рисовать цифры без особых изысков и в западной манере, 
    то доля успешного распознавания превышает 95%.
    Если что-то работает неправильно, или у вас есть идеи или предложения ко мне,
    прошу писать на почту DoroninDobro@gmail.com
    
    Интструкция:
    Кнопка "Clear all" очищает экран, если рисунок получился не таким, как вы хотели.
    Кнопка "What is the Number?" отправляет картинку нейронной сети.
    '''
    def __init__(self, parent):
         Frame.__init__(self, parent)
         self.parent = parent
         self.setUI()
         self.brush_size = 14
         self.brush_color = "white"
            
    def w_n(self):
        self._snapsaveCanvas()
        number = IMG.open('out_snapsave.jpg')
        number = number.resize([28,28])
        number = number.convert('L')
        number = image.img_to_array(number)
        number = number.reshape(1, 784)
        prediction = model.predict(number)
        predict = np.argmax(prediction)
        mb.showinfo("Приходи еще! =)", f"Я думаю это число: {predict}")
            
    def _snapsaveCanvas(self):        
        self.grabcanvas = ImageGrab.grab(bbox=(406,211,793,590)).save("out_snapsave.jpg")        
        
    def setUI(self):            
         
        self.parent.title("Нарисуй цифру")  # Устанавливаем название окна
        self.pack(fill=BOTH, expand=1)  # Размещаем активные элементы на родительском окне
 
        self.canv = Canvas(self, bg="black", height=387, width=387)  
        # Создаем поле для рисования, устанавливаем black фон
        self.canv.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.canv.bind("<B1-Motion>", self.draw)
        
        clear_btn = Button(self, text="Clear all", width=10, 
                           command=lambda: self.canv.delete("all"))
        clear_btn.grid(row=0, column=0, sticky=W)
        
        clear_btn = Button(self, text="What is the Number?", width=35, 
                           command=self.w_n)
        clear_btn.grid(row=0, column=1, sticky=W)
        
    def draw(self, event):
        self.canv.create_oval(event.x - self.brush_size,
                          event.y - self.brush_size,
                          event.x + self.brush_size,
                          event.y + self.brush_size,
                          fill=self.brush_color, outline=self.brush_color)
        
 
 
def main():
    root = Tk()
    root.geometry("399x423+400+150")
    app = Paint(root)
    root.mainloop()
 
if __name__ == "__main__":
    main()