#Biblioteca que fornecerá a HEAP de mínimo que será utilizado para fazer a fila de eventos discretos
import heapq
#Código feito pelo grupo onde é definido a classe Evento com dados necessários para o tratamento de um evento
from sim_evento import Evento
#Código feito pelo grupo onde é definido a classe Packet com dados necessários para o tratamento de eventos
#e geração de estatísticas
from sim_costumer import Packet
#Função importada para gerar valores para variavéis aleatórios exponenciais
from random import expovariate
#Função importada para decidir entre período de silêncio ou não
from random import randint
#Função para selecionar uma probabilidade aleatoriamente
from random import random
#Biblioteca importada para calcular raiz
from random import seed
import math
from decimal import getcontext
from decimal import Decimal
getcontext().prec = 12
print("-----------------------------------")
print(" THIS IS THE ROTEADOR SIMULATOR    ")
print("-----------------------------------")

#Aqui são definidos uma série de parâmetros para o simulador. Estão colocados assim para facilitar a vida
#do programador
#lamb_data: Taxa de chegada de pacotes de dados. Calculado por Little:
#utilização = lamb_data*E[X1]
#E[X1] = E[L]/data_speed
#utilização = lamb_data*E[L]/data_speed
#utilização*data_speed/E[L] = lamb_data
#Fazendo utilização = 10% e convertendo de bytes para bits
#lamb_data = 0.1*2000000/6040
lamb_data = 33.112582781456953642384105960265
#Colocado para facilitar a quantidade de utilização por dados que desejo colocar
multiplier_lamb_data = 7
#Definindo lamb_data para uma certa utilização
lamb_data = multiplier_lamb_data*lamb_data
#Capacidade do canal
data_speed = Decimal(2000000.0)
#Média do número de pacotes de voz transmitidos em um período de atividade por um canal de voz
mean_voice_packets = 22
#Intervalo entre pacotes de voz para um canal de voz
voice_time_gaps = Decimal(0.016)
#Taxa do tempo de um período de silêncio de canal de voz
lamb_silence = 1000.0/650.0
#Número de amostras por rodada
num_amostras = 3000
#Número de rodadas
num_rodadas = 100
#Variavél para definir a existência de interrupção ou não
withInterruption = False
#Tamanho da janela de voz
window_voice_size = Decimal(512)
#Tamanho da fase transiente
transient_size = 0
seed(1)

#A fila é inicializada com o evento de inicialização logo de início
#O evento de inicialização será explicado mais a frente
heap = [Evento(0.0,-1,-31,0)]
#Uma estrutura para mapear da identificação de um pacote para a instância do pacote
packets = {}
#Contador para definir identificação dos pacotes. Também é utilizado para determinar ordem de chegada dos pacotes
next_pid = 0
#Variável que facilita a obtenção do pacote sendo atendido para recalcular valores em outros pacotes
pid_OnService = -1
#Número de pacotes em espera na fila de voz
n_packs1_wait = 0
#Número de pacotes em espera na fila de dados
n_packs2_wait = 0
#Área do gráfico de número de pacotes de voz em espera ao longo do tempo
area_1 = Decimal(0.0)
#Área do gráfico de número de pacotes de voz em espera ao longo do tempo
area_2 = Decimal(0.0)
#Tempo da última chegada ou partida de pacote de voz
prev_time1 = Decimal(0.0)
#Tempo da última chegada ou partida de pacote de dados
prev_time2 = Decimal(0.0)
globaltime = Decimal(0.0)

def cdf_size(x):

    coefA=x-64
    coefB=x-512
    coefC=x-1500

    if coefA == 0:	
        uMenosUmA = 1
        uMenosDoisA = coefA
    if coefA>0:
        uMenosUmA = 1
        uMenosDoisA = coefA
    elif coefA<0:
        uMenosUmA = 0
        uMenosDoisA = 0

    if coefB == 0:	
        uMenosUmB = 1
        uMenosDoisB = coefB
    if coefB>0:
        uMenosUmB = 1
        uMenosDoisB = coefB
    elif coefB<0:
        uMenosUmB = 0
        uMenosDoisB = 0
	
    if coefC == 0:	
        uMenosUmC=1
        uMenosDoisC=coefC
    if coefC>0:
        uMenosUmC=1
        uMenosDoisC=coefC
    elif coefC<0:
        uMenosUmC=0
        uMenosDoisC=0
	
    l=Decimal(0.3*uMenosUmA+0.1*uMenosUmB+0.3*uMenosUmC+(0.3/1436.0)*(uMenosDoisA-uMenosDoisC))
    return l

