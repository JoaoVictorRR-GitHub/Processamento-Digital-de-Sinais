############################################################################################################
# IMPLEMENTACAO DA FUNCAO PRINCIPAL #
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
import Metodos_Graficos
from   Sistema_Reverberador import Schroeder_Reverbs_
import soundfile as Sound
############################################################################################################


# 
# Obtencao do sinal de audio.
############################################################################################################
Sinal, Freq = Sound.read("Audios/Audio_01_82bpm.wav")      # Audio 01.
# Sinal, Freq = Sound.read("Audios/Audio_02_88bpm.wav")      # Audio 02 (Processameto mais lento).
# Sinal, Freq = Sound.read("Audios/Audio_03_130bpm.wav")     # Audio 03 (Processamento mais lento).

Amostras = len(Sinal)           # Quantidade de amostras.
Ts       = (1 / Freq)           # Taxa de amostragem do sinal de audio.
Duracao  = (Amostras * Ts)      # Tempo de duracao do audio (segundos).
N = Np.arange(0, Duracao, Ts)   # Vetor de pontos no tempo.


# Informacao do sinal de audio.
print("\n")
print("Canal de áudio:              ", "Mono")
print("Quantidade de amostras:      ", Amostras)
print("Frequencia de amostragem:    ", Freq)
print("Taxa de amostragem:          ", Ts)
print(f"Tempo de áudio (s):           {Duracao:.02f} \n\n")


# 
# Funcoes.
############################################################################################################

# Funcao impulso.
Impulso = Np.zeros(len(N), dtype = int)
Impulso[N==0] = 1

# Funcao degrau.
Degrau = Np.zeros(len(N), dtype = int)
Degrau[N >= 0] = 1


# 
# Respostas ao sistema de reverberacao.
############################################################################################################
Reverb = Schroeder_Reverbs_(Freq)     # Inicializa a classe de reverberacao.

# Sistema de reverberacao (Metodo 01).
print("--->    Resposta ao Impulso:")
Saida_impulso = Reverb.Schroeder___Metodo_01_(Impulso)
print("--->    Resposta ao Degrau:")
Saida_degrau  = Reverb.Schroeder___Metodo_01_(Degrau)
print("--->    Resposta ao Sinal:")
Saida         = Reverb.Schroeder___Metodo_01_(Sinal)

# Sistema de reverberacao (Metodo 02).
# print("--->    Resposta ao Impulso:")
# Saida_impulso = Reverb.Schroeder___Metodo_02_(Impulso)
# print("--->    Resposta ao Degrau:")
# Saida_degrau  = Reverb.Schroeder___Metodo_02_(Degrau)
# print("--->    Resposta ao Sinal:")
# Saida         = Reverb.Schroeder___Metodo_02_(Sinal)



# 
# Analise dos sinais.
############################################################################################################
Metodos_Graficos.Plotar_Analise_Sinal_(Sinal,         N, Ts, "Sinal de Áudio")
Metodos_Graficos.Plotar_Analise_Sinal_(Saida_impulso, N, Ts, "Resposta do Sistema a função 'Impulso'")
Metodos_Graficos.Plotar_Analise_Sinal_(Saida_degrau,  N, Ts, "Resposta do Sistema a função 'Degrau'")
Metodos_Graficos.Plotar_Analise_Sinal_(Saida,         N, Ts, "Sinal Reverberado")
Metodos_Graficos.Plotar_Comparacao_Sinais_(Sinal, Saida,  N)


# 
# Processamento do audio reverberado para ".wav".
############################################################################################################
Sound.write("Audios/Saida_Reverberada.wav", Saida, Freq)