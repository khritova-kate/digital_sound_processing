import numpy as np
from scipy.fftpack import irfft
from scipy.fftpack import rfft 

# Задание 5: Фильтр Чебышева

'''
Полиномы Чебышева
''' 
def cheb_function(deg, x):
    if deg == 0:
        return 1
    if deg == 1:
        return x
    f0 = 1
    f1 = x
    for i in range(1,deg,1):
        f = 2*x*f1 - f0
        f0 = f1
        f1 = f
    return f
'''
Kоэффициент передачи (с нормировкой частоты)
'''
def H(W, deg, eps):
    return 1/np.sqrt(1+eps**2*cheb_function(deg, W)**2)
def K(w, w0, deg, eps):
    return H(w/w0, deg, eps)
    
'''
Фильтр Чебышева
Вход: sound_tser   - звуковой временной ряд в качестве массива numpy
      w0           - граничная частота полосы пропускания
      sample_rate  - частота дискретизации
      deg          - степень полинома Чебышева
      eps          - значение eps для коэффициента передачи
Выход: звуковой временной ряд в качестве массива numpy
'''
def chebyshev_noise_filter(sound_tser, w0, sample_rate, deg = 5, eps=0.1):
    sound_tser_w = rfft(sound_tser)                       # прямое преобразование Фурье 
    N     = sound_tser_w.shape[0]
    w_arr = np.linspace(0, sample_rate, N, endpoint=True)
    Kw    = K(w_arr, w0, deg, eps)                        # вычисляем коэффициент передачи
    sound_tser_t    = irfft(sound_tser_w * Kw)            # обратное преоразование Фурье
    return np.abs(sound_tser_t)