#Função geradora de amostras aleatórias de tamanho de pacote
def mySampleL(prob):
    from math import floor
    if(prob <= 0.3): return 64
    b = 64
    e = 1500
    while (b <= e):
        m = (b+e)/2
        probm = cdf_size(m)
        if(probm == prob): return Decimal(floor(m))
        elif(prob < probm): e = m-0.1
        else: b = m+0.1
    return Decimal(floor(b))

def myExpSample(lambd):
    value = expovariate(lambd)
    return Decimal(value)

#Função tratadora de eventos
#A fim de facilitar, colocarei o que significa o código de cada evento:
#EVENTO 0: Inicialização
#EVENTO 1: Chegada de pacote de voz
#EVENTO 2: Tratamento de pacote de dados interrompido
#EVENTO 3: Pedido de serviço por pacote de voz
#EVENTO 4: Chegada de pacote de dados
#EVENTO 5: Pedido de serviço por pacote de dados
#EVENTO 6: Fim de serviço de pacote de voz
#EVENTO 7: Fim de serviço de pacote de dados
def handleEvent (event) :
    global heap, packets, next_pid, pid_OnService
    global n_packs1_wait, n_packs2_wait
    global area_1, area_2
    global prev_time1, prev_time2, globaltime
    #EVENTO 0: Inicialização
    if(event.EID == 0) :
        #Calcula momento de chegada do primeiro de pacote de dados
        arrival_time = myExpSample(lamb_data)
        #Cria o evento de chega
        arrival_event = Evento(arrival_time,-1,0,4)
        #E coloca na fila
        heapq.heappush(heap,arrival_event)
        #O mesmo é repetido para os outros canais
        for i in range(1,31):
            #Se ao jogar o dado de 22 faces for tirado qualquer número maior que 1
            #Continua enviando pacotes
            if(randint(1,mean_voice_packets) > 1):
                #Gera evento de chegada do primeiro pacote de voz e coloca na fila
                arrival_event_2 = Evento(voice_time_gaps,-1,-i,1)
                ##heapq.heappush(heap,arrival_event_2)
            else:
                #O tempo de silêncio, ele sempre acaba assim que chega o pacote, por
                #isso um intervalo de tempo entre pacotes foi colocado
                silence_time = Decimal(voice_time_gaps+myExpSample(lamb_silence))
                #O evento do período de silêncio é colocado como um evento de chegada
                #de pacote de voz, porque ele basicamente prolonga o tempo até o
                #próximo pacote
                arrival_after_silence_event = Evento(silence_time,-1,-i,1)
                ##heapq.heappush(heap,arrival_after_silence_event)
        return -1
        #EVENTO 1: Chegada de pacote de voz
    elif (event.EID == 1) :
        #Em uma chegada de pacote de voz, o pacote vai fazer um pedido de serviço.
        #Tal evento é gerado e colocado na fila
        packet_event = Evento(event.time,next_pid,1,3)
        packet = Packet(next_pid,event.time,1,window_voice_size)
        heapq.heappush(heap,packet_event)
        #Aqui se decidi, assim como no evento 0, se há início de tempo de silêncio ou não
        if(randint(1,mean_voice_packets) > 1):
            #Note que o tempo agora é o tempo atual mais um intervalo de tempo.
            #Ou seja, o tempo realmente indica o momento que o evento ocorre
            arrival_event = Evento(event.time+voice_time_gaps,-1,event.TYPE,1)
            heapq.heappush(heap,arrival_event)
        else:
            silence_time = event.time+Decimal(voice_time_gaps+myExpSample(lamb_silence))
            arrival_after_silence_event = Evento(silence_time,-1,event.TYPE,1)
            heapq.heappush(heap,arrival_after_silence_event)
        #O novo pacote é guardado no dicionário para ser facilmente obtido depois
        packets[next_pid] = packet
        #Incrementa_se next_pid para o próximo pacote que chegar
        next_pid = next_pid+1
        return -1
    #EVENTO 2: Tratamento de pacote de dados interrompido
    elif (event.EID == 2) :
        #Pacote interrompido
        intd_packet = packets[event.PID]
        #Pacote que interrompeu
        serv_packet = packets[pid_OnService]
        #O tempo de serviço do pacote precisa ser atualizado, pois ele não realizou todo o seu serviço
        #dec_time_service corresponde aquela porção do tempo do serviço de intd_packet que não foi cumprido
        #dec_time_service = tempo_de_finalização_de_intd_packet-tempo_de_pedido_serv_packet
        dec_time_service = intd_packet.time-(serv_packet.time-serv_packet.time_service)
        #Este valor é finalmente retirado de itd_packet
        intd_packet.time_service = intd_packet.time_service-dec_time_service
        #Agora ele tem que esperar ele acabar o serviço desse novo pacote
        intd_packet.time_wait = intd_packet.time_wait+serv_packet.time_service
        #Ele atualiza o tempo dele (precisa estar sincronizado com o evento associado)
        intd_packet.time = serv_packet.time
        #Gera-se evento de retorno a fila. O evento recebe o mesmo tempo que o serviço termina
        #para que a solicitação de serviço seja feita no término do serviço
        back_event = Evento(serv_packet.time,event.PID,2,5)
        #Procura-se a posição ao qual está o evento associado ao pacote e o modifica
        for i in range(0,len(heap)):
            if(event.PID == heap[i].PID):
                heap[i] = back_event
                break
        #Ordena a heap para não ter bagunça
        heapq.heapify(heap)
        return -1
        #EVENTO 3: Pedido de serviço por pacote de voz
    elif (event.EID == 3):
        #Caso o canal esteja livre, pacote de voz pega canal
        if(pid_OnService < 0):
            if(n_packs1_wait > 0):
                area_1 = area_1 + (event.time-prev_time1)*n_packs1_wait
                n_packs1_wait = n_packs1_wait-1
                globaltime = globaltime+event.time-prev_time1
                prev_time1 = event.time
            
            pid_OnService = event.PID
            service_packet = packets[pid_OnService]
            service_packet.time = event.time+window_voice_size/data_speed
            service_packet.time_service = window_voice_size/data_speed
            #É gerado o evento de finalização do serviço do pacote de voz, por isso
            #seu tempo é definido como o tempo do pedido mais o tempo do para completar o serviço
            service_event = Evento(event.time+window_voice_size/data_speed,event.PID,1,6)
            heapq.heappush(heap,service_event)
            #No caso de ser um pacote de dados estiver sendo servido e ele puder ser interrompido
        elif(withInterruption and packets[pid_OnService].TYPE == 2):
            #Gera-se um evento com tempo 0 para a interrupção ser atendida logo após tratamento desse evento
            int_event = Evento(0,pid_OnService,2,2)
            heapq.heappush(heap,int_event)
            #Procede como se o canal estivesse livre
            pid_OnService = event.PID
            service_packet = packets[pid_OnService]
            service_packet.time = event.time+window_voice_size/data_speed
            service_packet.time_service = window_voice_size/data_speed
            service_event = Evento(event.time+window_voice_size/data_speed,event.PID,1,6)
            heapq.heappush(heap,service_event)
            #Caso não possa ser interrompido ou haver um pacote de voz
        else:
            voice_packet = packets[pid_OnService]
            packet = packets[event.PID]

            if(not (packet.time_wait > 0)):
                area_1 = area_1 + n_packs1_wait*(event.time-prev_time1)
                n_packs1_wait = n_packs1_wait+1
                globaltime = globaltime+event.time-prev_time1
                prev_time1 = event.time

            #O novo tempo de espera do pacote é calculado pela diferença entre o momento que o serviço
            #termina e o momento que ele pede serviço, pois um pacote pode chegar no meio do atendimento 
            #de outro pacote, tendo que esperar apenas o restante do serviço
            packet.time_wait = packet.time_wait+voice_packet.time-packet.time
            packet.time = voice_packet.time
            packet_event = Evento(packet.time,event.PID,1,3)
            heapq.heappush(heap,packet_event)
        return -1
        #EVENTO 4: Chegada de pacote de dados
    elif (event.EID == 4):
        packet = Packet(next_pid, event.time, 2, 8*mySampleL(random()))
        #packet = Packet(next_pid, event.time, 2, 6040)
        packets[next_pid] = packet
        packet_event = Evento(event.time,next_pid,2,5)
        event.time = event.time + myExpSample(lamb_data)
        heapq.heappush(heap,packet_event)
        heapq.heappush(heap,event)
        next_pid = next_pid+1
        return -1
        #EVENTO 5: Pedido de serviço por pacote de dados
    elif (event.EID == 5):
        #Funciona de forma muito similar ao pedido de serviço de pacote de voz
        if(pid_OnService < 0):
            if(n_packs2_wait > 0):
                area_1 = area_1 + n_packs1_wait*(event.time-prev_time1)
                area_2 = area_2 + n_packs2_wait*(event.time-prev_time2)
                n_packs2_wait = n_packs2_wait-1
                globaltime = globaltime+event.time-min([prev_time1,prev_time2])
                prev_time1 = event.time
                prev_time2 = event.time
            
            #Indica que ocupou o canal
            pid_OnService = event.PID
            service_packet = packets[event.PID]
            service_packet.time = event.time+service_packet.size/data_speed
            service_packet.time_service = service_packet.size/data_speed
            #Gera evento de finalização serviço
            service_event = Evento(event.time+service_packet.size/data_speed,event.PID,2,7)
            heapq.heappush(heap,service_event)
        else:
            #Pega o pacote que pediu serviço e o pacote em serviço
            service_packet = packets[pid_OnService]
            packet = packets[event.PID]
            if(not (packet.time_wait > 0)):
                area_1 = area_1 + n_packs1_wait*(event.time-prev_time1)
                area_2 = area_2 + n_packs2_wait*(event.time-prev_time2)
                n_packs2_wait = n_packs2_wait+1
                globaltime = globaltime+event.time-min([prev_time1,prev_time2])
                prev_time1 = event.time
                prev_time2 = event.time
            #Calcula seu novo tempo de espera conforme explicado antes
            packet.time_wait = packet.time_wait+service_packet.time-packet.time
            packet.time = service_packet.time
            #Programa o evento para ocorrer na finalização do serviço
            #Observe que o evento tratado possuía mesmo PID, mesmo TYPE e mesmo EID
            #Então para aproveitar o evento, foi alterado apenas o tempo em que ele
            #ocorre novamente
            event.time = service_packet.time
            heapq.heappush(heap,event)
        return -1
        #EVENTO 6: Fim de serviço de pacote de voz
    elif (event.EID == 6):
        #Para indicar fim de serviço, basta indicar que o canal está livre
        pid_OnService = -1
        area_1 = area_1 + n_packs1_wait*(event.time-prev_time1)
        globaltime = globaltime+event.time-prev_time1
        prev_time1 = event.time
        #Diferentemente dos outros eventos, este retorna o PID do pacote para
        #o cálculo de estatísticas
        return event.PID
        #EVENTO 7: Fim de serviço de pacote de dados
    elif (event.EID == 7):
        pid_OnService = -1
        area_1 = area_1 + n_packs1_wait*(event.time-prev_time1)
        area_2 = area_2 + n_packs2_wait*(event.time-prev_time2)
        globaltime = globaltime+event.time-min([prev_time1,prev_time2])
        prev_time1 = event.time
        prev_time2 = event.time
        return event.PID

