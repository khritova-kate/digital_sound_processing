import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from scipy.ndimage import gaussian_filter1d

# Задание 7. Выделение гармоники.

### Сглаживание функций

# по сейсмо-разведчески :)
'''
Сглаживание функции путем оконного среднего: элемент массива заменяется на среднее
значение для окна с центром в этом элементе
Вход:  array   - массив для обработки
       box_len - размер окна
Выход: массив с усредненными значениями
'''
def smoothing_mean(array, box_len = 9):
    if box_len%2 == 0:
        box_len = box_len + 1
    half_box_len = box_len//2
    array_len = len(array)
    smoothed_array = np.zeros(array_len,float)
    for i in range(len(array)):
        start = max(0, i-half_box_len)
        stop  = min(array_len, i+half_box_len+1)
        smoothed_array[i] = np.mean(array[start:stop])
    return  smoothed_array
'''
Сглаживание функции путем взвешенного оконного среднего: элемент массива заменяется на 
взвешенное среднее значение для окна с центром в этом элементе, вес определяется
расстоянием до элемента - чем ближе, тем больше
Вход:  array   - массив для обработки
       box_len - размер окна
Выход: массив с усредненными значениями
'''
def get_weights(half_box_len):
    weights = np.linspace(0.1, 1, half_box_len+1)
    return weights
def smoothing_mean_w(array, box_len = 9):
    if box_len%2 == 0:
        box_len = box_len + 1
    half_box_len = box_len//2
    array_len = len(array)
    # веса
    weights = get_weights(half_box_len)
    smoothed_array = np.zeros(array_len,float)
    for i in range(len(array)):
        # считаем взвешенное среднее в окошке
        real_box_len = 1
        for j in range(half_box_len):
            delta = half_box_len - j
            w = weights[j]
            if i - delta >= 0:
                smoothed_array[i] = smoothed_array[i] + array[i - delta]*w
                real_box_len = real_box_len + 1
            if i + delta < array_len:
                smoothed_array[i] = smoothed_array[i] + array[i + delta]*w
                real_box_len = real_box_len + 1
        smoothed_array[i] = smoothed_array[i] + array[i]
        smoothed_array[i] = smoothed_array[i] / real_box_len
    return  smoothed_array

'''
Сглаживание с помощью библиотечной функции scipy.ndimage.gaussian_filter1d
'''
def gaussian_filter(array, sigma = 2):
    return gaussian_filter1d(array, sigma)
'''
Без сглаживания
'''
def without_smothing(array):
    return array

### Гармоники

'''
Возвращает True если элементы массива array неубывают
'''
def increasing(array):
    increasing = True
    for i in range(1,len(array)):
        increasing = increasing * (not array[i] < array[i-1])
    return bool(increasing)
'''
Возвращает True если элементы массива array невозрастают
'''
def decreasing(array):
    decreasing = True
    for i in range(1,len(array)):
        decreasing = decreasing * (not array[i] > array[i-1])
    return bool(decreasing)
'''
Находит все локальные пики и соответсвующие им позиции
Вход:  window_smoothed - массив значений, полученный после применения одного из
                         методов сглаживания к окну
       box_len         - диаметр окрестности, в которой ищем пик; хотим отличать
                         пик от выброса - пусть в рассмотренной окрестности 
                         функция неубывает до пика и невозрастает после
Выход: loc_max         - все локальные пики
       loc_max_pos     - номера элементов, соответсующих локальным пикам
'''
def find_local_max(window_smoothed, box_len = 5):
    loc_max = []
    loc_max_pos = []
    if box_len%2 == 0:
        box_len = box_len + 1
    half_box_len = box_len//2
    array_len = len(window_smoothed)
    for i in range(array_len):
        start = max(0, i-half_box_len)
        stop  = min(array_len, i+half_box_len+1)
        cur_n = i
        if increasing(window_smoothed[start:i+1]) and decreasing(window_smoothed[i:stop]):
            loc_max.append(window_smoothed[i])
            loc_max_pos.append(i)
    return loc_max, loc_max_pos
'''
Выделение первых трех (по умолчанию) гармоник
Вход:  sample_rate - частота дискретизации
       spectrogram - спектрограмма
       number_of_harmonics - число гармоник
Выход: двумерный массив с гармониками для каждого окна
'''
def find_harmonics(sample_rate, spectrogram, number_of_harmonics = 3,\
                   smoothing_function = without_smothing, extra_freq = 6000, locmax_box_len = 3):
    windows_n     = spectrogram.shape[0]
    windows_shape = spectrogram.shape[1]
    harmonics = np.zeros((number_of_harmonics, windows_n))
    for i in range(windows_n):
        window = spectrogram[i]
        window_smoothed = smoothing_function(window)
        loc_max, loc_max_pos = find_local_max(window_smoothed, locmax_box_len)
        for hn in range(number_of_harmonics):
            pos = np.argmax(loc_max)
            loc_max[pos] = 0.0
            harmonics[hn][i] = loc_max_pos[pos]*sample_rate/windows_shape
            if  harmonics[hn][i] > extra_freq and (i > 0 and i < windows_n-1):
                harmonics[hn][i]= (harmonics[hn][i+1] + harmonics[hn][i-1])/2 
    for hn in range(number_of_harmonics):
        if  harmonics[hn][0] > extra_freq:
            harmonics[hn][0] = harmonics[hn][1]
        if  harmonics[hn][-1] > extra_freq:
            harmonics[hn][-1] = harmonics[hn][-2]
    return harmonics


### Рисование

'''
Изображение зависимости гармоники, от номера окна
Вход:  harmonic - гармоника
       numder_h - номер гармоники (1,2 или 3)
       sound_tser_shape - длина numpy массива звукового временного ряда
       sample_rate - частота дискретизации
       windows_shape - размер окна
       windows_n - количество окон
Выход: ---
'''
def plot_harmonic(harmonic, numder_h, sound_tser_shape, sample_rate, windows_shape, windows_n):
    plt.figure (figsize = (20, 8))
    plt.title("Harmonic №{}".format(numder_h+1))
    plt.plot(harmonic)
    
    ## подписываем ось x
    x_dash_n = 7
    signal_duration = sound_tser_shape / sample_rate                                   # продолжительность временного ряда в секундах                  
    x_ticks = np.linspace (0, windows_n, x_dash_n)                                     # положение делений - номер  
    end_x_label = signal_duration*windows_shape*windows_n/sound_tser_shape 
    x_labels  = [round(i,3) for i in np.linspace(0, end_x_label , x_dash_n)]           # метки делений - время
    plt.xticks(x_ticks,x_labels)                                                       # установить текущие положения делений и метки оси X
    plt.xlabel("sec")
    
    ## подписываем ось y
    plt.ylabel ("Hz")