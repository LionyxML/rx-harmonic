#!/usr/bin/python3
# Arquivo : rccalcX.py
# Programa: Calculadora de operações básicas em números
#           complexos para X
# Autor   : Rahul Martim Juliato
# Versão  : 0.1  -  10.04.2018



#---===[0. Bibliotecas]===---
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk
import cmath
import math
#---===[0. Fim das Bibliotecas]===---



#---===[1. Funções]===---
def quit():
    """ Sai do programa destruindo o necessário
    """
    global janela
    janela.destroy()


def sobre():
    """ Mostra as informações do programa
    """
    mb.showinfo("r[CCALC]X",'''

r[CCALC]X
Calculadora de Números Complexos

Versão: 0.1

Autor: Rahul Martim Juliato
(rahul.juliato@gmail.com)

''')
    
    
# Snipet para conversão em números de engenharia
from math import floor, log10

def powerise10(x):
    """ Returns x as a*10**b with 0 <= a < 10
    """
    if x == 0: return 0,0
    Neg = x < 0
    if Neg: x = -x
    a = 1.0 * x / 10**(floor(log10(x)))
    b = int(floor(log10(x)))
    if Neg: a = -a
    return a,b

def eng(x):
    """Return a string representing x in an engineer friendly notation"""
    a,b = powerise10(x)
    if -3 < b < 3: return "%.4g" % x
    a = a * 10**(b % 3)
    b = b - b % 3
    return "%.4gE%s" % (a,b)
## Fim do Snipet

def converte():
    """ converte retangular em polar
    """
    real = ent_real.get()
    imag = ent_imag.get()

    retan = float(real) + (1j) * float(imag)
    polar = cmath.polar(retan)

    polar = [eng(polar[0]),eng(math.degrees(polar[1]))]
    
    lab_resposta.delete(0,100)
    lab_resposta.insert(0,str(retan).strip("()"))

    ent_polar.delete(0,100)
    ent_polar.insert(0,str(polar).strip('[]').replace(",",u'\u2220').replace("E+00", "").replace("\'", "")+'°')


def converte2():
    """ converte polar em retangular
    """
    modu = ent_modu.get()
    faso = ent_faso.get()

    polar = str(eng(float(modu)) + u'\u2220' + eng(float(faso))+'°')
    retan = cmath.rect(float(modu), math.radians(float(faso)))

    if retan.imag >= 0:
        sinal = '+'
    else:
        sinal = ''
    
    retan = [eng(retan.real), eng(retan.imag)]
        
    ent_polo.delete(0,100)
    ent_polo.insert(0,str(polar))
        
    ent_reto.delete(0,100)
    ent_reto.insert(0,str(retan).strip('[]').replace(',', " " + sinal).replace("\'", "")+'j')


# Altera as labels para a representação correspondente
# Prefiro chamar uma função só com argumento, mas aparentemente não
# é possível no radio button utilizar command = escolhe(1), somente
# command = escolhe

def escolhe1():

    opcao = opnum1.get()
    
    if opcao == 1:
        lab_opnum1meio.config(text = "+")
        lab_opnum1fim.config(text = "j")
        
    else:
        opteste = "+"
        lab_opnum1meio.config(text=u'\u2220')
        lab_opnum1fim.config(text = "°")


def escolhe2():

    opcao = opnum2.get()
    
    if opcao == 1:
        lab_opnum2meio.config(text = "+")
        lab_opnum2fim.config(text = "j")
        
    else:
        opteste = "+"
        lab_opnum2meio.config(text=u'\u2220')
        lab_opnum2fim.config(text = "°")


def normaliza(parte_a,parte_b,formato):
    """Normaliza os números para o padrão complexo interno
    normaliza(parte a, parte b, formato)
    a e b são floats, formato é 1 ou 2 (ret, polar)
    """
    if formato == 1:
        return float(parte_a) + 1j * float(parte_b)
    else:
        return cmath.rect(float(parte_a), math.radians(float(parte_b)))


