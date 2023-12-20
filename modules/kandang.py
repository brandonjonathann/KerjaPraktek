import os
import pandas as pd
from datetime import datetime

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
        0: tanggal
        1: hari
        2: produksi telur siang
        3: produksi telur sore
        4: produksi telur total
        5: total double
        6: jumlah betina mati
        7: jumlah jantan mati
        8: jumlah betina B mati
        9: jumlah jantan B mati
        10: jumlah seleksi error mati
        11: pakan betina
        12: pakan jantan
        13: pakan betina B
        14: pakan jantan B
        15: pakan seleksi error
        16: hitungan pakan betina
        17: hitungan pakan jantan
        18: hitungan pakan betina B
        19: hitungan pakan jantan B
        20: hitungan pakan seleksi error
        21: jumlah ayam betina
        22: jumlah ayam jantan
        23: jumlah ayam betina B
        24: jumlah ayam jantan B
        25: jumlah ayam seleksi error
        26: keterangan
        27: hari ke-
        28: produksi
        29: mortality
        """
        data_hari = []
        data_hari.append(row[1])
        data_hari.append(hitung_hari(row[1]))
        data_hari.append(jumlah_telur(row[2], row[3], row[4], row[5]))
        data_hari.append(jumlah_telur(row[2], row[7], row[8], row[9]))
        data_hari.append(data_hari[2] + data_hari[3])
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
        data_hari.append(row[26])
        data_hari.append(row[27])
        data_hari.append(row[28])
        data_hari.append(row[29])
        data_hari.append(row[30])
        data_hari.append(row[36])
        data_hari.append(row_index + 1)
        data_hari.append(produksi(data_hari[4], data_hari[21], data_hari[22], data_hari[23], data_hari[24], data_hari[25]))
        data_hari.append(mortalitas(data_hari[6], data_hari[7], data_hari[8], data_hari[9], data_hari[10], data_hari[21], data_hari[22], data_hari[23], data_hari[24], data_hari[25]))
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
    result = round(karung * 60 + kg, 1)
    if result == 0:
        return ''
    else:
        return result

def hitungan_pakan(ekor: int, spf: float):
    result = round(ekor * spf, 1)
    if result == 0:
        return ''
    else:
        return result

def hitung_hari(tanggal: str):
    return datetime.strptime(tanggal, '%m/%d/%Y').strftime('%A')

def produksi(telur, jumlah_betina, jumlah_jantan, jumlah_betina_B, jumlah_jantan_B, jumlah_SE):
    total_ayam = jumlah_betina + jumlah_jantan + jumlah_betina_B + jumlah_jantan_B + jumlah_SE
    total_telur = telur
    return round(total_telur / total_ayam * 100, 1)

def mortalitas(mati_betina, mati_jantan, mati_betina_B, mati_jantan_B, mati_SE, jumlah_betina, jumlah_jantan, jumlah_betina_B, jumlah_jantan_B, jumlah_SE):
    total_ayam = jumlah_betina + jumlah_jantan + jumlah_betina_B + jumlah_jantan_B + jumlah_SE
    total_mati = mati_betina + mati_jantan + mati_betina_B + mati_jantan_B + mati_SE
    return round(total_mati / total_ayam * 100, 1)