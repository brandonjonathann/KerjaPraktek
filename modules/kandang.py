import os
import pandas as pd

def list_kandang():
    kandang = os.listdir(f'database/')
    kandang.sort(key = lambda x: int(x[1:]))
    return kandang

def data_kandang(kandang: str):
    path = f'database/{kandang}'
    csv_dataframe = pd.read_csv(path, header = None)
    
    data_kandang = []
    for row_index, row in csv_dataframe.iterrows():
        """
        0: produksi telur siang
        1: produksi telur sore
        2: produksi telur total
        3: total double
        4: jumlah betina mati
        5: jumlah jantan mati
        6: jumlah betina B mati
        7: jumlah jantan B mati
        8: jumlah seleksi error mati
        9: pakan betina
        10: pakan jantan
        11: pakan betina B
        12: pakan jantan B
        13: pakan seleksi error
        14: hitungan pakan betina
        15: hitungan pakan jantan
        16: hitungan pakan betina B
        17: hitungan pakan jantan B
        18: hitungan pakan seleksi error
        19: vaksin
        """
        data_hari = []
        data_hari.append(jumlah_telur(row[2], row[3], row[4], row[5]))
        data_hari.append(jumlah_telur(row[2], row[7], row[8], row[9]))
        data_hari.append(data_hari[0] + data_hari[1])
        data_hari.append(row[6] + row[10])
        data_hari.append(row[11])
        data_hari.append(row[12])
        data_hari.append(row[13])
        data_hari.append(row[14])
        data_hari.append(row[15])
        data_hari.append(jumlah_pakan(row[16], row[21]))
        data_hari.append(jumlah_pakan(row[17], row[22]))
        data_hari.append(jumlah_pakan(row[18], row[23]))
        data_hari.append(jumlah_pakan(row[19], row[24]))
        data_hari.append(jumlah_pakan(row[20], row[25]))
        data_hari.append(hitungan_pakan(row[26], row[31]))
        data_hari.append(hitungan_pakan(row[27], row[32]))
        data_hari.append(hitungan_pakan(row[28], row[33]))
        data_hari.append(hitungan_pakan(row[29], row[34]))
        data_hari.append(hitungan_pakan(row[30], row[35]))
        data_hari.append(row[36])
        data_kandang.append(data_hari)
    return data_kandang

def jumlah_telur(jenis: str, ikat: int, eggtray: int, butir: int):
    total = 0
    if jenis == 'Karton':
        eggtray = 8 * ikat + eggtray
        total = 30 * eggtray + butir    
    elif jenis == 'Plastik':
        eggtray = 6 * ikat + eggtray
        total = 36 * eggtray + butir  
    else:
        eggtray = 5 * ikat + eggtray
        total = 42 * eggtray + butir 
    return total 

def jumlah_pakan(karung: int, kg: float):
    return karung * 60 + kg

def hitungan_pakan(ekor: int, spf: float):
    return ekor * spf

print(data_kandang('R9'))