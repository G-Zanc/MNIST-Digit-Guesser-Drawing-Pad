from tkinter import *
from tkinter import ttk, colorchooser
from PIL import Image, ImageDraw, ImageOps
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.models import load_model
from matplotlib import pyplot

class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.old_x = None
        self.old_y = None
        self.penwidth = 50
        self.drawWidgets()
        self.c.bind('<B1-Motion>',self.paint)#drwaing the line 
        self.c.bind('<ButtonRelease-1>',self.reset)

    def paint(self,e):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,fill=self.color_fg,capstyle=ROUND,smooth=True)
            self.draw.line([self.old_x,self.old_y,e.x,e.y], self.color_fg, int(float(self.penwidth)))
        self.old_x = e.x
        self.old_y = e.y

    def reset(self,e):    #reseting or cleaning the canvas 
        self.old_x = None
        self.old_y = None      

    def changeW(self,e): #change Width of pen through slider
        self.penwidth = e
           
    def clear(self):
        self.c.delete(ALL)
        self.image = Image.new("RGB", (int(float(self.c.cget('width'))), int(float(self.c.cget('height')))), self.color_bg)
        self.draw = ImageDraw.Draw(self.image)
        
    def saveImage(self):
        newImg = self.image.resize((28,28), Image.ANTIALIAS)
        newImg = ImageOps.invert(newImg)
        newImg.save("Drawing.png");
        newImg = load_img("Drawing.png", color_mode = 'grayscale',target_size=(28, 28))
        newImg = img_to_array(newImg)
        newImg = newImg.reshape(1, 28, 28, 1)
        newImg = newImg.astype('float32')
        newImg = newImg / 255.0
        model = load_model("final_model.h5")
        digit = model.predict_classes(newImg)
        self.label['text'] = "Guess: " + str(digit[0])
        #newImg = newImg.reshape(1,28,28)
        #pyplot.imshow(newImg[0], "gray")
        #pyplot.show()
        
    def change_fg(self):  #changing the pen color
        self.color_fg=colorchooser.askcolor(color=self.color_fg)[1]

    def change_bg(self):  #changing the background color canvas
        self.color_bg=colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg'] = self.color_bg
    
    def drawWidgets(self):
        self.controls = Frame(self.master,padx = 5,pady = 5)
    
        self.controls.pack(side=LEFT)
        
        self.c = Canvas(self.master,width=500,height=400,bg=self.color_bg,)
        self.label = Label(self.controls, text="Guess: ")
        self.label.grid(row=1, column=1, ipadx=30)
        self.button = ttk.Button(self.controls, text="Guess Number", command = self.saveImage)
        self.button.grid(row=0,column=1,ipadx=30)
        self.c.pack(fill=BOTH,expand=True)
        menu = Menu(self.master)
        self.master.config(menu=menu)
        filemenu = Menu(menu)
        colormenu = Menu(menu)
        menu.add_cascade(label='Colors',menu=colormenu)
        colormenu.add_command(label='Brush Color',command=self.change_fg)
        colormenu.add_command(label='Background Color',command=self.change_bg)
        optionmenu = Menu(menu)
        menu.add_cascade(label='Options',menu=optionmenu)
        optionmenu.add_command(label='Clear Canvas',command=self.clear)
        optionmenu.add_command(label='Save Image',command=self.saveImage)
        optionmenu.add_command(label='Exit',command=self.master.destroy)
        self.image = Image.new("RGB", (int(float(self.c.cget('width'))), int(float(self.c.cget('height')))), self.color_bg)
        self.draw = ImageDraw.Draw(self.image)

if __name__ == '__main__':
    root = Tk()
    main(root)
    root.title('Application')
    root.mainloop()
