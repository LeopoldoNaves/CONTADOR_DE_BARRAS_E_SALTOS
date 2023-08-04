import numpy as np
from tkinter import *
from tkinter import ttk
import tkinter.filedialog as tkFileDialog
import pyglet
from PIL import Image
from PIL import ImageTk
import cv2 as cv



#Usar o pack ao invés do root

#Converte a imagem para o padrao aceito pelo tkinter
#Param: imagem RGB
#Return: imagem para o padrao tkinter
def convertToTk(image):
    convertedImage = Image.fromarray(image)
    convertedImage = ImageTk.PhotoImage(convertedImage)
    return convertedImage 


###################################################################################

###################################################################################
#Classe Principal do nosso App
class App(Tk):
    selectMenu = None
    #canvas = None
    sideMenu = None
    mainFrame = None
    imageLena = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Inicialiazacao da variaveis globais
        global zoomValue; zoomValue = IntVar(value=0)

        global flipCheck; flipCheck = BooleanVar(value=False)

        global blurCheck; blurCheck = BooleanVar(value= False)
        global blurValue; blurValue = IntVar(value = 1)

        global histogramCheck; histogramCheck = BooleanVar(value = False)

        global satCheck; satCheck = BooleanVar(value = False)
        global satValue; satValue = IntVar(value = 0)

        global lumaCheck; lumaCheck = BooleanVar(value = False)
        global lumaValue; lumaValue = IntVar(value = 0)

        global bgSubCheck; bgSubCheck = BooleanVar(value = False)

        global threshCheck; threshCheck = BooleanVar(value = False)
        global lowHueValue; lowHueValue = IntVar(value = 0)
        global lowSatValue; lowSatValue = IntVar(value = 0)
        global lowLumaValue; lowLumaValue = IntVar(value = 0)
        global highHueValue; highHueValue = IntVar(value = 0)
        global highSatValue; highSatValue = IntVar(value = 0)
        global highLumaValue; highLumaValue = IntVar(value = 0)

        global barPoint1; barPoint1 = (0,0)
        global barPoint2; barPoint2 = (0,0)
        global barTrack; barTrack = BooleanVar(value = False)
        global selectedFace; selectedFace = IntVar(value = -1)
        global barHeigth; barHeigth = 0
        global barHeightTracking; barHeightTracking = 0
        global headHeigth; headHeigth = 0
        global faceState; faceState = "down"
        global timer; timer = 60.00
        global run; run = False
        global barCount; barCount = 0

        global isPlaying; isPlaying = False
        global atualFrame; atualFrame = 0
        
        ####################################################
        self.title("Contador de barra fixa, Leop e Chico")
        self.resizable(0, 0)
        #inicia os estilos
        self.defStyle()

        #Inicia o mainFrame(Toda a gui vai ser implementada neste frame)
        self.mainFrame = ttk.Frame(self,style="Frame3.TFrame")
        self.mainFrame.propagate(False)
        self.mainFrame.configure(width=800, height=400)
        #Inicia o menu webcam ou video
        self.selectMenu = SelectMode(self)
        print("Mode selected:"+self.selectMenu.selectedMode.get())
        #cria todos os widgets do mainframe, sideMenu e canvas
        self.createWidgets(mode=self.selectMenu.selectedMode.get(), pathVideo = self.selectMenu.pathVideo.get())
        self.selectMenu.pack_forget()
        self.mainFrame.pack()
        
        
        #self.canvas.setThumbnail(self.selectMenu.selectedMode.get())
    

 
    def defStyle(self):
        styleManager = ttk.Style()
        styleManager.configure('sideMenu.TFrame', background='gray25')
        styleManager.configure('canvas.TFrame', background='gray25')
        styleManager.configure('Frame3.TFrame', background='gray')
        styleManager.configure('gray30.TFrame', background='gray30')
        styleManager.configure('gray30.TCheckbutton', background='gray30')
        styleManager.configure('gray30.TLabel', background='gray30',font=('Helvetica', 10, "bold"))
        styleManager.configure('gray25.TFrame', background='gray25')
        styleManager.configure('gray25.TLabel', background='gray25',font=('Helvetica', 14, "bold"))

        styleManager.configure('clock.TLabel', background='gray15', foreground = 'red',font=('Digital-7 Mono', 25,'bold'))
        styleManager.configure('counter.TLabel', background='gray15', foreground = 'green',font=('Digital-7 Mono', 25,'bold'))
        
        	

    #Cria o tela principal de acrodo com a escolha do usuario.
    def createWidgets(self,mode,pathVideo):
        #Criando o canvas 
        global canvas;canvas = CanvasArea(self.mainFrame,pathVideo, mode)
        canvas.pack(side=RIGHT)
        #Criando o side menu
        self.sideMenu = SideMenu(self.mainFrame)
        self.sideMenu.pack(side=LEFT)
        