def formata_complexo(num, formato='r'):
    """Formata um número tipo complex() para ser usado como string,
       retornando em retangular ou polar
    """


    if formato == 'r':
        num = [eng(num.real), eng(num.imag)]  # num convertido em lista
        
        if float(num[1]) >= 0:
            sinal = '+'
        else:
            sinal = ''
            
        return str(num).strip('[]').replace(',', " " + sinal).replace("\'", "")+'j'
    
    elif formato == 'p':
        polar = cmath.polar(num)
        
        polar = [eng(polar[0]),eng(math.degrees(polar[1]))]
        
        return str(polar).strip('[]').replace(",",u'\u2220').replace("E+00", "").replace("\'", "")+'°'

    
        

def operacoes():

    num1 = normaliza(ent_opnum1a.get(), ent_opnum1b.get(), opnum1.get())
    ent_num1a.delete(0,100)
    ent_num1a.insert(0,formata_complexo(num1))
    ent_num1b.delete(0,100)
    ent_num1b.insert(0,formata_complexo(num1, formato='p'))
    
    num2 = normaliza(ent_opnum2a.get(), ent_opnum2b.get(), opnum2.get())
    ent_num2a.delete(0,100)
    ent_num2a.insert(0,formata_complexo(num2))
    ent_num2b.delete(0,100)
    ent_num2b.insert(0,formata_complexo(num2, formato='p'))
    
    ent_somaa.delete(0,100)
    ent_somaa.insert(0,formata_complexo(num1+num2))
    ent_subta.delete(0,100)
    ent_subta.insert(0,formata_complexo(num1-num2))
    ent_multa.delete(0,100)
    ent_multa.insert(0,formata_complexo(num1*num2))
    ent_divia.delete(0,100)
    ent_divia.insert(0,formata_complexo(num1/num2))

    ent_somab.delete(0,100)
    ent_somab.insert(0,formata_complexo(num1+num2, formato='p'))
    ent_subtb.delete(0,100)
    ent_subtb.insert(0,formata_complexo(num1-num2, formato='p'))
    ent_multb.delete(0,100)
    ent_multb.insert(0,formata_complexo(num1*num2, formato='p'))
    ent_divib.delete(0,100)
    ent_divib.insert(0,formata_complexo(num1/num2, formato='p'))
    

#---===[1. Fim das Funções]===---




#---===[2. Início da geração da Janela]===---

# 2.0. Definições principais da janela
janela = tk.Tk()
janela.geometry('580x350')
janela.wm_title('r[CCALC]X v0.1')
#janela.tk_setPalette('gray')


# 2.0. Barra de menu
barramenu = tk.Menu(janela)
arquivo = tk.Menu(barramenu, tearoff=0)
arquivo.add_command(label="Sobre", command=sobre)
arquivo.add_separator()
arquivo.add_command(label="Sair", command=quit)
barramenu.add_cascade(label="Arquivo", menu=arquivo)
janela.config(menu=barramenu)

# 2.0 Título dentro da janela principal
titulo = tk.Label(janela, text="r[Calculadora Complexa]X", font="Arial 16 bold", height=2)
titulo.grid(column = 0, row = 0, sticky="NSEW")

# 2.1 Definições do notebook e ABAS
notebook = ttk.Notebook(janela, height=260, width=575)
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text = 'Retangular -> Polar', sticky = 'S')
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text = 'Polar -> Retangular', sticky = 'S')
frame3 = ttk.Frame(notebook)
notebook.add(frame3, text = 'Operações', sticky = 'S')
notebook.grid(column = 0, row = 1)



# 2.1 Início do Frame 1 - RETANGULAR -> POLAR
lab_real = tk.Label(frame1, text="Real:")
lab_real.grid(column = 0, row = 1, sticky='E')

ent_real = tk.Entry(frame1)
ent_real.configure(width = 30)
ent_real.grid(column = 1, row = 1)

lab_imag = tk.Label(frame1, text="Imaginário:")
lab_imag.grid(column = 0, row = 2, sticky='E')

ent_imag = tk.Entry(frame1)
ent_imag.configure(width = 30)
ent_imag.grid(column = 1, row = 2, sticky='W')

ttk.Separator(frame1).grid(column = 0, row = 3, pady = 10)

lab_complexo = tk.Label(frame1, text="Retangular =")
lab_complexo.grid(column = 0, row = 4, sticky='E')

lab_resposta = tk.Entry(frame1)
lab_resposta.configure(width = 30)
lab_resposta.grid(column = 1, row = 4, sticky='W')

