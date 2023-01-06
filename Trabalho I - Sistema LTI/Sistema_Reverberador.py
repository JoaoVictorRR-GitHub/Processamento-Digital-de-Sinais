############################################################################################################
# IMPLEMENTACAO DO SISTEMA DE REVERBERACAO #
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
############################################################################################################


# 
# Classe.
class Schroeder_Reverbs_:
 
    """
    Classe que representa o modelo
    de Reverberacao de Schroeder.
    """

    def __init__(Self, Freq) -> None:
        """
        Metodo responsavel pela inicializacao da
        classe com os seus respectivos atributos.
        """
        Self.Reverb = 0.3                                                   # Tempo de reverberacao (s) em um ambiente.
        Self.Delays = [29.7e-3, 37.1e-3, 41.1e-3, 43.7e-3, 5e-3, 1.7e-3]    # Tempo de delay para cada filtro (Comb-IIR ou All-pass).
        Self.Tds    = []                                                    # Taxa de amostragem para cada delay.
        Self.Ganhos = []                                                    # Taxa de ganho para cada filtro.

        # Loop para calcular as taxas de delay e os ganhos.
        for i in range(len(Self.Delays)):
            Self.Tds.append( round(Self.Delays[i] * Freq) )
            Self.Ganhos.append( (0.001) ** (Self.Delays[i] / Self.Reverb) )



    def Filtro_Universal_(Self, Sinal, Td, BL, FB, FF):
        """
        Metodo responsavel por filtrar um sinal atraves
        de um filtro "FIR" ou "IIR" (A mudanca ocorre
        de acordo com os parametros de entrada).

        Entrada:
            - Vetor de pontos do sinal.
            - Taxa de amostragem de delay por filtro.
            - Taxa de ganho de mesclagem.
            - Taxa de ganho de realimentacao.
            - Taxa de ganho de realimentacao direta.

        Saida:
            - Vetor de pontos do sinal filtrado.
        """

        Tam   = len(Sinal)
        Saida = Np.zeros(Tam)
        Delay = Np.zeros(Td)

        PA = -1 # Porcentagem de conclusao auxiliar.

        # Loop para aplicar o filtro universal.
        for i in range(Tam):
            D        = Sinal[i] + FB*Delay[Td-1]
            Saida[i] = FF*Delay[Td-1] + BL*D
            Delay    = list([D]) + list(Delay[0:Td-1])
            
            # Porcentagem de conclusao.
            PC = ((i*100)//Tam)
            if((PC % 10 == 0) and (PC != PA)):
                print(PC, "%")
                PA = PC

        print("Passagem concluída...\n")
        return Saida



    def Schroeder___Metodo_01_(Self, Sinal, Qnt_all_pass = 5):
        """
        Metodo para aplicar o efeito de reverberacao em
        um sinal passando-o por um sistema de filtros
        "All-pass" em serie (1º Metodo de Schroeder).

        Entrada:
            - Vetor de pontos do sinal.
            - Quantidade de filtros "All-pass" a serem aplicados.
        
        Saida:
            - Vetor de pontos do Sinal com o efeito de reverberacao.
        """ 

        # Loop para aplicar os filtros "All-pass" em serie.
        for i in range(Qnt_all_pass):
            print(f"--->    {i+1:02}º filtro All-pass.")
            Filtro_All_pass = [Self.Ganhos[i], -Self.Ganhos[i], 1]  # Parametros do filtro All-pass.
            Sinal           = Self.Filtro_Universal_(Sinal, Self.Tds[i], Filtro_All_pass[0], Filtro_All_pass[1], Filtro_All_pass[2])
            
        return Sinal



    def Schroeder___Metodo_02_(Self, Sinal, Qnt_comb = 4, Qnt_all_pass = 2):
        """
        Metodo para aplicar o efeito de reverberacao em um sinal
        passando-o por um sistema de filtros "Comb-IIR" em paralelo
        e filtros "All-pass" em serie (2º Metodo de Schroeder).

        Entrada:
            - Vetor de pontos do sinal.
            - Quantidade de filtros "Comb-IIR" a serem aplicados.
            - Quantidade de filtros "All-pass" a serem aplicados.
        
        Saida:
            - Vetor de pontos do Sinal com o efeito de reverberacao.
        """

        Saida = Np.zeros(len(Sinal))

        # Loop para aplicar os filtros "Comb-IIR" em paralelo.
        for i in range(Qnt_comb):
            print(f"--->    {i+1:02}º Comb-filter IIR.")
            Filtro_IIR = [1, Self.Ganhos[i], 0]                     # Parametros do filtro IIR. 
            Comb       = Self.Filtro_Universal_(Sinal, Self.Tds[i], Filtro_IIR[0], Filtro_IIR[1], Filtro_IIR[2])
            Saida     += Comb

        Saida /= Qnt_comb

        # Loop para aplicar os filtros "All-pass" em serie.
        for i in range(Qnt_all_pass):
            print(f"--->    {i+1:02}º filtro All-pass.")
            Filtro_All_pass = [Self.Ganhos[i], -Self.Ganhos[i], 1]  # Parametros do filtro All-pass.
            Saida           = Self.Filtro_Universal_(Saida, Self.Tds[Qnt_comb +i], Filtro_All_pass[0], Filtro_All_pass[1], Filtro_All_pass[2])
        
        return Saida
############################################################################################################