####################################################################################
#Classe que define o menu incial de seleção do modo
class SelectMode(ttk.Frame):
    #selectedMode pode ter duas opcões, webcam ou um arquivo de vídeo. 
    selectedMode = None
    width = 400
    height = 100
    btnFile = None
    btnCam = None
    pathVideo = None

    def __init__(self, parent):
        super().__init__(parent)
        #Carrega os icones
        self.iconCamera = ImageTk.PhotoImage(Image.open('./assets/camera.png').resize((70, 70)))
        self.iconVideo = ImageTk.PhotoImage(Image.open('./assets/video.png').resize((70, 70)))
        #Declaração de estilos
        self.defStyle()
        #algumas configurações...
        self.propagate(False)
        self.configure(width = self.width, height = self.height)
        #Botões de escolha
        self.selectedMode  = StringVar()
        self.pathVideo = StringVar()
        self.btnFile = ttk.Button(self, text="Video", style ="leave.TButton", command=lambda: self.selectedMode.set("video"))
        self.btnFile.configure(image = self.iconVideo)
        self.btnFile.image = self.iconVideo
        self.btnCam = ttk.Button(self, text="Câmera", style="leave.TButton",  command=lambda: self.selectedMode.set("webcam"))
        self.btnCam.configure(image = self.iconCamera)
        self.btnCam.image = self.iconCamera
        self.btnFile.pack(side=LEFT,fill=BOTH, expand=True)
        self.btnCam.pack(side=RIGHT,fill=BOTH, expand=True)
        self.pack()
        print("wait choose mode")
        self.wait_variable(self.selectedMode)
        #######
        if(self.selectedMode.get() == "video"):
            self.pathVideo.set(tkFileDialog.askopenfilename())
        else:
            self.pathVideo.set("none")

    def defStyle(self):
        styleManager = ttk.Style()
        styleManager.configure('leave.TButton', background='gray30')
        styleManager.configure('enter.TButton', background='green')

