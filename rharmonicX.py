#!/usr/bin/python3
# Arquivo : rharmonicX.py
# Programa: Programa para visualização e compreensão de sinais harmônicos
# Autor   : Rahul Martim Juliato
# Versão  : 0.1  -  05.11.2018


#---===[0. Bibliotecas]===---
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk
import math
from time import sleep
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
    mb.showinfo("r[HARMONIC]X",'''

    r[HARMONIC]X

Programa para compreensão de sinais harmônicos.

Versão: 0.1

Autor: Rahul Martim Juliato
(rahul.juliato@gmail.com)

''')

    
def erro(mensagem):
    """ Sobe uma messagebox de erro com a mensagem
    passada"""
    mb.showerror("Erro!", mensagem)
 
    
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

def calcula():

    numerador = 0
    denominador = 1
    
    leitura_amplitudes=[ ent_harmonicas[str('h %s' % x)].get() * int(checkbox[x].get()) for x in range(15)]

    for x in range (15):
        try:
            numerador += int(leitura_amplitudes[x+1])**2
        except:
            pass

    numerador = math.sqrt(numerador)


    
    try:
        thdf = (numerador / float(leitura_amplitudes[0]))*100
        thdf = str("%3.2f" % float(thdf))
        
    except:
        thdf = "Falta h1!"
        
    ent_thdf.delete(0, tk.END)
    ent_thdf.insert(0, thdf)

    

    for x in range (15):
        try:
            denominador += int(leitura_amplitudes[x])**2
        except:
            pass

    denominador = math.sqrt(denominador)

    try:
        thdr = (numerador / denominador)*100
        thdr = str("%3.2f" % float(thdr))
        
    except:
        thdr = ""


    ent_thdr.delete(0, tk.END)
    ent_thdr.insert(0, thdr)


def reset():

    global z
    global leitura_amplitudes

    for x in range(15):
        ent_harmonicas[str('h %s' % x)].delete(0, tk.END)
        chk_harmonicas[str('h %s' % (str(x)))].deselect()
        
    ent_thdr.delete(0, tk.END)
    ent_thdf.delete(0, tk.END)

    z.delete("all")
    y.delete("all")
    w.delete("all")
        

def grafico_soma():

    global w, y, z
    global xy

    primo = inicio_row + 1
    separacao = 5

    lab_graf_w = tk.Label(janela, text='Sinal Resultante')
    lab_graf_w.grid(sticky='WE', row = primo -1 , column = i + 4)
    
    w = tk.Canvas(janela, width = 300, height = 100, bg='white')
    w.grid(sticky='', row = primo, column = i + 4, rowspan = separacao)

    lab_graf_y = tk.Label(janela, text='Decomposição Harmônica')
    lab_graf_y.grid(sticky='WE', row = primo + separacao + 1 , column = i + 4)

    alt_y = 100
    lar_y = 300
    
    y = tk.Canvas(janela, width = lar_y, height = alt_y, bg='white')
    y.grid(sticky='', row = primo + separacao + 2, column = i + 4, rowspan = separacao)

    lab_graf_z = tk.Label(janela, text='Espectro Harmônico')
    lab_graf_z.grid(sticky='WE', row = primo + separacao + separacao + 3, column = i + 4)

    alt_z = 100
    lar_z = 300
    
    z = tk.Canvas(janela, width = lar_z, height = alt_z, bg='white')
    z.grid(sticky='', row = primo + separacao + separacao + 4, column = i + 4, rowspan = 17)



    
    # Precisa de otimização, houve uma dissecção do código para encontrar bugs com números grandes

    # Lê as entradas, formata espaço e plota o gráfico de barras do Espectro Harmônico
    
    leitura_amplitudes = [ ent_harmonicas[str('h %s' % x)].get() * int(checkbox[x].get()) for x in range(15) ]

    normaliza_barras = [ 0 for x in range(15) ]

    for x in range(15):
        try:
            normaliza_barras[x] = float(leitura_amplitudes[x])
        except:
            normaliza_barras[x] = 0

    maior = 0
    
    try:
        maior = float(max(normaliza_barras))
    except:
        pass

    
    for x in range(15):
        try:
            normaliza_barras[x] = normaliza_barras[x] / maior * alt_z * 0.95
        except:
            normaliza_barras[x] = 0
        
#    print(leitura_amplitudes)
#    print(normaliza_barras)
#    print(maior)


    xdif = 0
    xlarg = int(lar_z / 15)
    for x in range(15):
        z.create_rectangle(xdif, alt_z, xdif+xlarg, int(alt_z-int(normaliza_barras[x])), fill='blue', width=1)

