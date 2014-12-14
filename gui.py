# coding: utf-8
######################################## ----- GUI do cliente ----- ########################################

from Tkinter import *
from tkFileDialog import *
from PIL import ImageTk, Image

# Cores
CARROT_COLOR = '#e67e22';
POMEGRANATE_COLOR = '#c0392b';
CLOUDS_COLOR = '#ecf0f1';
MIDNIGHT_BLUE = '#2c3e50';

# Textos da GUI
TXT_TITULO = '  RPC para processamento de imagens'
TXT_BTN_CI = 'Carregar Imagem ...'
TXT_BTN_ENVIAR = 'Enviar'
TXT_BTN_EDITAR = 'Editar Imagem'
TXT_BTN_DET = 'Deteccao de Face'
TXT_BTN_OPC = 'Opcoes'
TXT_BTN_SAIR = 'Sair'

# Nome da Imagem padrão
NO_IMG = 'NoImage.jpg'

############################ IMPORTANTE ############################
# Variável para armazenar a imagem que será enviada para o servidor
# Sem redimensionamentos
img = Image.open(NO_IMG)

# Variável para armazenar a url de resposta do servidor
url = ''

# Variáveis referente a manipulação da imagem
width = ''
height = ''
effects = ''

# Dados para fazer a conexão com o servidor
ip = '127.0.0.1' # IP padrão
porta = '6666' # porta padrão
####################################################################

# Tipos de arquivos que podem ser abertos
TIPOS = [('Image Files', ('*.jpg', '*.gif', '*.png')), ('JPEG','*.jpg'), ('GIF','*.gif'), ('PNG','*.png')]




