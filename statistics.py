def decimal_to_float_list(list):
    for i in range(0,len(list)):
        list[i] = float(list[i])

def calc_and_plot(num_rodadas,total_times_1,total_times_2,total_time_waits_1,total_time_waits_2,total_time_services_1,total_time_services_2,queue_counts_1,queue_counts_2):
    import math
    xaxis = [i+1 for i in range(0,num_rodadas)]
    decimal_to_float_list(total_times_1)
    decimal_to_float_list(total_times_2)
    decimal_to_float_list(total_time_waits_1)
    decimal_to_float_list(total_time_waits_2)
    decimal_to_float_list(total_time_services_1)
    decimal_to_float_list(total_time_services_2)
    decimal_to_float_list(queue_counts_1)
    decimal_to_float_list(queue_counts_2)

    def calc_error(_list):
        if(max(_list) == min(_list)):
            return 0.001
        return (1-math.exp(float(-max(_list)+min(_list))))

    import matplotlib.pyplot as plt
    plt.figure()
    plt.scatter(xaxis,total_times_1)
    plt.title("(1-T) Tempo médio de voz")
    error = calc_error(total_times_1)
    plt.ylim(min(total_times_1)-error,max(total_times_1)+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,total_time_services_1)
    plt.title("(1-X) Tempo médio de serviço de voz")
    error = calc_error(total_time_services_1)
    plt.ylim(min(total_time_services_1)-error,max(total_time_services_1)+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,total_time_waits_1)
    plt.title("(1-W) Tempo médio de espera de voz")
    error = calc_error(total_time_waits_1)
    plt.ylim(min(total_time_waits_1)-error,max(total_time_waits_1)+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,queue_counts_1)
    plt.title("(1-Nq) Número médio de pacotes de voz em espera")
    error = calc_error(queue_counts_1)
    plt.ylim(min(queue_counts_1)-error,max(queue_counts_1)+error)
    plt.show()

    #plt.figure()
    #plt.scatter(total_time_waits_1,queue_counts_1)
    #plt.scatter(total_time_waits_1,[658.59375*x for x in total_time_waits_1])
    #error = calc_error(total_time_waits_1)
    #plt.xlim(min(total_time_waits_1)-error,max(total_time_waits_1)+error)
    #plt.show()

    #plt.figure()
    #newvet = []
    #for i in range(0,len(total_time_waits_1)) :    
    #    if(total_time_waits_1[i] > 0):
    #        newvet.append( queue_counts_1[i]/(658.59375*total_time_waits_1[i]) )
    #    else:
    #        newvet.append( 0.0 )
    #plt.scatter(total_time_waits_1,newvet)
    #error = calc_error(total_time_waits_1)
    #plt.xlim(min(total_time_waits_1)-error,max(total_time_waits_1)+error)
    #plt.show()

    plt.figure()
    plt.scatter(xaxis,total_times_2)
    plt.title("(2-T) Tempo médio de dados")
    error = calc_error(total_times_2)
    plt.ylim(min(total_times_2)-error,max(total_times_2)+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,total_time_services_2)
    plt.title("(2-X) Tempo médio de serviço de dados")
    error = calc_error(total_time_services_2)
    plt.ylim(min(total_time_services_2)-error,max(total_time_services_2)+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,total_time_waits_2)
    plt.title("(2-W) Tempo médio de espera de dados")
    error = calc_error(total_time_waits_2)
    plt.ylim(min(total_time_waits_2)-error,max(total_time_waits_2)+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,queue_counts_2)
    plt.title("(2-Nq) Número médio de pacotes de dados em espera")
    error = calc_error(queue_counts_2)
    plt.ylim(min(queue_counts_2)-error,max(queue_counts_2)+error)
    plt.show()

    #plt.figure()
    #plt.scatter(total_time_waits_2,queue_counts_2)
    #plt.show()