lab_polar = tk.Label(frame1, text="Polar =")
lab_polar.grid(column = 0, row = 5, sticky='E')

ent_polar = tk.Entry(frame1)
ent_polar.configure(width = 30)
ent_polar.grid(column = 1, row = 5, sticky='W')

bot_converte = tk.Button(frame1, text="Converter", command=converte)
bot_converte.grid(column = 1, pady='5', sticky='S')

ttk.Separator(frame1).grid(column = 0, pady = 28)


# 2.1 Fim do Frame 1 - RETANGULAR -> POLAR


# 2.2 Início do Frame 2 - POLAR -> RETANGULAR
lab_modu = tk.Label(frame2, text="Módulo:")
lab_modu.grid(column = 0, row = 0, sticky='E')

ent_modu = tk.Entry(frame2)
ent_modu.configure(width = 30)
ent_modu.grid(column = 1, row = 0)

lab_faso = tk.Label(frame2, text="Fasor:")
lab_faso.grid(column = 0, row = 1, sticky='E')

ent_faso = tk.Entry(frame2)
ent_faso.configure(width = 30)
ent_faso.grid(column = 1, row = 1)

ttk.Separator(frame2).grid(column = 0, row = 2, pady = 10)

lab_polo = tk.Label(frame2, text="Polar =")
lab_polo.grid(column = 0, row = 3, sticky='E')

ent_polo = tk.Entry(frame2)
ent_polo.configure(width = 30)
ent_polo.grid(column = 1, row = 3)

lab_reto = tk.Label(frame2, text="Retangular =")
lab_reto.grid(column = 0, row = 4, sticky='E')

ent_reto = tk.Entry(frame2)
ent_reto.configure(width = 30)
ent_reto.grid(column = 1, row = 4)


bot_convo = tk.Button(frame2, text="Converter", command=converte2)
bot_convo.grid(column = 1, pady='5', sticky='S')

ttk.Separator(frame2).grid(column = 0, pady = 28)
# 2.2 Fim do Frame 2 - POLAR -> RETANGULAR


# 2.3 Início do Frame 3 - OPERAÇÕES



        
opnum1 = tk.IntVar()
opnum2 = tk.IntVar()

opnum1.set(1)
opnum2.set(1)

lab_opnum1 = tk.Label(frame3, text="Num1: ")
lab_opnum1.grid(column = 0, row = 0, sticky = 'E', padx=4)

ent_opnum1a = tk.Entry(frame3)
ent_opnum1a.configure(width = 20)
ent_opnum1a.grid(column = 1, row = 0, padx = 4)

lab_opnum1meio = tk.Label(frame3, text="+")
lab_opnum1meio.grid(column = 2, row = 0)

ent_opnum1b = tk.Entry(frame3)
ent_opnum1b.configure(width = 20)
ent_opnum1b.grid(column = 3, row = 0, padx = 4)

lab_opnum1fim = tk.Label(frame3, text="j")
lab_opnum1fim.grid(column = 4, row = 0)

rad_opnum1 = tk.Radiobutton(frame3, text = 'R', variable = opnum1, value = 1, command = escolhe1)
rad_opnum1.grid(column = 5, row = 0, padx = 4)

rad_opnum1 = tk.Radiobutton(frame3, text = 'P', variable = opnum1, value = 2, command = escolhe1)
rad_opnum1.grid(column = 6, row = 0, padx = 4)


lab_opnum2 = tk.Label(frame3, text="Num2: ")
lab_opnum2.grid(column = 0, row = 1, sticky = 'E', padx=4)

ent_opnum2a = tk.Entry(frame3)
ent_opnum2a.configure(width = 20)
ent_opnum2a.grid(column = 1, row = 1, padx = 4)

lab_opnum2meio = tk.Label(frame3, text="+")
lab_opnum2meio.grid(column = 2, row = 1)

ent_opnum2b = tk.Entry(frame3)
ent_opnum2b.configure(width = 20)
ent_opnum2b.grid(column = 3, row = 1, padx = 4)

lab_opnum2fim = tk.Label(frame3, text="j")
lab_opnum2fim.grid(column = 4, row = 1)