#####################################################################################
#Classe que descreve o menu lateral onde os parametros serão alterados
class SideMenu(ttk.Frame):
    width = 300
    height = 400
    style = "sideMenu.TFrame"
    contadorBarras = None
    def __init__(self,parent):
        super().__init__(parent)
        self.propagate(False)
        self.configure(width = self.width, height = self.height, style = self.style)
        #Carrega os icones
        self.iconPlay = ImageTk.PhotoImage(Image.open('./assets/play.png').resize((30, 30)))
        self.iconStop = ImageTk.PhotoImage(Image.open('./assets/stop.png').resize((30, 30)))
        self.iconContinue = ImageTk.PhotoImage(Image.open('./assets/continue.png').resize((30, 30)))
        self.iconBack = ImageTk.PhotoImage(Image.open('./assets/back.png').resize((30, 30)))
        self.iconNext = ImageTk.PhotoImage(Image.open('./assets/next.png').resize((30, 30)))
        self.contadorBarras = ContadorBarras()
        self.createWidgets()

    def createWidgets(self):
        title = ttk.Label(self,text = "Menu",style ='gray25.TLabel')
        title.pack_propagate(0)
        title.pack( anchor = N)

        #Zoom
        self.zoomFrame = ttk.Frame(self, width = self.width, style='gray30.TFrame')
        self.zoomLabel = ttk.Label(self.zoomFrame,text = "Zoom", style='gray30.TLabel')
        self.zoomSlider = ttk.Scale(self.zoomFrame, variable = zoomValue, from_= -10 , to = 10, orient = "horizontal")
        self.zoomSlider.bind('<Double-Button-1>',lambda a: self.zoomSlider.set(0))
        self.zoomLabel.pack(side = LEFT)
        self.zoomSlider.pack(side = LEFT,fill=X, expand=True)
        self.zoomFrame.pack(side=TOP,anchor = N, fill = X)

        #FLIP
        self.flipFrame = ttk.Frame(self, width = self.width, style='gray30.TFrame')
        self.flipLabel = ttk.Label(self.flipFrame,text = "Flip", style='gray30.TLabel')
        self.flipCheckbox = ttk.Checkbutton(self.flipFrame, variable = flipCheck, onvalue = True, offvalue= False , style = 'gray30.TCheckbutton') 
        self.flipCheckbox.pack(side = LEFT)
        self.flipLabel.pack(side = LEFT)
        self.flipFrame.pack(side=TOP,anchor = N, fill = X)


        #BLUR
        self.blurFrame = ttk.Frame(self, width = self.width, style='gray30.TFrame')
        self.blurLabel = ttk.Label(self.blurFrame,text = "Blur", style='gray30.TLabel')
        self.blurCheckbox = ttk.Checkbutton(self.blurFrame, variable = blurCheck, onvalue = True, offvalue= False , style = 'gray30.TCheckbutton') 
        self.blurSlider = ttk.Scale(self.blurFrame, variable = blurValue, from_= 0 , to =10, orient = "horizontal")
        self.blurCheckbox.pack(side = LEFT)
        self.blurLabel.pack(side = LEFT)
        self.blurSlider.pack(side = RIGHT)
        self.blurFrame.pack(side=TOP,anchor = N, fill = X)

        #Histogram
        self.histogramFrame = ttk.Frame(self, width = self.width,style='gray30.TFrame')
        self.histogramLabel = ttk.Label(self.histogramFrame,text = "Histogram equalization", style = 'gray30.TLabel')
        self.histogramCheckbox = ttk.Checkbutton(self.histogramFrame, variable = histogramCheck, onvalue = True, offvalue= False, style = 'gray30.TCheckbutton' ) 
        self.histogramCheckbox.pack(side = LEFT)
        self.histogramLabel.pack(side = LEFT)
        self.histogramFrame.pack(side=TOP,anchor = N, fill = X)

        #Saturation
        self.satFrame = ttk.Frame(self, width = self.width,style='gray30.TFrame')
        self.satLabel = ttk.Label(self.satFrame,text = "Saturation", style = 'gray30.TLabel')
        self.satCheckbox = ttk.Checkbutton(self.satFrame, variable = satCheck, onvalue = True, offvalue= False, style = 'gray30.TCheckbutton' ) 
        self.satSlider = ttk.Scale(self.satFrame, variable = satValue, from_= -255 , to = 255, orient = "horizontal")
        self.satSlider.bind('<Double-Button-1>',lambda a: self.satSlider.set(0))
        self.satSlider.set(0)
        self.satCheckbox.pack(side = LEFT)
        self.satLabel.pack(side = LEFT)
        self.satSlider.pack(side = RIGHT)
        self.satFrame.pack(side=TOP,anchor = N, fill = X)
        
        #Luma
        self.lumaFrame = ttk.Frame(self, width = self.width,style='gray30.TFrame')
        self.lumaLabel = ttk.Label(self.lumaFrame,text = "Luma", style = 'gray30.TLabel')
        self.lumaCheckbox = ttk.Checkbutton(self.lumaFrame, variable = lumaCheck, onvalue = True, offvalue= False, style = 'gray30.TCheckbutton' ) 
        self.lumaSlider = ttk.Scale(self.lumaFrame, variable = lumaValue, from_= -255 , to = 255, orient = "horizontal")
        self.lumaSlider.bind('<Double-Button-1>',lambda a: self.lumaSlider.set(0))
        self.lumaSlider.set(0)
        self.lumaCheckbox.pack(side = LEFT)
        self.lumaLabel.pack(side = LEFT)
        self.lumaSlider.pack(side = RIGHT)
        
        self.lumaFrame.pack(side=TOP,anchor = N, fill = X)

        #BGsubtractor
        self.bgSubFrame = ttk.Frame(self, width = self.width,style='gray30.TFrame')
        self.bgSubLabel = ttk.Label(self.bgSubFrame,text = "BG Subtractor", style = 'gray30.TLabel')
        self.bgSubCheckbox = ttk.Checkbutton(self.bgSubFrame, variable = bgSubCheck, onvalue = True, offvalue= False, style = 'gray30.TCheckbutton' ) 
        self.bgSubCheckbox.pack(side = LEFT)
        self.bgSubLabel.pack(side = LEFT)
        self.bgSubFrame.pack(side=TOP,anchor = N, fill = X)

        #Threshold
        self.threshFrame = ttk.Frame(self, width = self.width,style='gray30.TFrame')
        self.threshFrame1 = ttk.Frame(self.threshFrame, width = self.width,style='gray30.TFrame')
        self.threshFrame2 = ttk.Frame(self.threshFrame, width = self.width,style='gray30.TFrame')
        self.threshFrame3 = ttk.Frame(self.threshFrame, width = self.width,style='gray30.TFrame')
        self.threshFrame4 = ttk.Frame(self.threshFrame, width = self.width,style='gray30.TFrame')
        self.threshFrame5 = ttk.Frame(self.threshFrame, width = self.width,style='gray30.TFrame')
        self.threshFrame6 = ttk.Frame(self.threshFrame, width = self.width,style='gray30.TFrame')

        self.threshLabel = ttk.Label(self.threshFrame,text = "Threshod", style = 'gray30.TLabel')
        self.threshCheckbox = ttk.Checkbutton(self.threshFrame, variable = threshCheck, onvalue = True, offvalue= False, style = 'gray30.TCheckbutton' ) 
        self.lowHueSlider = ttk.Scale(self.threshFrame1, variable = lowHueValue, from_= 0 , to =255, orient = "horizontal")
        self.lowSatSlider = ttk.Scale(self.threshFrame2, variable = lowSatValue, from_= 0 , to =255, orient = "horizontal")
        self.lowLumaSlider = ttk.Scale(self.threshFrame3, variable = lowLumaValue, from_= 0 , to =255, orient = "horizontal")
        self.highHueSlider = ttk.Scale(self.threshFrame4, variable = highHueValue, from_= 0 , to =255, orient = "horizontal")
        self.highSatSlider = ttk.Scale(self.threshFrame5, variable = highSatValue, from_= 0 , to =255, orient = "horizontal")
        self.highLumaSlider = ttk.Scale(self.threshFrame6, variable = highLumaValue, from_= 0 , to =255, orient = "horizontal")

        self.lowHueLabel = ttk.Label(self.threshFrame1, text =   "        lowHue    ",style = 'gray30.TLabel')
        self.lowSatLabel = ttk.Label(self.threshFrame2, text =   "        lowSat     ", style = 'gray30.TLabel')
        self.lowLumaLabel = ttk.Label(self.threshFrame3, text =  "        lowLuma ", style = 'gray30.TLabel')
        self.highHueLabel = ttk.Label(self.threshFrame4, text =  "        highHue  ", style = 'gray30.TLabel')
        self.highSatLabel = ttk.Label(self.threshFrame5, text =  "        highSat    ", style = 'gray30.TLabel')
        self.highLumaLabel = ttk.Label(self.threshFrame6, text = "        highLuma", style = 'gray30.TLabel')

        self.threshFrame6.pack(expand=True, side=BOTTOM, fill = BOTH, anchor=S)
        self.threshFrame5.pack(expand=True, side=BOTTOM, fill = BOTH, anchor=S)
        self.threshFrame4.pack(expand=True, side=BOTTOM, fill = BOTH, anchor=S)
        self.threshFrame3.pack(expand=True, side=BOTTOM, fill = BOTH, anchor=S)
        self.threshFrame2.pack(expand=True, side=BOTTOM, fill = BOTH, anchor=S)
        self.threshFrame1.pack(expand=True, side=BOTTOM, fill = BOTH, anchor=S)
        
        self.threshCheckbox.pack( fill=BOTH, side=LEFT)
        self.threshLabel.pack( fill=BOTH, side=LEFT)
        
        
        self.lowHueLabel.pack( expand=True, fill=X, side=LEFT)
        self.lowHueSlider.pack( expand=True, fill=X, side=LEFT)
        
        self.lowSatLabel.pack(expand=True, fill=X, side=LEFT)
        self.lowSatSlider.pack(expand=True, fill=X, side=LEFT)
        
        self.lowLumaLabel.pack(expand=True, fill=X, side=LEFT)
        self.lowLumaSlider.pack(expand=True, fill=X, side=LEFT)

        self.highHueLabel.pack(expand=True, fill=X, side=LEFT)
        self.highHueSlider.pack(expand=True, fill=X, side=LEFT)

        self.highSatLabel.pack(expand=True, fill=X, side=LEFT)
        self.highSatSlider.pack(expand=True, fill=X, side=LEFT)

        self.highLumaLabel.pack(expand=True, fill=X, side=LEFT)
        self.highLumaSlider.pack(expand=True, fill=X, side=LEFT)
        
        self.threshFrame.pack( side=TOP, fill = X)

        #Dumb frame
        self.dumbFrame = ttk.Frame(self, width = self.width, style='gray25.TFrame') 
        self.dumbFrame.pack( side=TOP, fill = X, expand= True)

        #Set bar and Select face
        self.setBarFrame = ttk.Frame(self, width = self.width, style = 'gray30.TFrame') 
        self.setBarButton = ttk.Button(self.setBarFrame, text="Set Bar", command= canvas.setBar)
        self.setFaceText = ttk.Label(self.setBarFrame, text =   "                       Select Face:",style = 'gray30.TLabel')
        self.setFace = ttk.Spinbox(self.setBarFrame, from_=0, to=100, textvariable= selectedFace,wrap=True,width=40)

        
        self.setBarButton.pack( side=LEFT, fill = X,anchor=N)
        # self.barTrackCheckbox.pack( side=LEFT, fill = X,anchor=N)
        self.setFaceText .pack( side=LEFT,anchor=N,expand=True, fill = BOTH)
        
        self.setFace.pack_propagate(0)
        self.setFace.pack()
        self.setBarFrame.pack( side=TOP, fill = X)

        #Start count
        global timer
        global barCount
        self.gameFrame = ttk.Frame(self,width= 100,style = 'gray30.TFrame')
        self.startButton = ttk.Button(self.gameFrame, text="Start", command = self.start)
        self.startButton.pack_propagate(0)
        self.resetButton = ttk.Button(self.gameFrame, text="Reset", command = self.reset)
        self.timerLabel = ttk.Label(self.gameFrame, text=str(timer), style='clock.TLabel')
        self.counterLabel = ttk.Label(self.gameFrame, text=str(barCount), style = 'counter.TLabel')
        
        self.gameFrame.pack(side=TOP)
        self.counterLabel.pack(fill=BOTH, side=LEFT, expand=True)
        self.startButton.pack( side=LEFT)
        self.resetButton.pack(fill=X, side=LEFT)
        self.timerLabel.pack(fill=BOTH, side=LEFT)

        
        self.counterFrame = ttk.Frame(self)
        

        self.counterFrame.pack(side=TOP)
        


        #Start stop play and next
        self.playerFrame = ttk.Frame(self, width= 300)
        self.playButton = ttk.Button(self.playerFrame, command = self.play)
        self.stopButton = ttk.Button(self.playerFrame, text="S", command = self.stop)
        self.continueButton = ttk.Button(self.playerFrame, text="C", command = self.cont)
        self.previousButton = ttk.Button(self.playerFrame, text="<", command = self.prev)
        self.nextButton = ttk.Button(self.playerFrame, text=">", command = self.next)

        #Bind the icons
        self.playButton.configure(image = self.iconPlay)
        self.playButton.image = self.iconPlay
        self.stopButton.configure(image = self.iconStop)
        self.stopButton.image = self.iconStop
        self.continueButton.configure(image = self.iconContinue)
        self.continueButton.image = self.iconStop
        self.previousButton.configure(image = self.iconBack)
        self.previousButton.image = self.iconBack
        self.nextButton.configure(image = self.iconNext)
        self.nextButton.image = self.iconNext


        self.playerFrame.pack(expand=True,anchor=S)
        self.playButton.pack( side=LEFT)
        self.stopButton.pack( side=LEFT)
        self.continueButton.pack( side=LEFT)
        self.previousButton.pack( side=LEFT)
        self.nextButton.pack( side=LEFT)

    def reset(self):
        global run
        global timer
        timer = 60.00
        run = False
        self.contadorBarras.reset()
        timerStr = "{:.2f}".format(timer)
        self.timerLabel.configure(text=timerStr)
        

    def start(self):
        global run
        run = True
        self.contadorBarras.reset()
        self.contadorBarras.countBar()
        self.contador()

    def contador(self):
        global timer
        global run
        global barCount
        self.counterLabel.configure(text=barCount)
        if(timer > 0.00 and run):
            self.contadorBarras.countBar()
            timerStr = "{:.2f}".format(timer)
            self.timerLabel.configure(text=timerStr)
            timer -= 0.01
            self.timerLabel.after(10, self.contador)
        else:
            run = False
            timer = 60.0

        
    def play(self):
        global isPlaying
        global atualFrame
        atualFrame = 0
        isPlaying = True

    def stop(self):
        global isPlaying
        isPlaying = False
    
    def cont(self):
        global isPlaying
        isPlaying = True

    def next(self):
        global atualFrame
        atualFrame += 1

    def prev(self):
        global atualFrame
        atualFrame -= 1



