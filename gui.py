# coding: utf-8

from Tkinter import *
from tkFileDialog import *
from PIL import ImageTk, Image

CARROT_COLOR = '#e67e22';
POMEGRANATE_COLOR = '#c0392b';
CLOUDS_COLOR = '#ecf0f1';

TXT_TITULO = 'RPC para processamento de imagens'
TXT_BTN_CI = 'Carregar Imagem'
TXT_BTN_ENVIAR = 'Enviar'
TXT_BTN_SAIR = 'Sair'

NO_IMG = 'NoImage.jpg'

TIPOS = [('Image Files', ('*.jpg', '*.gif', '*.png')), ('JPEG','*.jpg'), ('GIF','*.gif'), ('PNG','*.png')]

def addTitulo(root):
	texto = Label(root, text=TXT_TITULO, font=('Helvetica','18','bold'),
		borderwidth=2, highlightthickness=2)
	texto['foreground'] = CLOUDS_COLOR
	texto['background'] = POMEGRANATE_COLOR
	texto['width'] = 100

	return texto

def abrirImg(caminho, width, height):
	img = Image.open(caminho)
	# Redimensionando a imagem com os parâmetros especificados
	img = img.resize((width, height), Image.ANTIALIAS)
	foto = ImageTk.PhotoImage(img)

	return foto

def caixaImg(root, caminho):
	foto = abrirImg(caminho, 598, 378)

	painel = Label(root, image=foto, width=600, height=380,
		borderwidth=2, highlightthickness=2, background='white')
	# Para manter a referência
	painel.image = foto

	return painel

def caixaBtn(root):
	container = Frame(root)
	container['background'] = CARROT_COLOR

	return container

class Btn:
	def __init__(self, root, caixaBotao, caixaImagem, nomeBtn, largura = 10):
		self.root = root
		self.caixaBotao = caixaBotao
		self.caixaImagem = caixaImagem

		# Configuraçoes do botão
		self.button = Button(self.caixaBotao) 
		self.button['text']= nomeBtn
		self.button['foreground'] = CLOUDS_COLOR
		self.button['background'] = POMEGRANATE_COLOR
		self.button['width'] = largura
		self.button.bind('<Button>', self.trata_eventos) 
		self.button.pack(padx=12, pady=12)

		# Caminho da imagem aberta
		self.caminhoImg = ''

	def trata_eventos(self, event):
		if self.button['text'] == TXT_BTN_CI:
			self.caminhoImg = askopenfilename(filetypes=TIPOS)

			try:
				# Atualizando a Imagem
				foto = abrirImg(self.caminhoImg, 598, 378)
				self.caixaImagem.configure(image=foto)
				# Para manter a referência
				self.caixaImagem.image = foto
			except:
				#raise
				pass
		elif self.button['text'] == TXT_BTN_SAIR:
			self.root.destroy()
        	self.root = None

try:
	# Configuraçoes do root
	root = Tk()
	root.wm_title(TXT_TITULO)
	root.geometry('800x600')
	root.resizable(0,0)
	root.configure(background=CARROT_COLOR, bd=5)

	# Container com o título
	texto = addTitulo(root)
	texto.pack()

	# Container onde a imagem carregada ficará
	caixaImagem = caixaImg(root, NO_IMG)

	# Container com o primeiro grupo de botões
	caixaBtn1 = caixaBtn(root)
	caixaBtn1.pack()

	Btn(root, caixaBtn1, caixaImagem, TXT_BTN_CI, 15)

	caixaImagem.pack()

	# Container com o segundo grupo de botões
	caixaBtn2 = caixaBtn(root)
	caixaBtn2.pack()

	Btn(root, caixaBtn2, caixaImagem, TXT_BTN_ENVIAR) 
	Btn(root, caixaBtn2, caixaImagem, TXT_BTN_SAIR)

	root.mainloop()
except:
	raise
	#pass