rad_opnum2 = tk.Radiobutton(frame3, text = 'R', variable = opnum2, value = 1, command = escolhe2)
rad_opnum2.grid(column = 5, row = 1, padx = 4)

rad_opnum2 = tk.Radiobutton(frame3, text = 'P', variable = opnum2, value = 2, command = escolhe2)
rad_opnum2.grid(column = 6, row = 1, padx = 4)


ttk.Separator(frame3).grid(column = 0, row = 2, pady = 5)

lab_num1a = tk.Label(frame3, text = "num1 =")
lab_num1a.grid(column = 0, row = 3, sticky = 'E' )

ent_num1a = tk.Entry(frame3)
ent_num1a.configure(width = 20)
ent_num1a.grid(column = 1, row = 3, padx = 4)

lab_num1ou = tk.Label(frame3, text = "ou")
lab_num1ou.grid(column = 2, row = 3)

ent_num1b = tk.Entry(frame3)
ent_num1b.configure(width = 20)
ent_num1b.grid(column = 3, row = 3, padx = 4)

lab_num2a = tk.Label(frame3, text = "num2 =")
lab_num2a.grid(column = 0, row = 4, sticky = 'E' )

ent_num2a = tk.Entry(frame3)
ent_num2a.configure(width = 20)
ent_num2a.grid(column = 1, row = 4, padx = 4)

lab_num2ou = tk.Label(frame3, text = "ou")
lab_num2ou.grid(column = 2, row = 4)

ent_num2b = tk.Entry(frame3)
ent_num2b.configure(width = 20)
ent_num2b.grid(column = 3, row = 4, padx = 4)


#ttk.Separator(frame3).grid(column = 0, row = 5, pady = 5)

lab_soma = tk.Label(frame3, text = "num+num2 =")
lab_soma.grid(column = 0, row = 6, sticky = 'E' )

ent_somaa = tk.Entry(frame3)
ent_somaa.configure(width = 20)
ent_somaa.grid(column = 1, row = 6, padx = 4)

lab_somaou = tk.Label(frame3, text = "ou")
lab_somaou.grid(column = 2, row = 6)

ent_somab = tk.Entry(frame3)
ent_somab.configure(width = 20)
ent_somab.grid(column = 3, row = 6, padx = 4)

lab_subt = tk.Label(frame3, text = "num1-num2 =")
lab_subt.grid(column = 0, row = 7, sticky = 'E' )

ent_subta = tk.Entry(frame3)
ent_subta.configure(width = 20)
ent_subta.grid(column = 1, row = 7, padx = 4)

lab_subtou = tk.Label(frame3, text = "ou")
lab_subtou.grid(column = 2, row = 7)

ent_subtb = tk.Entry(frame3)
ent_subtb.configure(width = 20)
ent_subtb.grid(column = 3, row = 7, padx = 4)

lab_mult = tk.Label(frame3, text = "num1*num2 =")
lab_mult.grid(column = 0, row = 8, sticky = 'E' )

ent_multa = tk.Entry(frame3)
ent_multa.configure(width = 20)
ent_multa.grid(column = 1, row = 8, padx = 4)

lab_multou = tk.Label(frame3, text = "ou")
lab_multou.grid(column = 2, row = 8)

ent_multb = tk.Entry(frame3)
ent_multb.configure(width = 20)
ent_multb.grid(column = 3, row = 8, padx = 4)

lab_divi = tk.Label(frame3, text = "num1/num2 =")
lab_divi.grid(column = 0, row = 9, sticky = 'E' )

ent_divia = tk.Entry(frame3)
ent_divia.configure(width = 20)
ent_divia.grid(column = 1, row = 9, padx = 4)

lab_diviou = tk.Label(frame3, text = "ou")
lab_diviou.grid(column = 2, row = 9)

ent_divib = tk.Entry(frame3)
ent_divib.configure(width = 20)
ent_divib.grid(column = 3, row = 9, padx = 4)

bot_opera = tk.Button(frame3, text="Calcular", command=operacoes)
bot_opera.grid(column = 3, row = 10, sticky = 'S', pady = 10)
# 2.3 Fim do Frame 2 - OPERAÇÕES

tk.mainloop()

#---===[2 Fim da Geração da Janela]===---
