# coding: utf-8
######################################## ----- GUI do cliente ----- ########################################

from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from PIL import ImageTk, Image
import requests
import urllib2

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
img = NO_IMG

# Variável para armazenar a url de resposta do servidor
urlImg = ''

headers = {'content-type': 'multipart/form-data'}
proxies = {'http': 'http://10.0.0.254:8080'}

# Variáveis referente a manipulação da imagem
width = ''
height = ''

# Efeitos
faces = 'faces'
quadriculate = 'quadriculate'
grayscale = 'grayscale'
crop = 'crop'
negative = 'negative'
greening = 'greening'
reddening = 'reddening'
bluening = 'bluening'
rotate90 = 'rotate90'
rotate180 = 'rotate180'
rotate270 = 'rotate270'

# Dados para fazer a conexão com o servidor
ip = 'localhost' # IP padrão
porta = '9999' # porta padrão
####################################################################

# Tipos de arquivos que podem ser abertos
TIPOS = [('Image Files', ('*.jpg', '*.gif', '*.png')), ('JPEG','*.jpg'), ('GIF','*.gif'), ('PNG','*.png')]



def mainWindow():
    # Configuraçoes do root
    root = Tk()
    root.wm_title(TXT_TITULO)
    root.geometry('800x740')
    center(root)
    root.resizable(0,0)
    root.configure(background=CARROT_COLOR, bd=5, highlightthickness=2)

    return root

