from tkinter import * 
from PIL import Image
from PIL import ImageTk
import tkinter.filedialog as tkFileDialog
import cv2

#Converte a imagem para o padrao aceito pelo tkinter
#Param: imagem RGB
#Return: imagem para o padrao tkinter
def convertToTk(image):
    convertedImage = Image.fromarray(image)
    convertedImage = ImageTk.PhotoImage(convertedImage)
    return convertedImage 




def select_image():
    global panelA, panelB
    path = tkFileDialog.askopenfilename()

    if(len(path)) > 0:
        
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        ##edged = Image.fromarray(edged)

        ##edged = ImageTk.PhotoImage(edged)

        image = convertToTk(image)
        edged = convertToTk(edged)
        if panelA is None or panelB is None:
            panelA = Label(image = image)
            panelA.image = image
            panelA.pack(side="left", padx=10,pady=10)

            panelB = Label(image = edged)
            panelB.image = edged
            panelB.pack(side="right", padx=10, pady=10)

        else:

            panelA.configure(image=image)
            panelB.configure(image=edged)
            panelA.image = image
            panelB.image = edged

root = Tk()
panelA = None
panelB = None


btn = Button(root, text="Select an iamge", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")


root.mainloop()
