import numpy as np
import math
import pandas as pd
import cloudpickle
import pickle
import streamlit as st

try:
    
    st.title('HDD project calculator')
    #bent = st.checkbox('base bentonite')
    #col1, col2 = st.columns(2)
    with open('d.pkl', 'rb') as f:
        d = pickle.load(f)
        ddf = pickle.loads(d)
    df = ddf()
    #pac = col1.number_input('PAC', min_value = 2.0, value = 4.0, step = 0.1)
    #flom = col1.number_input('Flomin', min_value = 0.2, value = 0.4, step = 0.01)
    #pac = float(input('Кнцентрация PAC: '))
    #flom = float(input('Концентрация Flomin: '))
    rates = {'Мини до 100 кН':1, 'Миди 100 - 400 кН':2, 'Макси 400 - 2500 кН':3, 'Мега > 2500 кН':4}
    n11 = st.checkbox('Задать максимальную тяговую силу установки')
    F = 1
    if n11:
        force = st.selectbox('Установка ', list(rates))
        F = rates[force]
    z = 1
    if F==3 or F==4:
        zd = {'винтовой забойный двигатель':2, 'гидромонитор':1}
        zd_1 = st.selectbox('Тип забойного двигателя: ', list(zd))
        z = zd[zd_1] 
    rates_1 = {'Стальной':1, 'Полиэтиленовые трубы':2}
    n12 = st.checkbox('Задать материал трубопровода')
    sig = 0.1
    if n12:
        mat = st.selectbox('Материал трубопровода ', list(rates_1))
        if rates_1[mat] == 1:
            sig = 0.1
        else:
            sig = 0.05
    
    rates_2 = {'мягкие породы':1, 'породы средней прочности':2, 'твердые и крепкие породы':3}
    n13 = st.checkbox('Выбрать твердость горных пород')
    tvv = 1
    if n13:
        tverd = st.selectbox('Тип горных пород: ', list(rates_2))
        tv = rates_2[tverd]
        if tv == 1:
            v_1 = {'пески, супеси (без гальки), торф, растит слой':1, 'поастичные глины, ил':2, 'плотные супеси, суглинки':3, 'глины тугопластичные, плывуны':4, 'песчано-глинистые породы с мелкой галькой (до 3 см)':5, 'глины с прослоями песчаника и мергеля':6}
            vs_1 = st.selectbox('Описание породы: ', list(v_1))
            tvv = int(v_1[vs_1])
            print(tvv)
        elif tv == 2:
            v_1 = {'водоносный песок и торф':7, 'песчаник глинистыйй, алевролиты':8, 'глины твердые':9, 'крупнозернистый песок, песчаные глины, доломиты':10, 'галечник песчаный или глинистый':11, 'галечно-шебенистые породы':12}
            vs_1 = st.selectbox('Описание породы: ', list(v_1))
            tvv = int(v_1[vs_1])
        else:
            v_1 = {'песчанистый известняк':13, 'ангидриты и плотные доломиты':14, 'плотные доломитовые глины':15, 'песчано-глинистые породы с галькой (до 50 %)':16, 'Кремнистые аргиллиты, базальты':17, 'Валунно-галечные отложения':18}
            vs_1 = st.selectbox('Описание породы: ', list(v_1))
            tvv = int(v_1[vs_1])
    n2 = st.checkbox('Добавить расширитель_1')
    ut = []
    if n2:
        num0 = []
        a11 = st.number_input('Расширитель_1', min_value = 100, max_value = 1200, value = 100, step = 100)
        num0.append(a11)
        ut.append(float(st.number_input(f'Уточнить скорость протягивания расширителя_1 {num0[0]} мм, м/мин', min_value = 0.2, max_value = 1.5, value = 0.5, step = 0.1)))
        n21 = st.checkbox('Добавить расширитель_2')
        if n21:
            num0.append(st.number_input('Расширитель_2', min_value = 100, max_value = 1200, value = 100, step = 100))
            ut.append(float(st.number_input(f'Уточнить скорость протягивания расширителя_2 {num0[1]} мм, м/мин', min_value = 0.2, max_value = 1.5, value = 0.5, step = 0.1)))
            n22 = st.checkbox('Добавить расширитель_3')
            if n22:
                num0.append(st.number_input('Расширитель_3', min_value = 100, max_value = 1200, value = 100, step = 100))
                ut.append(float(st.number_input(f'Уточнить скорость протягивания расширителя_3 {num0[2]} мм, м/мин', min_value = 0.2, max_value = 1.5, value = 0.5, step = 0.1)))
                n23 = st.checkbox('Добавить расширитель_4')
                if n23:
                    num0.append(st.number_input('Горизонт_4', min_value = 100, max_value = 1200, value = 100, step = 100))
                    ut.append(float(st.number_input(f'Уточнить скорость протягивания расширителя_4 {num0[3]} мм, м/мин', min_value = 0.2, max_value = 1.5, value = 0.5, step = 0.1)))
                    n24 = st.checkbox('Добавить расширитель_5')    
                    if n24:
                        num0.append(st.number_input('Расширитель_5', min_value = 100, max_value = 1200, value = 100, step = 100))
                        ut.append(float(st.number_input(f'Уточнить скорость протягивания расширителя_5 {num0[4]} мм, м/мин', min_value = 0.2, max_value = 1.5, value = 0.5, step = 0.1)))
                        n25 = st.checkbox('Добавить горизонт_6')
                        if n25:
                            num0.append(st.number_input('Расширитель_6', min_value = 100, max_value = 1200, value = 100, step = 100))
                            ut.append(float(st.number_input(f'Уточнить скорость протягивания расширителя_6 {num0[5]} мм, м/мин', min_value = 0.2, max_value = 1.5, value = 0.5, step = 0.1)))
                            n26 = st.checkbox('Добавить расширитель_7')
                            if n26:
                                num0.append(st.number_input('Расширитель_7', min_value = 100, max_value = 1200, value = 100, step = 100))
                                ut.append(float(st.number_input(f'Уточнить скорость протягивания расширителя_7 {num0[6]} мм, м/мин', min_value = 0.2, max_value = 1.5, value = 0.5, step = 0.1)))
    else:
        num0 = [100]
    
    L = float(st.number_input('Расчетная длина скважины по профилю, м', min_value = 5, max_value = 5000, value = 5, step = 5))
    n3 = st.checkbox('Добавить расчет расхода материалов')
    ww = 1
    mm = 1
    if n3:
        ww = 1
        w = {'базовый Альбрехта-CV':1, 'низковязкий Альбрехта-LV':2, 'средневязкий Альбрехта-MV':3, 'высоковязкий Альбрехта-HV':4}
        w_1 = st.selectbox('Выбор бентопорошка: ', list(w))
        ww = w[w_1]
        mm = 1
        m = {'Минимальный расход реагентов':1, 'средний расход реагентов':2, 'максимальный расход реагентов':3}
        m_1 = st.selectbox('Выбор категории расхода материалов: ', list(m))
        mm = m[m_1]    
    r = st.checkbox('Показывать рецептуру раствора')
    rr = st.checkbox('Показывать технологические свойства раствора')
    
    if F==1 or F==2:
        Vn = float(st.number_input('Объем смесителя, м3', min_value = 2, max_value = 10, value = 2, step = 1))
        if st.button('Объем раствора и расход реагентов'):
            V = 0.785*0.001*0.001*max(num0)*max(num0)*(L+sig)*df.loc[df['num']==tvv, 'F'][tvv-1] + Vn
            st.success(f'Объем приготовленного раствора: {V:,.1f} м3')
            if ww == 1:
                if mm == 1:
                    soda = V * df.loc[df['num']==tvv, 'soda_min'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_min'][tvv-1] 
                    paa = V * df.loc[df['num']==tvv, 'paa_min'][tvv-1] 
                    pac = V * df.loc[df['num']==tvv, 'pac_min'][tvv-1] 
                    xc = V * df.loc[df['num']==tvv, 'xc_min'][tvv-1] 
                    lub = V * df.loc[df['num']==tvv, 'lub_min'][tvv-1]
                        
                elif mm == 2:
                    soda = V * df.loc[df['num']==tvv, 'soda_c'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_c'][tvv-1] 
                    paa = V * df.loc[df['num']==tvv, 'paa_c'][tvv-1] 
                    pac = V * df.loc[df['num']==tvv, 'pac_c'][tvv-1] 
                    xc = V * df.loc[df['num']==tvv, 'xc_c'][tvv-1] 
                    lub = V * df.loc[df['num']==tvv, 'lub_c'][tvv-1]
                    
                else:
                    soda = V * df.loc[df['num']==tvv, 'soda_max'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_max'][tvv-1] 
                    paa = V * df.loc[df['num']==tvv, 'paa_max'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_max'][tvv-1] 
                    xc = V * df.loc[df['num']==tvv, 'xc_max'][tvv-1] 
                    lub = V * df.loc[df['num']==tvv, 'lub_max'][tvv-1]
                    
            elif ww == 2:
                if mm == 1:
                    soda = V * df.loc[df['num']==tvv, 'soda_min'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_min'][tvv-1] * 0.7
                    paa = V * df.loc[df['num']==tvv, 'paa_min'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_min'][tvv-1] * 0.8
                    xc = V * df.loc[df['num']==tvv, 'xc_min'][tvv-1] * 0.9
                    lub = V * df.loc[df['num']==tvv, 'lub_min'][tvv-1]
                   
                elif mm == 2:
                    soda = V * df.loc[df['num']==tvv, 'soda_c'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_c'][tvv-1] * 0.7
                    paa = V * df.loc[df['num']==tvv, 'paa_c'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_c'][tvv-1] * 0.8
                    xc = V * df.loc[df['num']==tvv, 'xc_c'][tvv-1] * 0.9
                    lub = V * df.loc[df['num']==tvv, 'lub_c'][tvv-1]
                   
                else:
                    soda = V * df.loc[df['num']==tvv, 'soda_max'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_max'][tvv-1] * 0.7
                    paa = V * df.loc[df['num']==tvv, 'paa_max'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_max'][tvv-1] * 0.8
                    xc = V * df.loc[df['num']==tvv, 'xc_max'][tvv-1] * 0.9
                    lub = V * df.loc[df['num']==tvv, 'lub_max'][tvv-1]
                    
            elif ww == 3:
                if mm == 1:
                    soda = V * df.loc[df['num']==tvv, 'soda_min'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_min'][tvv-1] * 0.5
                    paa = V * df.loc[df['num']==tvv, 'paa_min'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_min'][tvv-1] * 0.6
                    xc = V * df.loc[df['num']==tvv, 'xc_min'][tvv-1] * 0.8
                    lub = V * df.loc[df['num']==tvv, 'lub_min'][tvv-1]
                    
                elif mm == 2:
                    soda = V * df.loc[df['num']==tvv, 'soda_c'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_c'][tvv-1] * 0.5
                    paa = V * df.loc[df['num']==tvv, 'paa_c'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_c'][tvv-1] * 0.6
                    xc = V * df.loc[df['num']==tvv, 'xc_c'][tvv-1] * 0.8
                    lub = V * df.loc[df['num']==tvv, 'lub_c'][tvv-1]
                    
                else:
                    soda = V * df.loc[df['num']==tvv, 'soda_max'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_max'][tvv-1] * 0.5
                    paa = V * df.loc[df['num']==tvv, 'paa_max'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_max'][tvv-1] * 0.6
                    xc = V * df.loc[df['num']==tvv, 'xc_max'][tvv-1] * 0.8
                    lub = V * df.loc[df['num']==tvv, 'lub_max'][tvv-1]
                    
            elif ww == 4:
                if mm == 1:
                    soda = V * df.loc[df['num']==tvv, 'soda_min'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_min'][tvv-1] * 0.4
                    paa = V * df.loc[df['num']==tvv, 'paa_min'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_min'][tvv-1] * 0.5
                    xc = V * df.loc[df['num']==tvv, 'xc_min'][tvv-1] * 0.7
                    lub = V * df.loc[df['num']==tvv, 'lub_min'][tvv-1]
                    
                elif mm == 2:
                    soda = V * df.loc[df['num']==tvv, 'soda_c'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_c'][tvv-1] * 0.4
                    paa = V * df.loc[df['num']==tvv, 'paa_c'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_c'][tvv-1] * 0.5
                    xc = V * df.loc[df['num']==tvv, 'xc_c'][tvv-1] * 0.7
                    lub = V * df.loc[df['num']==tvv, 'lub_c'][tvv-1]
                    
                else:
                    soda = V * df.loc[df['num']==tvv, 'soda_max'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_max'][tvv-1] * 0.4
                    paa = V * df.loc[df['num']==tvv, 'paa_max'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_max'][tvv-1] * 0.5
                    xc = V * df.loc[df['num']==tvv, 'xc_max'][tvv-1] * 0.7
                    lub = V * df.loc[df['num']==tvv, 'lub_max'][tvv-1]
    
            if n3:
                st.write('Общий расход реагентов и материалов, кг:')
                st.warning(f'Расход соды: {soda:,.1f}')
                st.warning(f'Расход бентонита: {bent:,.1f}')
                st.warning(f'Расход полиакриламида: {paa:,.1f}')
                st.warning(f'Расход ПАЦ: {pac:,.1f}')
                st.warning(f'Расход ксантана: {xc:,.1f}')
                st.warning(f'Расход смазки: {lub:,.1f}')
            
            if r:
                st.write('Рецептура бурового раствора, кг/м3:')
                st.success(f'Сода: {soda/V:,.2f}')
                st.success(f'Бентонит: {bent/V:,.2f}')
                st.success(f'ПАА: {paa/V:,.2f}')
                st.success(f'ПАЦ: {pac/V:,.2f}')
                st.success(f'Ксантан: {xc/V:,.2f}')
                st.success(f'Смазка: {lub/V:,.2f}')
            if rr:
                st.write('Технологические свойства раствора:')
                T = df.loc[df['num']==tvv, 'T'][tvv-1]
                gel = df.loc[df['num']==tvv, 'gel'][tvv-1]
                yp = df.loc[df['num']==tvv, 'yp'][tvv-1]
                st.success(f'Условная вязкость: {T} сек')
                st.success(f'СНС 1 min: {gel} Фунт/100Фут2')
                st.success(f'ДНС: {yp} Фунт/100Фут2')
    else:
        Vn = float(st.number_input('Объем смесителя, м3', min_value = 10, max_value = 60, value = 10, step = 2))
        rs = st.checkbox('Разбить объем раствора по расширителям')
        if st.button('Объем раствора и расход реагентов'):
            
            if z == 1:
                u = df.loc[df['num']==tvv, 'pil_gm'][tvv-1]
                if L <= 300:
                    Q = 0.2
                elif L > 300 and L <= 500:
                    Q = 0.3
                elif L > 500 and  L <= 1000:
                    Q = 0.5
                elif L > 1000 and L <= 1500:
                    Q = 0.7
                else:
                    Q = 1
            else:
                u = df.loc[df['num']==tvv, 'pil_vint'][tvv-1]
                if L <= 300:
                    Q = 0.7
                elif L > 300 and L <= 500:
                    Q = 0.8
                elif L > 500 and  L <= 1000:
                    Q = 1
                elif L > 1000 and L <= 1500:
                    Q = 1.5
                else:
                    Q = 2
            Vp = (Q/u)*60*(L+sig)*1.2
            Vr = []
            Vk = []
            Vt = []
            for i in range(len(num0)):
                tr = (L+sig)/(60*ut[i])
                Vr.append(60*tr*num0[i]*0.001*1.2)
                Vk.append((num0[i]*0.001/(3*ut[i]*60))*60*(L+sig)*1.2)
                Vt.append((num0[i]*0.001/(3*60))*60*(L+sig)*1.2)
                V = Vn + Vp + sum(Vr) + sum(Vk) + Vt[-1]
            st.success(f'Общий объем приготовленного раствора: {(Vn + Vp + sum(Vr) + sum(Vk) + Vt[-1]):,.1f} м3')
            if rs:
                st.warning(f'Объем раствора на пилотный ствол: {Vp:,.1f} м3')
                st.warning(f'Объем раствора на затяжку: {Vt[-1]:,.1f} м3')
                for i in range(len(num0)):
                    st.warning(f'Объем раствора на расширение {num0[i]} мм: {(Vr[i] + Vk[i]):,.1f} м3')
            if ww == 1:
                if mm == 1:
                    soda = V * df.loc[df['num']==tvv, 'soda_min'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_min'][tvv-1] 
                    paa = V * df.loc[df['num']==tvv, 'paa_min'][tvv-1] 
                    pac = V * df.loc[df['num']==tvv, 'pac_min'][tvv-1] 
                    xc = V * df.loc[df['num']==tvv, 'xc_min'][tvv-1] 
                    lub = V * df.loc[df['num']==tvv, 'lub_min'][tvv-1]
                        
                elif mm == 2:
                    soda = V * df.loc[df['num']==tvv, 'soda_c'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_c'][tvv-1] 
                    paa = V * df.loc[df['num']==tvv, 'paa_c'][tvv-1] 
                    pac = V * df.loc[df['num']==tvv, 'pac_c'][tvv-1] 
                    xc = V * df.loc[df['num']==tvv, 'xc_c'][tvv-1] 
                    lub = V * df.loc[df['num']==tvv, 'lub_c'][tvv-1]
                    
                else:
                    soda = V * df.loc[df['num']==tvv, 'soda_max'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_max'][tvv-1] 
                    paa = V * df.loc[df['num']==tvv, 'paa_max'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_max'][tvv-1] 
                    xc = V * df.loc[df['num']==tvv, 'xc_max'][tvv-1] 
                    lub = V * df.loc[df['num']==tvv, 'lub_max'][tvv-1]
                    
            elif ww == 2:
                if mm == 1:
                    soda = V * df.loc[df['num']==tvv, 'soda_min'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_min'][tvv-1] * 0.7
                    paa = V * df.loc[df['num']==tvv, 'paa_min'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_min'][tvv-1] * 0.8
                    xc = V * df.loc[df['num']==tvv, 'xc_min'][tvv-1] * 0.9
                    lub = V * df.loc[df['num']==tvv, 'lub_min'][tvv-1]
                   
                elif mm == 2:
                    soda = V * df.loc[df['num']==tvv, 'soda_c'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_c'][tvv-1] * 0.7
                    paa = V * df.loc[df['num']==tvv, 'paa_c'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_c'][tvv-1] * 0.8
                    xc = V * df.loc[df['num']==tvv, 'xc_c'][tvv-1] * 0.9
                    lub = V * df.loc[df['num']==tvv, 'lub_c'][tvv-1]
                   
                else:
                    soda = V * df.loc[df['num']==tvv, 'soda_max'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_max'][tvv-1] * 0.7
                    paa = V * df.loc[df['num']==tvv, 'paa_max'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_max'][tvv-1] * 0.8
                    xc = V * df.loc[df['num']==tvv, 'xc_max'][tvv-1] * 0.9
                    lub = V * df.loc[df['num']==tvv, 'lub_max'][tvv-1]
                    
            elif ww == 3:
                if mm == 1:
                    soda = V * df.loc[df['num']==tvv, 'soda_min'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_min'][tvv-1] * 0.5
                    paa = V * df.loc[df['num']==tvv, 'paa_min'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_min'][tvv-1] * 0.6
                    xc = V * df.loc[df['num']==tvv, 'xc_min'][tvv-1] * 0.8
                    lub = V * df.loc[df['num']==tvv, 'lub_min'][tvv-1]
                    
                elif mm == 2:
                    soda = V * df.loc[df['num']==tvv, 'soda_c'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_c'][tvv-1] * 0.5
                    paa = V * df.loc[df['num']==tvv, 'paa_c'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_c'][tvv-1] * 0.6
                    xc = V * df.loc[df['num']==tvv, 'xc_c'][tvv-1] * 0.8
                    lub = V * df.loc[df['num']==tvv, 'lub_c'][tvv-1]
                    
                else:
                    soda = V * df.loc[df['num']==tvv, 'soda_max'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_max'][tvv-1] * 0.5
                    paa = V * df.loc[df['num']==tvv, 'paa_max'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_max'][tvv-1] * 0.6
                    xc = V * df.loc[df['num']==tvv, 'xc_max'][tvv-1] * 0.8
                    lub = V * df.loc[df['num']==tvv, 'lub_max'][tvv-1]
                    
            elif ww == 4:
                if mm == 1:
                    soda = V * df.loc[df['num']==tvv, 'soda_min'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_min'][tvv-1] * 0.4
                    paa = V * df.loc[df['num']==tvv, 'paa_min'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_min'][tvv-1] * 0.5
                    xc = V * df.loc[df['num']==tvv, 'xc_min'][tvv-1] * 0.7
                    lub = V * df.loc[df['num']==tvv, 'lub_min'][tvv-1]
                    
                elif mm == 2:
                    soda = V * df.loc[df['num']==tvv, 'soda_c'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_c'][tvv-1] * 0.4
                    paa = V * df.loc[df['num']==tvv, 'paa_c'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_c'][tvv-1] * 0.5
                    xc = V * df.loc[df['num']==tvv, 'xc_c'][tvv-1] * 0.7
                    lub = V * df.loc[df['num']==tvv, 'lub_c'][tvv-1]
                    
                else:
                    soda = V * df.loc[df['num']==tvv, 'soda_max'][tvv-1]
                    bent = V * df.loc[df['num']==tvv, 'cv_max'][tvv-1] * 0.4
                    paa = V * df.loc[df['num']==tvv, 'paa_max'][tvv-1]
                    pac = V * df.loc[df['num']==tvv, 'pac_max'][tvv-1] * 0.5
                    xc = V * df.loc[df['num']==tvv, 'xc_max'][tvv-1] * 0.7
                    lub = V * df.loc[df['num']==tvv, 'lub_max'][tvv-1]
    
            if n3:
                st.write('Общий расход реагентов и материалов, кг:')
                st.warning(f'Расход соды: {soda:,.1f}')
                st.warning(f'Расход бентонита: {bent:,.1f}')
                st.warning(f'Расход полиакриламида: {paa:,.1f}')
                st.warning(f'Расход ПАЦ: {pac:,.1f}')
                st.warning(f'Расход ксантана: {xc:,.1f}')
                st.warning(f'Расход смазки: {lub:,.1f}')
            
            if r:
                st.write('Рецептура бурового раствора, кг/м3:')
                st.success(f'Сода: {soda/V:,.2f}')
                st.success(f'Бентонит: {bent/V:,.2f}')
                st.success(f'ПАА: {paa/V:,.2f}')
                st.success(f'ПАЦ: {pac/V:,.2f}')
                st.success(f'Ксантан: {xc/V:,.2f}')
                st.success(f'Смазка: {lub/V:,.2f}')
            if rr:
                st.write('Технологические свойства раствора:')
                T = df.loc[df['num']==tvv, 'T'][tvv-1]
                gel = df.loc[df['num']==tvv, 'gel'][tvv-1]
                yp = df.loc[df['num']==tvv, 'yp'][tvv-1]
                st.success(f'Условная вязкость: {T} сек')
                st.success(f'СНС 1 min: {gel} Фунт/100Фут2')
                st.success(f'ДНС: {yp} Фунт/100Фут2')

except:
    st.error("Ошибка ввода данных")
 
       