#        print(xdif, alt_z, xlarg, int(alt_z-int(normaliza_barras[x])))
        xdif += xlarg

        
    xy = [ [] for x in range(15) ]
    totalx = [ [] for x in range(15) ]
    totaly = [ [] for x in range(15) ]
    tt = [ 0 for x in range(1800)]
    uiax = [ 0 for x in range(1800)]
    uiay = [ 0 for x in range(1800)]
    
    x_incremento = lar_y / 1800
    amplitude = alt_y
    center = alt_y / 2

    
    for j in range(15):
        for x in range(1800):

            xizio = x * float(x_incremento) 
            yizio = int(math.sin(3*math.radians(xizio * (j+1))) * (-1) * normaliza_barras[j])

            totalx[j].append(xizio)
            totaly[j].append(yizio)
            
            yizio = int(yizio)/2 + center

            xy[j].append(xizio)
            xy[j].append(yizio)

        ylinha = y.create_line(xy[j], fill='blue')


    # média de todos os x
    # soma de todos os y

    for x in range(1800):
        uiax[x] = x * float(x_incremento)
                
    
    for x in range(1800):
        for j in range(15):
            uiay[x] += totaly[j][x]


    # inserir função de normalizar a o y
    try:
        maior = float(max(uiay))
    except:
        pass
    
    for x in range(1800):
        try:
            uiay[x] = uiay[x] / maior * alt_z * 0.95
        except:
            uiay[x] = 0
    
            
    for x in range(1800):
        tt.append(uiax[x])
        tt.append(int(uiay[x]/2 +center))

    wlinha = w.create_line(tt, fill='blue')
    
            

#---===[1. Fim das Funções]===---



#---===[2. Início da geração da Janela]===---
# 2.0. Definições principais da janela
janela = tk.Tk()
janela.wm_title('r[HARMONIC]X v0.1')
janela.wm_minsize(600,500)
janela.grid_anchor(anchor='c')
#janela.tk_setPalette('white')


# 2.0. Barra de menu
barramenu = tk.Menu(janela)
arquivo = tk.Menu(barramenu, tearoff=800)
arquivo.add_command(label="Sobre", command=sobre)
arquivo.add_separator()
arquivo.add_command(label="Sair", command=quit)
barramenu.add_cascade(label="Arquivo", menu=arquivo)

janela.config(menu=barramenu)


# 2.0. Apresentaçã da tela principal


# Base para alinhamento do grid
inicio_row = 2
inicio_col = 1


# Cria as Labels, Entrys e Checkboxes
ii = inicio_row + 1
i  = inicio_col
ent_harmonicas = {}
chk_harmonicas = {}


lab_harm = tk.Label(janela, text='Harmônica')
lab_harm.grid(sticky='E', row = inicio_row, column = inicio_col-1)

lab_ampl = tk.Label(janela, text='Amplitude')
lab_ampl.grid(sticky='', row = inicio_row, column = inicio_col)

lab_uso = tk.Label(janela, text='Usa?')
lab_uso.grid(sticky='W', row = inicio_row, column = inicio_col+2)

checkbox = [ tk.IntVar() for x in range(15) ]

for y in range(15):
    l = tk.Label(janela, text=str('h%s = ' % (1+y)))
    l.grid(sticky='E', row = ii, column = i-1)
    
    e = tk.Entry(janela, width = 10)
    e.grid(sticky='', row = ii, column = i, columnspan = 2)
    ent_harmonicas[str('h %s' % (str(y)))] = e

    checkbox[y] = tk.IntVar()  #pulo do gato! Se criado fora do laço, não funciona
    c = tk.Checkbutton(janela, variable = checkbox[y])
    c.grid(sticky='W', row = ii, column = i + 2)
    chk_harmonicas[str('h %s' % (str(y)))] = c
    
    ii += 1

ii = 17
    
line = tk.ttk.Separator(janela)
line.grid(sticky = 'EW', row = ii + y, column = i - 1, columnspan = 4, pady = 10 )
    
lab_thdf = tk.Label(janela, text='thd(f) = ')
lab_thdf.grid(sticky='E', row = 1 + ii + y, column = i - 1)

ent_thdf = tk.Entry(janela, width = 10)
ent_thdf.grid(sticky = '', row = 1 + ii + y, column = i)

lab_thdf_por = tk.Label(janela, text='%')
lab_thdf_por.grid(sticky='W', row = 1 + ii + y, column = i + 2)

lab_thdr = tk.Label(janela, text='thd(r) = ')
lab_thdr.grid(sticky='E', row = 1 + ii + y + 1, column = i - 1)

ent_thdr = tk.Entry(janela, width = 10)
ent_thdr.grid(sticky = '', row = 1 + ii + y + 1, column = i)

lab_thdr_por = tk.Label(janela, text='%')
lab_thdr_por.grid(sticky='W', row = 1 + ii + y + 1 , column = i + 2)

line = tk.ttk.Separator(janela)
line.grid(sticky = 'EW', row = 1+ ii + y + 2, column = i - 1, columnspan = 6, pady = 10 )

but_reset = tk.Button(janela, text = "Reset", command = reset)
but_reset.grid(sticky = 'WE', row = 1 + ii + y + 3, column = i-1 , columnspan = 1 )

but_calc_thd = tk.Button(janela, text = "THDs", command = calcula)
but_calc_thd.grid(sticky = 'WE', row = 1 + ii + y + 3, column = i, columnspan = 3 )

but_grafico = tk.Button(janela, text = "Gráficos", width = 10, command = grafico_soma)
but_grafico.grid(sticky = 'WE', row = 1 + ii + y + 3, column = i + 3, columnspan = 3)

line = tk.ttk.Separator(janela, orient=tk.VERTICAL)
line.grid(sticky = 'NS', row = inicio_row, column = i + 3, rowspan = 1 + ii + y , padx = 10 )

grafico_soma()


tk.mainloop()
#---===[2 Fim da Geração da Janela]===---
