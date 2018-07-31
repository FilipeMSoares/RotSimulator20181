import event_handler as sim
from decimal import Decimal
from decimal import getcontext
getcontext().prec = 12
#Ignore e vá para o LOOP do simulador da fase em equilíbrio
#Este simplesmente trata eventos e finaliza a fase transiente
print("transient state")
count_rodadas = 0
count_samples = 0
#Esta variável está aqui para calcular o tempo decorrido, já que uma fase transiente
#acaba no instante com tempo maior que zero
prevtime = 0.0
while count_rodadas < sim.transient_size :
    event = sim.heapq.heappop(sim.heap)
    pid = sim.handleEvent(event)
    if(event.time > prevtime):
        prevtime = event.time
    if(pid >= 0):
        count_samples = count_samples+1
        if(count_samples == sim.num_amostras):
            count_samples = 0
            count_rodadas = count_rodadas + 1

#Fase de equilíbrio
print("steady state")
#Somatório do tempo gasto por pacotes de voz
total_time_1 = Decimal(0.0)
#Somatório do tempo gasto por pacotes de dados
total_time_2 = Decimal(0.0)
#Lista das médias do tempo médio gasto por pacote de voz em cada rodada
total_times_1 = []
#Lista das médias do tempo médio gasto por pacote de dados em cada rodada
total_times_2 = []
#Somatório dos tempos de espera de pacotes de voz
total_time_wait_1 = Decimal(0.0)
#Somatório dos tempos de espera de pacotes de dados
total_time_wait_2 = Decimal(0.0)
#Lista das médias do tempo médio gasto por pacotes de dados em cada rodada
total_time_waits_1 = []
#Lista das médias do tempo médio de espera por pacote de dados em cada rodada
total_time_waits_2 = []
#Somatório dos tempos de serviço de pacotes de voz
total_time_service_1 = Decimal(0.0)
#Somatório dos tempos de serviço de pacotes de dados
total_time_service_2 = Decimal(0.0)
#Lista das médias do tempo médio de serviço por pacote de voz em cada rodada
total_time_services_1 = []
#Lista das médias do tempo médio de serviço por pacote de dados em cada rodada
total_time_services_2 = []
#Lista das médias do número médio de pacotes de voz em espera em cada rodada
queue_counts_1 = []
#Lista das médias do número médio de pacotes de dados em espera em cada rodada
queue_counts_2 = []
#Contador de amostras obtidas numa rodada
count = 0
#Número de amostras de pacotes de voz obtidas em uma rodada
count1 = 0
#Número de amostras de pacotes de dados obtidas em uma rodada
count2 = 0
#Contador do número de rodadas já passadas
count_rodadas = 0
#Tempo decorrido em uma rodada
starttime = Decimal(sim.heap[0].time)
sim.area_1 = Decimal(0.0)
sim.area_2 = Decimal(0.0)
#LOOP do simulador
prevprint = 0
prevtime = 0.0
little = []
while count_rodadas < sim.num_rodadas :
    #print(n_packs1_wait,n_packs2_wait)
    #Pega o evento da fila
    event = sim.heapq.heappop(sim.heap)
    #Trata ele e pega o pid de um possível pacote
    pid = sim.handleEvent(event)
    #Se for pid de um pacote
    if(pid >= 0):
        #Pega o pacote
        packet = sim.packets[pid]
        #Conta amostra obtida
        count = count+1
        #if(packet.TYPE == 1 and packet.time_service != Decimal(0.000256) ):
            #print("ERROR")
        #Conta qual o tipo do amostra
        if(packet.TYPE == 1):
            count1 = count1+1
        elif(packet.TYPE == 2):
            count2 = count2+1
        #Calcula o tempo decorrido
        if(prevtime < event.time):
            #globaltime = globaltime + event.time-prevtime
            prevtime = event.time
        if(count_rodadas < sim.num_rodadas):
            #Caso a rodada não tenha acabado, calcule as somas
            if(count2 < sim.num_amostras):
                if(packet.TYPE == 1):
                    total_time_1 = total_time_1+packet.time_wait+packet.time_service
                    total_time_service_1 = total_time_service_1+packet.time_service
                    total_time_wait_1 = total_time_wait_1+packet.time_wait
                    #print(total_time_service_1,count1,total_time_service_1/count1,packet.time_service)
                elif(packet.TYPE == 2):
                    total_time_2 = total_time_2+packet.time_wait+packet.time_service
                    total_time_service_2 = total_time_service_2+packet.time_service
                    total_time_wait_2 = total_time_wait_2+packet.time_wait
            #Senão, calcule as estatísticas
            else:
                endtime = Decimal(event.time)
                sim.globaltime = Decimal(endtime-starttime)
                #Algums resets de variavéis
                count_rodadas = count_rodadas+1
                count = 0
                #Evitando divisão por zero
                if(count1 == 0):
                    count1 = 1
                if(count2 == 0):
                    count2 = 1
                #Adiciona as médias as listas para o caso dos pacotes voz
                total_times_1.append(total_time_1/count1)
                total_time_services_1.append(total_time_service_1/count1)
                total_time_waits_1.append(total_time_wait_1/count1)
                queue_counts_1.append(sim.area_1/sim.globaltime)
                #Mais resets
                total_time_1 = Decimal(0.0)
                total_time_service_1 = Decimal(0.0)
                total_time_wait_1 = Decimal(0.0)
                sim.area_1 = Decimal(0.0)
                count1 = 0
                #Adiciona as médias as listas para o caso dos pacotes dados
                total_times_2.append(total_time_2/count2)
                total_time_services_2.append(total_time_service_2/count2)
                total_time_waits_2.append(total_time_wait_2/count2)
                queue_counts_2.append(sim.area_2/sim.globaltime)
                little.append( Decimal(sim.lamb_data)*(total_time_wait_2/count2) )
                #Últimos resets
                total_time_2 = Decimal(0.0)
                total_time_service_2 = Decimal(0.0)
                total_time_wait_2 = Decimal(0.0)
                sim.area_2 = Decimal(0.0)
                count2 = 0
                starttime = endtime
    #Caso um pacote tenha sido retornado, retirá-lo, pois ele não é mais necessário
    if(pid >= 0):
        del sim.packets[pid]

from statistics import calc_and_plot
from statistics import plot_confidence_ints
calc_and_plot(sim.num_rodadas,total_times_1,total_times_2,total_time_waits_1,total_time_waits_2,total_time_services_1,total_time_services_2,queue_counts_1,queue_counts_2)
#plot_confidence_ints(sim.num_rodadas,total_times_1,total_times_2,total_time_waits_1,total_time_waits_2,total_time_services_1,total_time_services_2,queue_counts_1,queue_counts_2)
