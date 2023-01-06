############################################################################################################
# IMPLEMENTACAO DE METODOS GRAFICOS PARA ANALISE DE SINAIS #
# 
# Periodo:      2022/02
# Aluno:        João Victor do Rozário Recla.
# Professor:    Daniel Jose Custodio Coura.
# Disciplina:   Processamento Digital de Sinais.
# 
# UNIVERSIDADE FEDERAL DO ESPÍRITO SANTO       - UFES
# CENTRO UNIVERSITÁRIO NORTE DO ESPÍRITO SANTO - CEUNES
############################################################################################################

# 
# Imports.
import numpy as Np
from   numpy.fft import fft      as FFT
from   numpy.fft import fftfreq  as FFTFREQ
from   numpy.fft import fftshift as FFTSHIFT
import matplotlib.pyplot as Graph

# Macros.
PI = Np.pi
############################################################################################################


# 
# 
def Aplicar_DFFT_(Sinal, Periodo = 1):
    """
    Metodo para aplicar a DTTF em um sinal e obter
    a sua representacao na frequencia sob a forma
    do espectro de amplitude e do espectro de fase.

    Entrada:
        - Vetor de pontos do sinal.
        - Periodo, ou taxa de amostragem, do sinal.

    Saida:
        - Espectro de amplitude do sinal.
        - Espectro de fase do sinal.
        - Frequencia de amostragem do sinal.
    """
    
    Sinal_Freq = Periodo * FFT(Sinal)                       # DTTF do sinal.
    Sinal_Freq = FFTSHIFT(Sinal_Freq)                       # Ajuste do sinal na frequencia para a origem.
    
    Sinal_Mod  = Np.abs(Sinal_Freq)                         # Modulo do sinal (Amplitude / Magnitude).
    Sinal_Fase = Np.angle(Sinal_Freq)                       # Fase do sinal na frequencia.
    
    Rotacao = (2 * PI)                                      # Periodo rotacional.
    w = FFTFREQ(len(Sinal_Freq), d = Periodo) * Rotacao     # Frequencia angular do sinal {(2 * PI * Freq)[Rad/s]}.
    w = FFTSHIFT(w / Rotacao)                               # Frequencia angular do sinal {(Freq)[Hz]}.

    return (Sinal_Mod, Sinal_Fase, w)
############################################################################################################


# 
# 
def Plotar_Grafico_(X, Y, Lim_inf_x = 0, Lim_sup_x = 100, Titulo = "Titulo", Rotulo_x = "Eixo X", Rotulo_y = "Eixo Y", Legenda = " "):
    """
    Metodo para plotar a representacao
    grafica de um conjunto de dados.

    Entrada:
        - Vetor de pontos para o eixo X.
        - Vetor de pontos para o eixo Y.
        - Limite inferior para a representacao do eixo X.
        - Limite superior para a representacao do eixo X.
        - Titulo do grafico.
        - Rotulo do eixo X.
        - Rotulo do eixo Y.
        - Legenda para a figura.

    Saida:
        - Void.
    """

    # Representacao Grafica dos dados.
    Graph.plot(X, Y)
    Graph.title(Titulo,     fontsize = 12)
    Graph.xlabel(Rotulo_x,  fontsize = 9)
    Graph.ylabel(Rotulo_y,  fontsize = 9)
    Graph.xlim(Lim_inf_x, Lim_sup_x)                    # Intervalo limite do eixo X.
    Graph.grid()
    Graph.suptitle(Legenda, y = 0.96, fontsize = 15)    # Legenda da figura.
    Graph.show()
############################################################################################################


# 
# 
def Plotar_Analise_Sinal_(Sinal, Tempo, Ts, Legenda = " "):
    """
    Metodo para plotar a representacao grafica de
    um sinal no tempo e na frequencia (espectro de
    amplitude e espectro de fase).

    Entrada:
        - Vetor de pontos do sinal.
        - Vetor de pontos do sinal no tempo.
        - Periodo, ou taxa de amostragem, do sinal.
        - Legenda da figura.

    Saida:
        - Void.
    """

    # Titulo e rotulo dos graficos.
    Titulos   = ["X(t) - Sinal no Tempo", "|X(jw)| - Espectro de Amplitude", "Angle(X(jw)) - Espectro de Fase"]
    Rotulos_x = ["Tempo [s]", "Frequência [Hz]"]
    Rotulos_y = "Amplitude"

    Duracao = len(Sinal) * Ts
    Sinal_Mod, Sinal_Fase, Frequencia = Aplicar_DFFT_(Sinal, Ts)    # Aplicacao da DTFT no sinal.


    # Plotagem individual de cada grafico (Relatorio).
    # Plotar_Grafico_(Tempo,           Sinal,   0, Duracao, Titulos[0], Rotulos_x[0], Rotulos_y, Legenda)
    # Plotar_Grafico_(Frequencia,  Sinal_Mod,   0,    3400, Titulos[1], Rotulos_x[1], Rotulos_y, Legenda)
    # Plotar_Grafico_(Frequencia, Sinal_Fase, -15,      15, Titulos[2], Rotulos_x[1], Rotulos_y, Legenda)


    # Plotagem unica dos graficos.
    Fig, Plots = Graph.subplots(3, 1)

    # Sinal no tempo.
    Plots[0].plot(Tempo, Sinal)
    Plots[0].set_title(Titulos[0],      fontsize = 12)
    Plots[0].set_xlabel(Rotulos_x[0],   fontsize = 9)
    Plots[0].set_ylabel(Rotulos_y,      fontsize = 9)
    Plots[0].set_xlim(0, Duracao)
    Plots[0].grid()

    # Espectro de amplitude.
    Plots[1].plot(Frequencia, Sinal_Mod)
    Plots[1].set_title(Titulos[1],      fontsize = 12)
    Plots[1].set_xlabel(Rotulos_x[1],   fontsize = 9)
    Plots[1].set_ylabel(Rotulos_y,      fontsize = 9)
    Plots[1].set_xlim(0, 3400)                              # 0 <= Freq [Hz] <= 3400.
    Plots[1].grid()

    # Espectro de fase.
    Plots[2].plot(Frequencia, Sinal_Fase)
    Plots[2].set_title(Titulos[2],      fontsize = 12)
    Plots[2].set_xlabel(Rotulos_x[1],   fontsize = 9)
    Plots[2].set_ylabel(Rotulos_y,      fontsize = 9)
    Plots[2].set_xlim(-15, 15)
    Plots[2].grid()

    Graph.suptitle(Legenda, fontsize = 15)                  # Legenda da figura.
    Graph.tight_layout()
    Graph.show()
############################################################################################################


# 
# 
def Plotar_Comparacao_Sinais_(Sinal_01, Sinal_02, Tempo):
    """
    Metodo para plotar a representacao grafica
    de dois sinais em uma mesma linha de tempo.

    Entrada:
        - Vetor de pontos do sinal 01.
        - Vetor de pontos do sinal 02.
        - Vetor de pontos no tempo para ambos os sinais.
    
    Saida:
        - Void.
    """
    
    # Representacao Grafica dos dados.
    Graph.plot(Tempo, Sinal_02, 'r', label = "Sinal Reverberado.")
    Graph.plot(Tempo, Sinal_01, 'b', label = "Sinal de Entrada.")
    Graph.legend()
    Graph.title("Comparação dos Sinais",    fontsize = 12)
    Graph.xlabel("Tempo [s]",               fontsize = 9)
    Graph.ylabel("Amplitude",               fontsize = 9)
    Graph.grid()
    Graph.show()
############################################################################################################