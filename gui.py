# coding: utf-8

from Tkinter import *
from tkFileDialog import *
from PIL import ImageTk, Image

CARROT_COLOR = '#e67e22';
POMEGRANATE_COLOR = '#c0392b';
CLOUDS_COLOR = '#ecf0f1';

TXT_BTN_CI = 'Carregar Imagem'
TXT_BTN_ENVIAR = 'Enviar'
TXT_BTN_SAIR = 'Sair'

TIPOS = [('Image Files', ('*.jpg', '*.gif', '*.png')), ('JPEG','*.jpg'), ('GIF','*.gif'), ('PNG','*.png')]

class Titulo:
	def __init__(self, root):
		self.texto = Label(root, text='RPC para processamento de imagens', font=('Helvetica','18','bold'))
		self.texto['foreground'] = CLOUDS_COLOR
		self.texto['background'] = POMEGRANATE_COLOR
		self.texto['width'] = 100
		self.texto.pack()

class CaixaImg:
	def __init__(self, root, caminho):
		self.img = Image.open(caminho)
		self.foto = ImageTk.PhotoImage(self.img)
		self.painel = Label(root, image=self.foto)
		self.painel.image = self.foto # Para manter a referência
		self.painel.pack()

class CaixaBtn:
	def __init__(self, root):
		self.container = Frame(root)
		self.container['background'] = CARROT_COLOR
		self.container.pack()

class Btn:
	def __init__(self, root, container, nomeBtn, largura = 10):
		self.root = root
		self.container = container

		self.button = Button(self.container) 
		self.button['text']= nomeBtn
		self.button['foreground'] = CLOUDS_COLOR
		self.button['background'] = POMEGRANATE_COLOR
		self.button['width'] = largura
		self.button.bind('<Button>', self.trata_eventos) 
		self.button.pack(padx=10, pady=10)

		# Caminho da imagem aberta
		self.caminhoImg = ''

	def trata_eventos(self, event):
		if self.button['text'] == TXT_BTN_CI:
			self.caminhoImg = askopenfilename(filetypes=TIPOS)
		elif self.button['text'] == TXT_BTN_SAIR:
			self.root.destroy()
        	self.root = None

try:
	# Configuraçoes do root
	root = Tk()
	root.wm_title('RPC para processamento de imagens')
	root.geometry('800x600')
	root.resizable(0,0)
	root.configure(background=CARROT_COLOR, bd=5)

	Titulo(root)

	# Container com o primeiro grupo de botões
	caixaBtn1 = CaixaBtn(root)

	Btn(root, caixaBtn1.container, TXT_BTN_CI, 15)

	CaixaImg(root, 'ceu-azul1.jpg')

	# Container com o segundo grupo de botões
	caixaBtn2 = CaixaBtn(root)

	Btn(root, caixaBtn2.container, TXT_BTN_ENVIAR) 
	Btn(root, caixaBtn2.container, TXT_BTN_SAIR) 

	root.mainloop()
except:
	raise
	#pass