def plot_confidence_ints(num_rodadas,total_times_1,total_times_2,total_time_waits_1,total_time_waits_2,total_time_services_1,total_time_services_2,queue_counts_1,queue_counts_2):
    import matplotlib.pyplot as plt
    import math 
    def mean(_list):
        return sum(_list)/max(len(_list),1)

    def std(_list):
        mean_value = mean(_list)
        return math.sqrt(sum([(value-mean_value)*(value-mean_value) for value in _list])/max(len(_list)-1,1))
    
    decimal_to_float_list(total_times_1)
    decimal_to_float_list(total_times_2)
    decimal_to_float_list(total_time_waits_1)
    decimal_to_float_list(total_time_waits_2)
    decimal_to_float_list(total_time_services_1)
    decimal_to_float_list(total_time_services_2)
    decimal_to_float_list(queue_counts_1)
    decimal_to_float_list(queue_counts_2)

    mean_time_1 = mean(total_times_1)
    std_time_1 = std(total_times_1)

    mean_time_2 = mean(total_times_2)
    std_time_2 = std(total_times_2)

    mean_time_service_1 = mean(total_time_services_1)
    std_time_service_1 = std(total_time_services_1)

    mean_time_service_2 = mean(total_time_services_2)
    std_time_service_2 = std(total_time_services_2)

    mean_time_wait_1 = mean(total_time_waits_1)
    std_time_wait_1 = std(total_time_waits_1)

    mean_time_wait_2 = mean(total_time_waits_2)
    std_time_wait_2 = std(total_time_waits_2)

    mean_queue_count_1 = mean(queue_counts_1)
    std_queue_count_1 = std(queue_counts_1)

    mean_queue_count_2 = mean(queue_counts_2)
    std_queue_count_2 = std(queue_counts_2)

    percentil_90 = 1.64

    plt.figure()
    means = [mean_time_1]
    errs = [percentil_90*std_time_1/math.sqrt(num_rodadas)]
    plt.errorbar(means,['T1'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Tempo médio de voz")
    plt.show()

    plt.figure()
    means = [mean_time_2]
    errs = [percentil_90*std_time_2/math.sqrt(num_rodadas)]
    plt.errorbar(means,['T2'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Tempo médio de dados")
    plt.show()

    plt.figure()
    means = [mean_time_service_1]
    errs = [percentil_90*std_time_service_1/math.sqrt(num_rodadas)]
    plt.errorbar(means,['X1'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Tempo médio de serviço de voz")
    plt.show()

    plt.figure()
    means = [mean_time_service_2]
    errs = [percentil_90*std_time_service_2/math.sqrt(num_rodadas)]
    plt.errorbar(means,['X2'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Tempo médio de serviço de dados")
    plt.show()

    plt.figure()
    means = [mean_time_wait_1]
    errs = [percentil_90*std_time_wait_1/math.sqrt(num_rodadas)]
    plt.errorbar(means,['W1'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Tempo médio de espera de voz")
    plt.show()

    plt.figure()
    means = [mean_time_wait_2]
    errs = [percentil_90*std_time_wait_2/math.sqrt(num_rodadas)]
    plt.errorbar(means,['W2'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Tempo médio de espera de dados")
    plt.show()

    plt.figure()
    means = [mean_queue_count_1]
    errs = [percentil_90*std_queue_count_1/math.sqrt(num_rodadas)]
    plt.errorbar(means,['Nq1'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Número médio de pacotes de voz em espera")
    plt.show()

    plt.figure()
    means = [mean_queue_count_2]
    errs = [percentil_90*std_queue_count_2/math.sqrt(num_rodadas)]
    plt.errorbar(means,['Nq2'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Número médio de pacotes de dados em espera")
    plt.show()

def make_little(lamb,list):
    _list = []
    for x in list :
        _list.append(lamb*x)
    return _list

def make_inv_little(lamb,list):
    _list = []
    for x in list :
        _list.append(x/lamb)
    return _list

def little_plots(lamb1,lamb2,num_rodadas,utilization_1,utilization_2,total_time_waits_1,total_time_waits_2,total_time_services_1,total_time_services_2,queue_counts_1,queue_counts_2):
    import math
    xaxis = [i+1 for i in range(0,num_rodadas)]
    utilization_1 = [0 for i in range(0,num_rodadas)]
    
    decimal_to_float_list(total_time_waits_1)
    little_q_counts_1 = make_little(lamb1,total_time_waits_1)

    decimal_to_float_list(total_time_waits_2)
    little_q_counts_2 = make_little(lamb2,total_time_waits_2)

    decimal_to_float_list(total_time_services_1)
    little_utilization_1 = make_little(lamb1,total_time_services_1)

    decimal_to_float_list(total_time_services_2)
    little_utilization_2 = make_little(lamb2,total_time_services_2)
    
    decimal_to_float_list(utilization_1)
    little_time_services_1 = make_inv_little(lamb1,utilization_1)

    decimal_to_float_list(utilization_2)
    little_time_services_2 = make_inv_little(lamb2,utilization_2)

    decimal_to_float_list(queue_counts_1)
    little_time_waits_1 = make_inv_little(lamb1,queue_counts_1)

    decimal_to_float_list(queue_counts_2)
    little_time_waits_2 = make_inv_little(lamb2,queue_counts_2)

    def calc_error(_list):
        if(max(_list) == min(_list)):
            return 0.001
        return (1-math.exp(float(-max(_list)+min(_list))))

    import matplotlib.pyplot as plt
    
    plt.figure()
    plt.scatter(xaxis,total_time_services_1)
    plt.scatter(xaxis,little_time_services_1)
    plt.title("(1-X) Tempo médio de serviço de voz")
    error = max(calc_error(total_time_services_1),calc_error(little_time_services_1))
    plt.ylim(min(min(total_time_services_1),min(little_time_services_1))-error,max(max(total_time_services_1),max(little_time_services_1))+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,total_time_waits_1)
    plt.scatter(xaxis,little_time_waits_1)
    plt.title("(1-W) Tempo médio de espera de voz")
    error = max(calc_error(total_time_waits_1),calc_error(little_time_waits_1))
    plt.ylim(min(min(total_time_waits_1),min(little_time_waits_1))-error,max(max(total_time_waits_1),max(little_time_waits_1))+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,queue_counts_1)
    plt.scatter(xaxis,little_q_counts_1)
    plt.title("(1-Nq) Número médio de pacotes de voz em espera")
    error = max(calc_error(queue_counts_1),calc_error(little_q_counts_1))
    plt.ylim(min(min(queue_counts_1),min(little_q_counts_1))-error,max( max(queue_counts_1),max(little_q_counts_1) )+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,utilization_1)
    plt.scatter(xaxis,little_utilization_1)
    plt.title("(1-Ns) Número médio de pacotes de voz em serviço")
    error = max(calc_error(utilization_1),calc_error(little_utilization_1))
    plt.ylim(min(min(utilization_1),min(little_utilization_1))-error,max( max(utilization_1),max(little_utilization_1) )+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,total_time_services_2)
    plt.scatter(xaxis,little_time_services_2)
    plt.title("(2-X) Tempo médio de serviço de dados")
    error = max(calc_error(total_time_services_2),calc_error(little_time_services_2))
    plt.ylim(min(min(total_time_services_2),min(little_time_services_2))-error,max(max(total_time_services_2),max(little_time_services_2))+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,total_time_waits_2)
    plt.scatter(xaxis,little_time_waits_2)
    plt.title("(2-W) Tempo médio de espera de dados")
    error = max(calc_error(total_time_waits_2),calc_error(little_time_waits_2))
    plt.ylim(min(min(total_time_waits_2),min(little_time_waits_2))-error,max(max(total_time_waits_2),max(little_time_waits_2))+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,queue_counts_2)
    plt.scatter(xaxis,little_q_counts_2)
    plt.title("(2-Nq) Número médio de pacotes de dados em espera")
    error = max(calc_error(queue_counts_2),calc_error(little_q_counts_2))
    plt.ylim(min(min(queue_counts_2),min(little_q_counts_2))-error,max( max(queue_counts_2),max(little_q_counts_2) )+error)
    plt.show()

    plt.figure()
    plt.scatter(xaxis,utilization_2)
    plt.scatter(xaxis,little_utilization_2)
    plt.title("(2-Ns) Número médio de pacotes de dados em serviço")
    error = max(calc_error(utilization_2),calc_error(little_utilization_2))
    plt.ylim(min(min(utilization_2),min(little_utilization_2))-error,max( max(utilization_2),max(little_utilization_2) )+error)
    plt.show()

def plot_little_conf_ints(lamb1,lamb2,num_rodadas,utilization_1,utilization_2,total_time_waits_1,total_time_waits_2,total_time_services_1,total_time_services_2,queue_counts_1,queue_counts_2):
    import matplotlib.pyplot as plt
    import math 
    def mean(_list):
        return sum(_list)/max(len(_list),1)

    def std(_list):
        mean_value = mean(_list)
        return math.sqrt(sum([(value-mean_value)*(value-mean_value) for value in _list])/max(len(_list)-1,1))
    
    utilization_1 = [0 for i in range(0,num_rodadas)]
    
    decimal_to_float_list(total_time_waits_1)
    little_q_counts_1 = make_little(lamb1,total_time_waits_1)

    decimal_to_float_list(total_time_waits_2)
    little_q_counts_2 = make_little(lamb2,total_time_waits_2)

    decimal_to_float_list(total_time_services_1)
    little_utilization_1 = make_little(lamb1,total_time_services_1)

    decimal_to_float_list(total_time_services_2)
    little_utilization_2 = make_little(lamb2,total_time_services_2)
    
    decimal_to_float_list(utilization_1)
    little_time_services_1 = make_inv_little(lamb1,utilization_1)

    decimal_to_float_list(utilization_2)
    little_time_services_2 = make_inv_little(lamb2,utilization_2)

    decimal_to_float_list(queue_counts_1)
    little_time_waits_1 = make_inv_little(lamb1,queue_counts_1)

    decimal_to_float_list(queue_counts_2)
    little_time_waits_2 = make_inv_little(lamb2,queue_counts_2)

    mean_utilization_1 = mean(utilization_1)
    std_utilization_1 = std(utilization_1)

    mean_utilization_2 = mean(utilization_2)
    std_utilization_2 = std(utilization_2)

    mean_time_service_1 = mean(total_time_services_1)
    std_time_service_1 = std(total_time_services_1)

    mean_time_service_2 = mean(total_time_services_2)
    std_time_service_2 = std(total_time_services_2)

    mean_time_wait_1 = mean(total_time_waits_1)
    std_time_wait_1 = std(total_time_waits_1)

    mean_time_wait_2 = mean(total_time_waits_2)
    std_time_wait_2 = std(total_time_waits_2)

    mean_queue_count_1 = mean(queue_counts_1)
    std_queue_count_1 = std(queue_counts_1)

    mean_queue_count_2 = mean(queue_counts_2)
    std_queue_count_2 = std(queue_counts_2)

    l_mean_utilization_1 = mean(little_utilization_1)
    l_std_utilization_1 = std(little_utilization_1)

    l_mean_utilization_2 = mean(little_utilization_2)
    l_std_utilization_2 = std(little_utilization_2)

    l_mean_time_service_1 = mean(little_time_services_1)
    l_std_time_service_1 = std(little_time_services_1)

    l_mean_time_service_2 = mean(little_time_services_2)
    l_std_time_service_2 = std(little_time_services_2)

    l_mean_time_wait_1 = mean(little_time_waits_1)
    l_std_time_wait_1 = std(little_time_waits_1)

    l_mean_time_wait_2 = mean(little_time_waits_2)
    l_std_time_wait_2 = std(little_time_waits_2)

    l_mean_queue_count_1 = mean(little_q_counts_1)
    l_std_queue_count_1 = std(little_q_counts_1)

    l_mean_queue_count_2 = mean(little_q_counts_2)
    l_std_queue_count_2 = std(little_q_counts_2)

    percentil_90 = 1.64

    plt.figure()
    means = [mean_utilization_1,l_mean_utilization_1]
    errs = [percentil_90*std_utilization_1/math.sqrt(num_rodadas),percentil_90*l_std_utilization_1/math.sqrt(num_rodadas)]
    plt.errorbar(means,['Ns1','L Ns1'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Número médio de pacotes de voz em serviço")
    plt.show()

    plt.figure()
    means = [mean_utilization_2,l_mean_utilization_2]
    errs = [percentil_90*std_utilization_2/math.sqrt(num_rodadas),percentil_90*l_std_utilization_2/math.sqrt(num_rodadas)]
    plt.errorbar(means,['Ns2','L Ns2'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Número médio de pacotes de dados em serviço")
    plt.show()

    plt.figure()
    means = [mean_time_service_1,l_mean_time_service_1]
    errs = [percentil_90*std_time_service_1/math.sqrt(num_rodadas),percentil_90*l_std_time_service_1/math.sqrt(num_rodadas)]
    plt.errorbar(means,['X1','L X1'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Tempo médio de serviço de voz")
    plt.show()

    plt.figure()
    means = [mean_time_service_2,l_mean_time_service_2]
    errs = [percentil_90*std_time_service_2/math.sqrt(num_rodadas),percentil_90*l_std_time_service_2/math.sqrt(num_rodadas)]
    plt.errorbar(means,['X2','L X2'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Tempo médio de serviço de dados")
    plt.show()

    plt.figure()
    means = [mean_time_wait_1,l_mean_time_wait_1]
    errs = [percentil_90*std_time_wait_1/math.sqrt(num_rodadas),percentil_90*l_std_time_wait_1/math.sqrt(num_rodadas)]
    plt.errorbar(means,['W1','L W1'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Tempo médio de espera de voz")
    plt.show()

    plt.figure()
    means = [mean_time_wait_2,l_mean_time_wait_2]
    errs = [percentil_90*std_time_wait_2/math.sqrt(num_rodadas),percentil_90*l_std_time_wait_2/math.sqrt(num_rodadas)]
    plt.errorbar(means,['W2','L W2'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Tempo médio de espera de dados")
    plt.show()

    plt.figure()
    means = [mean_queue_count_1,l_mean_queue_count_1]
    errs = [percentil_90*std_queue_count_1/math.sqrt(num_rodadas),percentil_90*l_std_queue_count_1/math.sqrt(num_rodadas)]
    plt.errorbar(means,['Nq1','L Nq1'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Número médio de pacotes de voz em espera")
    plt.show()

    plt.figure()
    means = [mean_queue_count_2,l_mean_queue_count_2]
    errs = [percentil_90*std_queue_count_2/math.sqrt(num_rodadas),percentil_90*l_std_queue_count_2/math.sqrt(num_rodadas)]
    plt.errorbar(means,['Nq2','L Nq2'],xerr=errs,fmt='o')
    plt.title("Intervalo de confiança - Número médio de pacotes de dados em espera")
    plt.show()
