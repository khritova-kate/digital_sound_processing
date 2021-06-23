from scipy.fftpack import irfft
from scipy.fftpack import rfft
import librosa
import librosa.display
import IPython.display as ipd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
    
# Задание 3: Построение спектрограммы

'''
Построение спектрограммы
Вход:  sound_tser    - звуковой временной ряд в качестве массива numpy
       windows_n     - количесвто окон
Выход: spectrogram   - двумерный numpy массив со значениями амплитуд (после преобразования Фурье)
       windows_shape - размер окна
'''
def make_spectrogram(sound_tser, windows_n):
    N   = sound_tser.shape[0]
    N   = N - N%windows_n
    windows_shape  = N//windows_n   
    spectrogram = np.empty((windows_n, windows_shape), float)
    for i in range(windows_n):
        start = windows_shape*i
        stop = start + windows_shape
        spectrogram[i] = np.abs(rfft(sound_tser[start:stop]))
    print("sound time series length: {}".format(len(sound_tser)))
    print("spectrogram shape: {}".format(spectrogram.shape))
    return spectrogram, windows_shape

'''
Логарифмическая нормировка массива
'''
def norm_log(array):
    return 10*np.log10(array + 1e-14)
'''
Рисование спектрограммы
Рисование спектрограммы производится с помощью функции matplotlib.pyplot.imshow(). Вдоль вертикальной оси откладывается
значение частоты, вдоль горизонтальной - время. Цветом каждой точки изображения обозначена амплитуда
Вход:  spectrogram    - двумерный numpy массив со значениями амплитуд (после преобразования Фурье)
       sample_rate    - частота дискретизации
       windows_shape  - размер окна
       oud_tser_shape - длина звукового временного ряда в качестве массива numpy
       windows_n      - количесвто окон
Выход: spectrogram    - двумерный numpy массив со значениями амплитуд (после преобразования Фурье)
       windows_shape  - размер окна
'''
def plot_spectrogramm (spectrogram, sample_rate, windows_shape, sound_tser_shape, windows_n):
    #plt.style.use('ggplot') 
    spectrogram = norm_log(spectrogram)
    
    plt.figure(figsize = (20, 8))
    plt.title("Spectrogram") 
    plt.gca().set_facecolor((0.9, 0.9, 0.9))                                           # цвет фона
    plt_spec = plt.imshow(spectrogram, origin = 'lower', cmap = 'twilight')            # спектрограмма
   
    ## подписываем ось y
    y_dash_n = 5                                                                       # количество делений на оси
    y_ticks  = np.linspace (0, spectrogram.shape[0], y_dash_n)                         # положение делений - номер
    y_labels = [int(sample_rate*pos/windows_shape) for pos in y_ticks]                 # метки делений - частота
    plt.yticks (y_ticks, y_labels)                                                     # установить текущие положения делений и метки оси Y
    plt.ylabel ("Hz")
    
    ## подписываем ось x
    x_dash_n = 5
    signal_duration = sound_tser_shape / sample_rate                                   # продолжительность временного ряда в секундах                  
    x_ticks = np.linspace (0, spectrogram.shape[1], x_dash_n)                          # положение делений - номер  
    end_x_label = signal_duration*windows_shape*windows_n/sound_tser_shape 
    x_labels  = [round(i,3) for i in np.linspace(0, end_x_label , x_dash_n)]           # метки делений - время
    plt.xticks(x_ticks,x_labels)                                                       # установить текущие положения делений и метки оси X
    plt.xlabel("sec")
    
    mappable = None
    plt.colorbar (mappable, use_gridspec = True)