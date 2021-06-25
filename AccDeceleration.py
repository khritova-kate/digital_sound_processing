import numpy as np


'''
Ускорение/змедление воспроизведения путем удаления/повторения
элементов массива, соответсвующего звуковому временному ряду
Вход:  sound_tser - звуковой временной ряд в качестве массива numpy
       speed_c - коэффициент ускорения/замедления
Выход: звуковой временной ряд в качестве массива numpy
'''
def speed_up(sound_tser, speed_c):
    stop = int(sound_tser.shape[0]/speed_c)
    ids  = [int(speed_c*i) for i in range(stop)]
    return np.array([sound_tser[i] for i in ids])

def i_to_inew(speed_c, i):
    return int(speed_c*i)
def ab(x1,x2,y1,y2):
    a = (y2-y1)/(x2-x1)
    b = (x2*y1 - x1*y2)/(x2-x1)
    return a,b
    
'''
Замедление воспроизведения не больше чем в 2 раза путем добавления
элементов, равных среднему значению соседей
Вход:  sound_tser - звуковой временной ряд в качестве массива numpy
       speed_c - коэффициент ускорения/замедления
Выход: звуковой временной ряд в качестве массива numpy
'''
def slow_down1(sound_tser, speed_c):
    if speed_c < 1 or speed_c > 2:
        print('incorrect coefficient --- 1.5 now')
        speed_c = 1.5
    stop = sound_tser.shape[0]
    ids_save = [int(speed_c*i) for i in range(stop)]
    saved = set(ids_save)
    ids_new  = []
    for i in range(int(sound_tser.shape[0]*speed_c)):
        if not i in saved:
            ids_new.append(i)
        
    new_len = i_to_inew(speed_c, sound_tser.shape[0])
    res = np.zeros(new_len)
    for i in range(sound_tser.shape[0]):
        res[i_to_inew(i,speed_c)] = sound_tser[i]
    if ids_new[-1] >= new_len-1:
        ids_new = ids_new[:-1]
        res[-1] = res[-2]
    for i in ids_new:
        res[i] = (res[i-1]+res[i+1])/2
    return res
'''
Замедление воспроизведения больше чем в 2 раза путем добавления
элементов, лежащих на прямой линии, проходящей через соседние 
известные значения
Вход:  sound_tser - звуковой временной ряд в качестве массива numpy
       speed_c - коэффициент ускорения/замедления
Выход: звуковой временной ряд в качестве массива numpy
'''
def slow_down2(sound_tser, speed_c):
    stop = sound_tser.shape[0]
    ids_save = [int(speed_c*i) for i in range(stop)]
    saved = set(ids_save)
    ids_new  = []
    for i in range(int(sound_tser.shape[0]*speed_c)):
        if not i in saved:
            ids_new.append(i)

    new_len = ids_save[-1] + 1
    res = np.zeros(new_len)

    for i in range(sound_tser.shape[0]):
        res[i_to_inew(i,speed_c)] = sound_tser[i]

    while ids_new[-1] >= new_len-1:
        ids_new = ids_new[:-1]
    bord_i = 0
    x1 = i_to_inew(bord_i,speed_c)
    x2 = i_to_inew(bord_i+1,speed_c)
    y1 = sound_tser[bord_i]
    y2 = sound_tser[bord_i+1]
    a,b  = ab(x1,x2,y1,y2)
    for i in ids_new:
        if i > x2:
            bord_i = bord_i + 1
            x1 = x2
            x2 = i_to_inew(bord_i+1,speed_c)
            y1 = sound_tser[bord_i]
            y2 = sound_tser[bord_i+1]
            a,b  = ab(x1,x2,y1,y2)
        res[i] = a*i + b
    return res

def slow_down(sound_tser, speed_c):
    if speed_c > 2:
        return slow_down2(sound_tser, speed_c)
    else:
        return slow_down1(sound_tser, speed_c)