class ContadorBarras():
    state = 0
    def __init__(self):
        global barCount
        self.state = 0
        barCount = 0
    
    def countBar(self):
        global run
        global faceState
        global barCount
        if run:
            
            if(self.state == 0):
                if(faceState == "down"):
                    self.state = 1
            elif(self.state == 1):
                if(faceState == "up"):
                    print("bar")
                    self.state = 2
                    barCount += 1
            elif(self.state == 2):
                if(faceState == "down"):
                    self.state = 0

    def reset(self):
        global barCount
        barCount = 0
        self.state = 0 
        self.counter = 0




    

    
        

####################################################################################
#Classe qeu define o canvas
class CanvasArea(ttk.Frame):
    width = 500
    height = 400
    canvasLabel= None
    videoPipeline = None
    style = "canvas.TFrame"
    clickBar = 2
    mouseCoord = None
    

    def __init__(self,parent,path, mode):
        super().__init__(parent)
        self.propagate(False)
        self.configure(width = self.width, height = self.height, style = self.style)
        self.videoPipeline = VideoPipeline(self.width, self.height, path)
        self.canvasLabel = Canvas(self,width=str(self.width),height=str(self.height))
        self.canvasLabel.bind("<Motion>", self.setMouseCoordinates)
        self.canvasLabel.bind("<Button-1>", self.mouseClick)
        self.setThumbnail(mode)
        
    def setThumbnail(self,mode):
        global isPlaying
        if(mode == "webcam"):
            isPlaying = True
        self.play()
        
    #Take a image and push to screen
    def flush(self, img):
        img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        img = convertToTk(img)
        self.canvasLabel.create_image( 250,200,image = img)
        self.canvasLabel.image = img
        #Draw the bar
        self.drawBar()
    
    #Draw bar with or whithout tracking
    def drawBar(self):
        global barPoint1
        global barPoint2
        global barHeightTracking
        global barTrack
        self.canvasLabel.create_line(barPoint1[0],barPoint1[1],barPoint2[0],barPoint2[1],width = 10,fill = "purple",)
        self.canvasLabel.pack(side=LEFT,padx=10,pady=10)

    def play(self):
        self.flush(self.videoPipeline.render())
        #Melhoria deltaTime
        self.canvasLabel.after(self.videoPipeline.deltaTime, self.play)
        
    def setBar(self):
        global barPoint1
        global barPoint2
        #Clean the bar
        barPoint1 = (0,0)
        barPoint2 = (0,0)
        #clickbar
        self.clickBar = 0

    def mouseClick(self,event):
        global barPoint1
        global barPoint2
        global canvas
        print("click")
        global barHeigth
        if(self.clickBar == 0):
            barPoint1 = self.mouseCoord
            barPoint2 = (barPoint1[0]+10, barPoint1[1])
            barHeigth = barPoint1[1]
            self.clickBar = 1
        elif(self.clickBar == 1):
            barPoint2 = (self.mouseCoord[0], barPoint1[1])
            self.clickBar = 2
            
    def setMouseCoordinates(self,event):
        self.mouseCoord= (event.x, event.y)
    
    def resize(self,width,
                height):
        self.width = width
        self.height = height
        self.configure(width = self.width, height = self.height)

    

