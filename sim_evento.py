class Evento :
    #Tempo em que ocorre o evento
    time = 0.0
    #Identificação de pacote possivelmente associado a este evento
    # (PIDs são sempre positivos)
    PID = -1
    #Tipo do pacotes (1: Voz, 2: Dados)
    TYPE = 0
    #Identificação do evento, muito importante para o tratamento de eventos
    EID = -1
    
    #Construtor
    def __init__(self,time,pid,_type,eid):
        self.time = time
        self.PID = pid
        self.TYPE = _type
        self.EID = eid
    
    #Função de comparação para saber como a heap ordenar os eventos
    def __lt__(self,other):
        #Caso não seja possível ordenar por tempo
        if(self.time == other.time):
            #Essa condição é assumidamente uma "gambiarra"
            #Foi necessária para garantir que encerramento de serviço de dados
            #Seja ignorado pois tem pacotes de voz na fila
            if(self.TYPE == 2 and other.TYPE != self.TYPE):
                if(self.EID == 7):
                    return self.EID > other.EID
            elif(self.TYPE != other.TYPE and other.TYPE == 2):
                if(other.EID == 7):
                    return self.EID > other.EID
            #Caso sejam do mesmo tipo
            if(self.TYPE == other.TYPE):
                #Quarto critério: ordem de chegada
                #Ordem de chegada pois assim que o pacote "chega ao roteador",
                #ele recebe uma identificação determinado por uma variável que
                #começa em 0 e aumenta em 1 para cada novo pacote que chega
                return self.PID < other.PID
            else:
                #Terceiro critério: Tipo do pacote
                return self.TYPE < other.TYPE
        else:
            #Primeiro critério de ordenação: tempo
            return self.time < other.time
