############################################################################################################
# Processamento Digital de Sinais
# Atividade 05: Amostragem de Sinais Continuos.
# Aluno:        João Victor do Rozário Recla.
#
# UNIVERSIDADE FEDERAL DO ESPÍRITO SANTO       (UFES)
# CENTRO UNIVERSITÁRIO NORTE DO ESPÍRITO SANTO (CEUNES)
############################################################################################################


# Imports.
import numpy as Np
from time import sleep
from numpy.fft import fft as FFT
from numpy.fft import fftshift as FFTSHIFT
from numpy.fft import fftfreq as FFTFREQ
import matplotlib.pyplot as Graph
import sounddevice as Gravador
from scipy.io.wavfile import write as Sound_write
############################################################################################################


# Frequencias de amostragem [Hz].
Freq_amost = [1000, 8000, 44100]


# Gravacao dos audios.
Duracao    = 5              # Tempo de gravacao (s).
Recordings = []             # Vetor de audios gravados.

# Loop para gravar os audios.
for i in range(len(Freq_amost)):
    Record = Gravador.rec(int(Duracao * Freq_amost[i]), samplerate = Freq_amost[i], channels = 1)
    Recordings.append(Record)

    print('\nGravando...')
    Gravador.wait()

    print('Salvando gravação ......')
    Sound_write(f"Gravacao_0{i+1}.wav", Freq_amost[i], Recordings[i])
    sleep(3)    # Pausa o tempo por 3s.
############################################################################################################





# Loop para plotar os graficos de cada sinal de audio.
for i in range(len(Freq_amost)):

    Ts      = (1 / Freq_amost[i])           # Taxa de amostragem do sinal.
    Duracao = (len(Recordings[i]) * Ts)     # Tempo de duracao do audio (s).


    # Calculando a FFT do sinal.
    Record_freq = Ts * FFT(Recordings[i])
    Record_freq = FFTSHIFT(Record_freq)     # Ajuste do sinal na frequencia para a origem.
    Record_Mod  = Np.abs(Record_freq)       # Modulo do sinal na frequencia.

    Rotacao = (2 * Np.pi)                               # Periodo rotacional.
    w = FFTFREQ(len(Recordings[i]), d = Ts) * Rotacao   # Frequencia angular do sinal {(2 * PI * Freq)[Rad/s]}.
    w = FFTSHIFT(w / Rotacao)                           # Frequencia angular do sinal {(Freq)[Hz]}.


    # Plotando os graficos. 
    Tempo = Np.arange(0, Duracao, Ts)
    Fig, Plots = Graph.subplots(2, 1)
    
    # Sinal no tempo.
    Plots[0].plot(Tempo, Recordings[i], 'r-')
    Plots[0].set_ylabel("Amplitude")
    Plots[0].set_xlabel("Tempo [s]")
    Plots[0].set_xlim(0, Duracao)
    Plots[0].grid(True)

    # Espectro de amplitude do sinal.
    Plots[1].plot(w, Record_Mod)
    Plots[1].set_ylabel("Amplitude")
    Plots[1].set_xlabel("Frequencia [Hz]")
    # Plots[1].set_xlim(0, 3400)
    Plots[1].grid(True)

    Graph.suptitle(f'Gravação 0{i+1}', y = 0.96, fontsize = 15)    # Legenda da figura.
    Graph.show()
############################################################################################################





# Resposta das perguntas.
def Respostas_():
    print("\n\nRespostas para as questoes da atividade:\n")

    # Questao A.
    print("\n A) - Qual arquivo tem a melhor qualidade de áudio ?")
    print("\t O arquivo da Gravação 03 (Com taxa de amostragem de 44,1 [KHz]).")

    # Questao B.
    print("\n B) - Qual o arquivo que perde menos informação ?")
    print("\t O arquivo da Gravação 03 (Com taxa de amostragem de 44,1 [KHz]).")

    # Questao C.
    print("\n C) - Qual o arquivo que consegue entregar a informação com o menor custo (menor tamanho) ?")
    print("\t O arquivo da Gravação 02 (Com taxa de amostragem de 8 [KHz]).")

    # Questao D.
    print("\n D) - Qual o arquivo que tem o melhor custo beneficio (qualidade e tamanho) ?")
    print("\t O arquivo da Gravação 02 (Com taxa de amostragem de 8 [KHz]).\n")

Respostas_()
############################################################################################################