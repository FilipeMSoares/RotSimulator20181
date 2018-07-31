class Packet:
    from decimal import Decimal
    #Identificação do pacote
    pid = -1
    #Tamanho do pacote
    size = Decimal(0)
    #Tipo dele
    TYPE = 0
    #Variável utilizada para facilitar o cálculo de time_wait em outros pacotes
    #Ele deve estar obrigatoriamente sincronizado com o do evento associado para
    #que tudo ocorra de maneira correta
    time = Decimal(0.0)
    #Variável utilizada no cálculo de estatísticas, especificamente o tempo de espera
    time_wait = Decimal(0.0)
    #Variável utilizada no cálculo de estatística, especificamente o tempo de serviço
    time_service = Decimal(0.0)

    #Construtor
    def __init__ (self,pid,time,_type,size):
        self.pid = pid
        self.time = time
        self.TYPE = _type
        self.size = size
    