###################################################################################
#Classe que defina a engine do video##
#Todos os filtros esta'o aqui
class VideoPipeline():
    cap = None
    img = None
    firstFrame = None
    bufferFrame = None
    heightCanvas = None
    widthCanvas = None
    aspectRatioCanvas = None
    path = None
    
    frameCount = 0
    global atualFrame
    fps = 0
    deltaTime = 0
    
    heightCap = None
    widthCap = None
    aspectRatioCap = None

    play = False
    global isPlaying

    #facedetect
    fd = None

    #subtrator
    backSub = cv.createBackgroundSubtractorMOG2()
    def __init__(self, width, height, path):
        if(path == "none"):
            self.cap = cv.VideoCapture(0)
        else:
            self.path = path
            self.cap = cv.VideoCapture(path)
        #Informacoes de frame
        self.frameCount = self.cap.get(cv.CAP_PROP_FRAME_COUNT)
        self.fps = self.cap.get(cv.CAP_PROP_FPS)
        self.deltaTime = int(1/self.fps * 1000)
        print("Frame per second: "+str(self.fps))
        print("Framecout: "+str(self.frameCount))
        print("Deltatime: "+str(self.deltaTime)+"ms")
        #Video native resolution
        self.heightCap = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT) 
        self.widthCap =  self.cap.get(cv.CAP_PROP_FRAME_WIDTH) 
        self.aspectRatioCap = self.widthCap / self.heightCap
        print("Native resolution: "+str(self.widthCap)+"x"+str(self.heightCap)+" | AspectRatio: "+str(self.aspectRatioCap))
        #Canvas resolution 
        self.heightCanvas = height
        self.widthCanvas = width
        self.aspectRatioCanvas =   self.widthCanvas / self.heightCanvas
        print("Canvas resolution: "+str(self.widthCanvas)+"x"+str(self.heightCanvas)+" | AspectRatio: "+str(self.aspectRatioCanvas))
        #facedetect
        self.fd = faceDetect()

    #Captura o frame
    def capture(self):
        global isPlaying
        global atualFrame
        #print("nFrame:"+str(atualFrame)+" de "+str(self.frameCount))
        #Seguranca
        if(atualFrame > self.frameCount):
            atualFrame = self.frameCount
        if(atualFrame < 0):
            atualFrame = 0

        #Se o meu frame atual for maior que meu frame count
        if(self.play):
            self.cap.set(cv.CAP_PROP_POS_FRAMES, atualFrame)
            _,img = self.cap.read(0)   #Aquizicao
            #Automatic stop at final frame
            if((atualFrame < (self.frameCount - 1)) or (self.frameCount == -1)):
                atualFrame += 1
            else:
                isPlaying = False
                self.play = False
        else:
            self.cap.set(cv.CAP_PROP_POS_FRAMES, atualFrame)
            _,img = self.cap.read(0)   #Aquizicao
        self.play = isPlaying
        return img



    #Renderiza um frame do cap
    def render(self):
        img = self.capture()
        img = self.zoom(img)
        img = self.autoFit(img)
        img = self.flip(img)
        img = self.blur(img)        #blur
        img = self.histogram(img)   #histogram equalization
        img = self.saturation(img)  #saturation adjust
        img = self.luma(img)  #Luma adjust
        img = self.bgSub(img)       #bg subtractor
        img = self.tresh(img)       #Threshold
        img = self.fd.detect(img)
        return img
    
    def zoom(self, img):
        altura, largura = img.shape[:2]
        if(zoomValue.get() > 0):
            scaleFactor = zoomValue.get()
            nova_altura = int(altura * scaleFactor)
            nova_largura = int(largura * scaleFactor)
            imagem_ampliada = cv.resize(img, (nova_largura, nova_altura), interpolation=cv.INTER_LINEAR)

            corte_vertical = int((nova_altura - altura) / 2)
            corte_horizontal = int((nova_largura - largura) / 2)

            imagem_cortada = imagem_ampliada[corte_vertical:corte_vertical+altura, corte_horizontal:corte_horizontal+largura]
        elif(zoomValue.get() < 0):
            scaleFactor = 1.00 - float((zoomValue.get()*-1)*0.1)
            nova_altura = int(altura * scaleFactor)
            nova_largura = int(largura * scaleFactor)

            imagem_reduzida = cv.resize(img, (nova_largura, nova_altura), interpolation=cv.INTER_LINEAR)

            dif_altura = altura - nova_altura
            dif_largura = largura - nova_largura
            pad_vertical_topo = dif_altura // 2
            pad_vertical_base = dif_altura - pad_vertical_topo
            pad_horizontal_esquerda = dif_largura // 2
            pad_horizontal_direita = dif_largura - pad_horizontal_esquerda
            imagem_cortada = cv.copyMakeBorder(imagem_reduzida, pad_vertical_topo, pad_vertical_base, pad_horizontal_esquerda, pad_horizontal_direita, cv.BORDER_CONSTANT, value=(0, 0, 0))
        else:
            scaleFactor = 1
            nova_altura = int(altura * scaleFactor)
            nova_largura = int(largura * scaleFactor)
            imagem_ampliada = cv.resize(img, (nova_largura, nova_altura), interpolation=cv.INTER_LINEAR)

            corte_vertical = int((nova_altura - altura) / 2)
            corte_horizontal = int((nova_largura - largura) / 2)

            imagem_cortada = imagem_ampliada[corte_vertical:corte_vertical+altura, corte_horizontal:corte_horizontal+largura]

        return imagem_cortada


    #faz o autofit da imagem para a resolução do Canvas
    def autoFit(self, img):
        #ajuste pela altura
        
        if self.aspectRatioCap >= self.aspectRatioCanvas:
            scaleFactor = self.heightCanvas / self.heightCap
            newWidth =  scaleFactor * self.widthCap
            newHeight = scaleFactor * self.heightCap 
            centerOffsetI = (int(newWidth) - int(self.widthCanvas)) / 2
            centerOffsetF = newWidth - centerOffsetI
            newRes = (int(newWidth), int(newHeight))
            img_resize = cv.resize(img, newRes, interpolation= cv.INTER_LINEAR)
            img_resize = img_resize[:, int(centerOffsetI):int(centerOffsetF),:]

        else:#Ajuste pelo comprimento
            scaleFactor = self.widthCanvas / self.widthCap
            newWidth =  scaleFactor * self.widthCap
            newHeight = scaleFactor * self.heightCap 
            centerOffsetI = (int(newHeight) - int(self.heightCanvas)) / 2
            centerOffsetF = newHeight - centerOffsetI
            newRes = (int(newWidth), int(newHeight))
            img_resize = cv.resize(img, newRes, interpolation= cv.INTER_LINEAR)
            img_resize = img_resize[int(centerOffsetI):int(centerOffsetF), :,:]

        return img_resize
    #Flip img
    def flip(self, img):
        if(flipCheck.get()):
            img = cv.flip(img, 1)
        return img
    #Aplica o efeito blur
    def blur(self, img):
        if(blurCheck.get()):
            return cv.medianBlur(img,(blurValue.get()*2 + 1))
        else:
            return img 

    #Aplica equalizacao do histograma
    def histogram(self, img):
        if(histogramCheck.get()):
            imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            imgLuma = imgHSV[:,:,2]
            clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            imgLuma = clahe.apply(imgLuma)
           #imgLuma = cv.equalizeHist(imgLuma)
            imgHSV[:,:,2] = imgLuma
            img = cv.cvtColor(imgHSV, cv.COLOR_HSV2BGR)
            return img 
        else:
            return img 
        
    #Ajuste de saturacao
    def saturation(self, img):
        if(satCheck.get()):
            imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            imgSat = imgHSV[:,:,1]
            imgSat_16 = imgSat.astype(np.int16)
            imgSat_16 += satValue.get()
            imgSat_16 = np.clip(imgSat_16,0,255)
            imgSat = imgSat_16.astype(np.uint8)
            imgHSV[:,:,1] = imgSat
            img = cv.cvtColor(imgHSV, cv.COLOR_HSV2BGR)
            return img 
        else:
            return img 
        
    #Ajuste de saturacao
    def luma(self, img):
        if(lumaCheck.get()):
            imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            imgLuma = imgHSV[:,:,2]
            imgLuma_16 = imgLuma.astype(np.int16)
            imgLuma_16 += lumaValue.get()
            imgLuma_16 = np.clip(imgLuma_16,0,255)
            imgLuma = imgLuma_16.astype(np.uint8)
            imgHSV[:,:,2] = imgLuma
            img = cv.cvtColor(imgHSV, cv.COLOR_HSV2BGR)
            return img 
        else:
            return img 
        
    #Aplica o efeito blur
    def bgSub(self, img):
        if(bgSubCheck.get()):
            fgMask = self.backSub.apply(img)
            masked = cv.bitwise_and(img, img, mask=fgMask)
            return masked
        else:
            return img 
    #Faz o trhreshold da imagem no pizel format HSV
    def tresh(self,img):
        if(threshCheck.get()):
            lowHue = lowHueValue.get()
            lowSat = lowSatValue.get()
            lowLuma = lowLumaValue.get()
            highHue = highHueValue.get()
            highSat = highSatValue.get()
            highLuma = highLumaValue.get()
            imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            maskThreshold = cv.inRange(imgHSV, (lowHue, lowSat, lowLuma), (highHue, highSat, highLuma))
            img = cv.bitwise_and(img, img, mask=maskThreshold)
            return img
        else:
            return img 
        
        