def center(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def addTitulo(root):
	foto = PhotoImage(file='Images-48.png')
	texto = Label(root, image=foto, text=TXT_TITULO, compound=LEFT, font=('Helvetica','18','bold'),
		borderwidth=2, highlightthickness=2)
	texto.photo = foto
	texto['foreground'] = CLOUDS_COLOR
	texto['background'] = POMEGRANATE_COLOR
	texto['width'] = 1000

	return texto

def addRodape(root):
	texto = Label(root, text='Copyright © 2014 - Todos os direitos reservados - Evandro Loschi / Gian Carlos', font=('Helvetica','10'),
		borderwidth=2, highlightthickness=2, padx=20, pady=20)
	texto['foreground'] = CLOUDS_COLOR
	texto['background'] = POMEGRANATE_COLOR
	texto['width'] = 150

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
	def __init__(self, root, caixaBotao, caixaImagem, nomeBtn, largura = 10, cor = POMEGRANATE_COLOR):
		self.root = root
		self.caixaBotao = caixaBotao
		self.caixaImagem = caixaImagem

		# Configuraçoes do botão
		self.button = Button(self.caixaBotao) 
		self.button['text']= nomeBtn
		self.button['foreground'] = CLOUDS_COLOR
		self.button['background'] = cor
		self.button['width'] = largura
		self.button.bind('<Button>', self.trata_eventos) 
		self.button.pack(padx=6, pady=6)

		# Caminho da imagem aberta
		self.caminhoImg = ''

	def trata_eventos(self, event):
		if str(self.button['text']) == TXT_BTN_CI:
			self.caminhoImg = askopenfilename(filetypes=TIPOS)

			try:
				# Atualiza a variável que é responsável por armazenar a imagem que será enviada
				global img
				img = Image.open(self.caminhoImg)

				# Atualizando a Imagem
				foto = abrirImg(self.caminhoImg, 598, 378)
				self.caixaImagem.configure(image=foto)

				# Para manter a referência
				self.caixaImagem.image = foto
			except:
				#raise
				pass
		elif self.button['text'] == TXT_BTN_ENVIAR:
			####################################################
			####################################################
			####################################################
			# ****** FAZER AQUI A CONEXÃO COMO SERVIDOR ****** #
			####################################################
			####################################################
			####################################################
			pass
		elif self.button['text'] == TXT_BTN_EDITAR:
			DialogEdit(self.root)
			#* Manipulação da Imagem *
		elif self.button['text'] == TXT_BTN_DET:
			# * Detecção de Face *
			pass
		elif self.button['text'] == TXT_BTN_OPC:
			DialogOpc(self.root)
		elif self.button['text'] == TXT_BTN_SAIR:
			self.root.destroy()
        	self.root = None

class DialogOpc:
	def __init__(self, root):
		# Configuraçoes da janela
		self.top = Toplevel(root)
		self.top.wm_title(TXT_BTN_OPC)
		self.top.geometry('250x100')
		center(self.top)
		self.top.resizable(0,0)
		self.top.configure(background=CARROT_COLOR, bd=5, highlightthickness=2)

		# Labels
		Label(self.top, text='IP: ', background=CARROT_COLOR,
			foreground=CLOUDS_COLOR).grid(row=0)
		Label(self.top, text='Porta: ', background=CARROT_COLOR,
			foreground=CLOUDS_COLOR).grid(row=1)

		# Inputs
		self.entradaIp = Entry(self.top)
		self.entradaIp.insert(0, ip)
		self.entradaPorta = Entry(self.top)
		self.entradaPorta.insert(0, porta)

		self.entradaIp.grid(row=0, column=1, padx=2, pady=2)
		self.entradaPorta.grid(row=1, column=1, padx=2, pady=2)

		# Botão de OK
		self.btn = Button(self.top, text='OK', background=POMEGRANATE_COLOR,
			foreground=CLOUDS_COLOR,command=self.ok)
		self.btn.grid(row=2, column=1, padx=4, pady=4)
	def ok(self):
		# Atualizando os parâmetros para comunicação com o servidor
		global ip
		global porta
		ip = self.entradaIp.get()
		porta = self.entradaPorta.get()

		# Destruindo a caixa de dialogo
		self.top.destroy()

class DialogEdit:
	def __init__(self, root):
		# Configuraçoes da janela
		self.top = Toplevel(root)
		self.top.wm_title(TXT_BTN_EDITAR)
		self.top.geometry('250x120')
		center(self.top)
		self.top.resizable(0,0)
		self.top.configure(background=CARROT_COLOR, bd=5, highlightthickness=2)

		# Labels
		Label(self.top, text='Width: ', background=CARROT_COLOR,
			foreground=CLOUDS_COLOR).grid(row=0)
		Label(self.top, text='Height: ', background=CARROT_COLOR,
			foreground=CLOUDS_COLOR).grid(row=1)
		Label(self.top, text='Effects: ', background=CARROT_COLOR,
			foreground=CLOUDS_COLOR).grid(row=2)

		# Inputs
		self.entradaWidth = Entry(self.top)
		self.entradaHeight = Entry(self.top)
		self.entradaEffects = Entry(self.top)

		self.entradaWidth.grid(row=0, column=1, padx=2, pady=2)
		self.entradaHeight.grid(row=1, column=1, padx=2, pady=2)
		self.entradaEffects.grid(row=2, column=1, padx=2, pady=2)

		# Botão de OK
		self.btn = Button(self.top, text='OK', background=POMEGRANATE_COLOR,
			foreground=CLOUDS_COLOR,command=self.ok)
		self.btn.grid(row=3, column=1, padx=4, pady=4)
	def ok(self):
		# Atualizando os parâmetros para comunicação com o servidor
		global width
		global height
		global effects
		width = self.entradaWidth.get()
		height = self.entradaHeight.get()
		effects = self.entradaEffects.get()

		# Destruindo a caixa de dialogo
		self.top.destroy()



		
if __name__ == '__main__':
	try:
		# Configuraçoes do root
		root = Tk()
		root.wm_title(TXT_TITULO)
		root.geometry('800x740')
		center(root)
		root.resizable(0,0)
		root.configure(background=CARROT_COLOR, bd=5, highlightthickness=2)

		# Container com o título
		textoTitulo = addTitulo(root)
		textoTitulo.pack()

		# Container onde a imagem carregada ficará
		caixaImagem = caixaImg(root, NO_IMG)

		# Container com o primeiro grupo de botões
		caixaBtn1 = caixaBtn(root)
		caixaBtn1.pack()

		# Botões inferiores (carregar imagem, enviar)
		Btn(root, caixaBtn1, caixaImagem, TXT_BTN_CI, 15)
		Btn(root, caixaBtn1, caixaImagem, TXT_BTN_ENVIAR, 15)

		caixaImagem.pack()

		# Container com o segundo grupo de botões
		caixaBtn2 = caixaBtn(root)
		caixaBtn2.pack()

		# Botões inferiores (editar, Dtecção, opções, sair)
		Btn(root, caixaBtn2, caixaImagem, TXT_BTN_EDITAR, 15, MIDNIGHT_BLUE)
		Btn(root, caixaBtn2, caixaImagem, TXT_BTN_DET, 15, MIDNIGHT_BLUE)
		Btn(root, caixaBtn2, caixaImagem, TXT_BTN_OPC)
		Btn(root, caixaBtn2, caixaImagem, TXT_BTN_SAIR)

		# Container com o rodapé
		textoRodape = addRodape(root)
		textoRodape.pack()

		root.mainloop()
	except:
		raise
		#pass