def center(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def addTitulo(root):
    img = Image.open('Images-48.png')
    foto = ImageTk.PhotoImage(img)
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
        self.button.bind('<Button>', self.trataEventos) 
        self.button.pack(padx=6, pady=6)

        # Caminho da imagem aberta
        self.caminhoImg = ''

    def trataEventos(self, event):
        global img
        global urlImg
        global faces
        
        if str(self.button['text']) == TXT_BTN_CI:
            self.caminhoImg = askopenfilename(filetypes=TIPOS)

            try:
                # Atualiza a variável que é responsável por armazenar a imagem que será enviada
                img = self.caminhoImg

                # Atualizando a Imagem
                foto = abrirImg(self.caminhoImg, 598, 378)
                self.caixaImagem.configure(image=foto)

                # Para manter a referência
                self.caixaImagem.image = foto
            except:
                #raise

                # Exibe uma mensagem de erro
                showerror('Erro', 'Falha ao carregar a imagem!')
        elif self.button['text'] == TXT_BTN_ENVIAR:
            # Acessar: /upload_image
            # Enviar o arquivo no campo do tipo file de nome 'file'
            # Recebe o nome do arquivo armazenado ou erro de servidor
            
            try:
                # Construindo a url que será enviada ao servidor
                urlServer = 'http://' + ip + ':' + porta + '/upload_image'

                r = requests.post(urlServer, files={'file': open(img, 'rb')})
                
                # Salva a url de acesso a imagem em sua devida variável
                urlImg = r.content

                # Exibe uma mensagem de sucesso
                showinfo('Sucesso', 'Mensagem enviada com sucesso!')
            except:
                urlImg = ''

                # Exibe uma mensagem de erro
                showerror('Erro', 'Falha no envio da imagem!')
        elif self.button['text'] == TXT_BTN_EDITAR:
            if len(urlImg):
                DialogEdit(self.root)
            else:
                showwarning('Aviso', 'Nenhuma imagem enviada ao servidor!')
        elif self.button['text'] == TXT_BTN_DET:
            if len(urlImg):
                # ********** Detecção de Face **********
                # Efeitos para detecção de faces: 'faces'
                urlServer = 'http://' + ip + ':' + porta + '/apply_effects'
                r = requests.get(urlServer, params={'file': urlImg, 'effects': faces})
                
                # Obtendo a url para realizar o download da imagem alterada
                urlDownload = r.content
                
                # Obtendo a imagem alterada
                urlServer = 'http://' + ip + ':' + porta + '/' + urlDownload
                
                # Salva e exibe a imagem retornada pelo servidor
                a = open('%s' % urlDownload.split('/')[-1], 'wb')
                a.write(urllib2.urlopen(urlServer).read())
                a.close()
                Image.open('%s' % urlDownload.split('/')[-1]).show()
                ####################################################
            else:
                showwarning('Aviso', 'Nenhuma imagem enviada ao servidor!')
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
        self.top.geometry('250x125')
        center(self.top)
        self.top.resizable(0,0)
        self.top.configure(background=CARROT_COLOR, bd=5, highlightthickness=2)

        self.caixaEndereco = LabelFrame(self.top, text='Endereço', padx=5, pady=5,
            background=CARROT_COLOR, foreground=CLOUDS_COLOR)
        self.caixaEndereco.grid(sticky=E+W)

        # Labels
        Label(self.caixaEndereco, text='IP: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=0, sticky=W)
        Label(self.caixaEndereco, text='Porta: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=1, sticky=W)

        # Inputs
        self.entradaIp = Entry(self.caixaEndereco)
        self.entradaIp.insert(0, ip)
        self.entradaPorta = Entry(self.caixaEndereco)
        self.entradaPorta.insert(0, porta)

        self.entradaIp.grid(row=0, column=1, padx=2, pady=2, sticky=W)
        self.entradaPorta.grid(row=1, column=1, padx=2, pady=2, sticky=W)

        # Botão de OK
        self.btn = Button(self.top, text='OK', background=POMEGRANATE_COLOR,
            foreground=CLOUDS_COLOR,command=self.ok)
        self.btn.grid(row=12, column=0, padx=4, pady=4)
        
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
        self.top.geometry('250x375')
        center(self.top)
        self.top.resizable(0,0)
        self.top.configure(background=CARROT_COLOR, bd=5, highlightthickness=2)

        self.caixaRedimensionar = LabelFrame(self.top, text='Redimensionar', padx=5, pady=5,
            background=CARROT_COLOR, foreground=CLOUDS_COLOR)
        self.caixaEfeitos = LabelFrame(self.top, text='Efeitos', padx=5, pady=5,
            background=CARROT_COLOR, foreground=CLOUDS_COLOR)

        self.caixaRedimensionar.grid(sticky=E+W)
        self.caixaEfeitos.grid(sticky=E+W)

        # Labels
        Label(self.caixaRedimensionar, text='Width: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=0, sticky=W)
        Label(self.caixaRedimensionar, text='Height: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=1, sticky=W)
        Label(self.caixaEfeitos, text='Quadriculate: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=2, sticky=W)
        Label(self.caixaEfeitos, text='Grayscale: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=3, sticky=W)
        Label(self.caixaEfeitos, text='Crop: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=4, sticky=W)
        Label(self.caixaEfeitos, text='Negative: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=5, sticky=W)
        Label(self.caixaEfeitos, text='Greening: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=6, sticky=W)
        Label(self.caixaEfeitos, text='Reddening: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=7, sticky=W)
        Label(self.caixaEfeitos, text='Bluening: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=8, sticky=W)
        Label(self.caixaEfeitos, text='Rotate 90: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=9, sticky=W)
        Label(self.caixaEfeitos, text='Rotate 180: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=10, sticky=W)
        Label(self.caixaEfeitos, text='Rotate 270: ', background=CARROT_COLOR,
            foreground=CLOUDS_COLOR).grid(row=11, sticky=W)

        # Inputs
        self.entradaWidth = Entry(self.caixaRedimensionar)
        self.entradaHeight = Entry(self.caixaRedimensionar)
        self.entradaWidth.grid(row=0, column=1, padx=2, pady=2, sticky=W)
        self.entradaHeight.grid(row=1, column=1, padx=2, pady=2, sticky=W)

        self.varQuadriculate = IntVar()
        self.varGrayscale = IntVar()
        self.varCrop = IntVar()
        self.varNegative = IntVar()
        self.varGreening = IntVar()
        self.varReddening = IntVar()
        self.varBluening = IntVar()
        self.varRotate90 = IntVar()
        self.varRotate180 = IntVar()
        self.varRotate270 = IntVar()

        # Checkbuttons
        self.quadriculateCheckbutton = Checkbutton(self.caixaEfeitos, background=CARROT_COLOR,
            variable=self.varQuadriculate).grid(row=2, column=1, sticky=W)
        self.grayscaleCheckbutton = Checkbutton(self.caixaEfeitos, background=CARROT_COLOR,
            variable=self.varGrayscale).grid(row=3, column=1, sticky=W)
        self.cropCheckbutton = Checkbutton(self.caixaEfeitos, background=CARROT_COLOR,
            variable=self.varCrop).grid(row=4, column=1, sticky=W)
        self.negativeCheckbutton = Checkbutton(self.caixaEfeitos, background=CARROT_COLOR,
            variable=self.varNegative).grid(row=5, column=1, sticky=W)
        self.greeningCheckbutton = Checkbutton(self.caixaEfeitos, background=CARROT_COLOR,
            variable=self.varGreening).grid(row=6, column=1, sticky=W)
        self.reddeningCheckbutton = Checkbutton(self.caixaEfeitos, background=CARROT_COLOR,
            variable=self.varReddening).grid(row=7, column=1, sticky=W)
        self.blueningCheckbutton = Checkbutton(self.caixaEfeitos, background=CARROT_COLOR,
            variable=self.varBluening).grid(row=8, column=1, sticky=W)
        self.rotate90Checkbutton = Checkbutton(self.caixaEfeitos, background=CARROT_COLOR,
            variable=self.varRotate90).grid(row=9, column=1, sticky=W)
        self.rotate180Checkbutton = Checkbutton(self.caixaEfeitos, background=CARROT_COLOR,
            variable=self.varRotate180).grid(row=10, column=1, sticky=W)
        self.rotate270Checkbutton = Checkbutton(self.caixaEfeitos, background=CARROT_COLOR,
            variable=self.varRotate270).grid(row=11, column=1, sticky=W)

        # Botão de OK
        self.btn = Button(self.top, text='OK', background=POMEGRANATE_COLOR,
            foreground=CLOUDS_COLOR,command=self.ok)
        self.btn.grid(row=12, column=0, padx=7, pady=7)
        
    def ok(self):
        # Atualizando os parâmetros para comunicação com o servidor
        # URL da imagem enviada
        global urlImg

        # Parâmetros de redimensionamento
        global width
        global height

        # Efeitos
        global quadriculate
        global grayscale
        global crop
        global negative
        global greening
        global reddening
        global bluening
        global rotate90
        global rotate180
        global rotate270

        # Armazenado a entrada de dados do redimensionamento
        width = self.entradaWidth.get()
        height = self.entradaHeight.get()

        # Variável para armazenar os efeitos escolhidos
        effects = ''

        if self.varQuadriculate.get() == 1:
            effects += quadriculate + ','
        if self.varGrayscale.get() == 1:
            effects += grayscale + ','
        if self.varCrop.get() == 1:
            effects += crop + ','
        if self.varNegative.get() == 1:
            effects += negative + ','
        if self.varGreening.get() == 1:
            effects += greening + ','
        if self.varReddening.get() == 1:
            effects += reddening + ','
        if self.varBluening.get() == 1:
            effects += bluening + ','
        if self.varRotate90.get() == 1:
            effects += rotate90 + ','
        if self.varRotate180.get() == 1:
            effects += rotate180 + ','
        if self.varRotate270.get() == 1:
            effects += rotate270

        # Parâmetros que serão enviados ao servidor
        parametros = {'file': urlImg, 'effects': effects}

        # Verificando se os dados de redimensionamento foram inseridos
        if len(width):
            parametros['width'] = width
        if len(height):
            parametros['height'] = height

        # Enviar requisição POST ou GET para /apply_effects
        # O atributo 'file' contém o nome do arquivo a ser modificado
        # Opcionais width e height
        # Effects (separados por ',')
        urlServer = 'http://' + ip + ':' + porta + '/apply_effects'
        r = requests.get(urlServer, params=parametros)
        
        # Obtendo a url para realizar o download da imagem alterada
        urlDownload = r.content
        
        # Obtendo a imagem alterada
        urlServer = 'http://' + ip + ':' + porta + '/' + urlDownload
        
        # Salva e exibe a imagem retornada pelo servidor
        a = open('%s' % urlDownload.split('/')[-1], 'wb')
        a.write(urllib2.urlopen(urlServer).read())
        a.close()
        Image.open('%s' % urlDownload.split('/')[-1]).show()
        ####################################################

        # Destruindo a caixa de dialogo
        self.top.destroy()



        
if __name__ == '__main__':
    try:
        # Janela principal
        root = mainWindow()

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
        #raise
        pass