###################################################################################
#Classe do detector de face
class faceDetect():
    face_detector = None
    faces = None
    y = 0
    def __init__(self):
        self.face_detector = cv.FaceDetectorYN_create("yunet.onnx", "", (0, 0))

    def detect(self,img):
        global headHeigth
        global barHeigth
        global selectedFace
        global faceState

        height, width, _ = img.shape
        self.face_detector.setInputSize((width, height))
        _, self.faces = self.face_detector.detect(img)
        self.faces = self.faces if self.faces is not None else []
        index = 0
        font = cv.FONT_HERSHEY_SIMPLEX
        for face in self.faces:
            box = list(map(int, face[:4]))
            #altura da face(aresta inferior)
            color=(0,255,255)
            thickness = 1
            cv.rectangle(img, box, color, thickness, cv.LINE_AA)
            cv.putText(img, str(index), (box[0],box[1]), font, 1, color, thickness, cv.LINE_AA)
            #Seleciona a Face
            if(index == selectedFace.get()):
                #cordenadas da face
                box = list(map(int, face[:4]))
                #altura da face(aresta inferior)
                self.y = face[1] + face[3]
                if(self.y <= barHeigth):
                    color=(0,255,0)
                else:
                    color = (0, 0, 255)
                thickness = 3
                cv.rectangle(img, box, color, thickness, cv.LINE_AA)
                cv.putText(img, str(index), (box[0],box[1]), font, 1, color, thickness, cv.LINE_AA)
            index += 1

        headHeigth = self.y 
        if(headHeigth < barHeigth):
            faceState  = "up"
        else:
            faceState = "down"
        #print(faceState)
        
        return img
    
    
if __name__ == "__main__":
    app = App()
    app.mainloop()


