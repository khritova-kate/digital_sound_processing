import librosa
import soundfile as sf
import numpy as np

# Задание 1: чтение аудио-файла

'''
Чтение производится с помощью функции librosa.load()
Вход: имя файла
Выход: sound_tser  - звуковой временной ряд в качестве массива numpy
       sample_rate - частотота дискретизации (по умолчанию 22 кГц моно)
'''
def read_audio(audioFileName):
    sound_tser, sample_rate = librosa.load(audioFileName)
    return sound_tser, sample_rate


# Задание 2: Добавление писка и запись файла

'''
Добавление писка
Вход:  sound_tser  - звуковой временной ряд в качестве массива numpy
       sample_rate - частотота дискретизации (по умолчанию 22 кГц моно)
Выход: ---
'''
def add_noise(sound_tser, sample_rate, f_noise = 15000):                
    signal_duration = len(sound_tser) / sample_rate                                  # продолжительность временного ряда в секундах
    t_arr = np.linspace(0, signal_duration, sound_tser.shape[0], endpoint=False)     # переменная времени
    noise = 0.01*np.sin(2*np.pi*f_noise*t_arr)                                       # чистая синусоидная волна при 15 кГц
    return sound_tser + noise

'''
Запись файла
Для записи файла используется функция soundfile.write()
Вход: out_audioFileName - имя файла для записи
      sound_tser  - звуковой временной ряд в качестве массива numpy
      sample_rate - частотота дискретизации
Выход: ----'''
def write_audio(out_audioFileName, sound_tser, sample_rate):
    sf.write(out_audioFileName, sound_tser, sample_rate)
    print("written to '" + out_audioFileName + "'")
    