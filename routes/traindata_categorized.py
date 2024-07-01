from flask import Blueprint, jsonify
from collections import Counter
from function.obj_converter import call_DatasetCleaned_obj, call_trainingdata_obj
from function.categorize_trainingdata import categorize_text
from models.model import db

traindata = Blueprint('traindata', __name__, template_folder='routes')

@traindata.route("/get-kategori-trainingdata")
def get_kategori():
    data = call_DatasetCleaned_obj()
    
    # Ambil kolom yang berisi kategori
    kategori_column = [row['category'] for row in data]
    
    # Hitung frekuensi setiap kategori
    kategori_counter = Counter(kategori_column)
    
    # Ubah hasil ke format yang bisa dijadikan JSON
    kategori_json = [{"kategori": kategori, "jumlah": jumlah} for kategori, jumlah in kategori_counter.items()]
    # Membuat dictionary yang berisi data asli dan kategori_json
    total = {"datas": data, "categories": kategori_json}
    
    return jsonify(total)

@traindata.route("/get-relevance-data")
def get_relevance():
    data = call_DatasetCleaned_obj()

    # Ambil kolom yang berisi kategori
    kategori_column = [row['category'] for row in data]
    relevansi_column = [row['relevansi'] for row in data]
    tipeakun_column = [row['tipe_akun'] for row in data]

    # Hitung frekuensi setiap kategori
    kategori_counter = Counter(kategori_column)
    relevansi_counter = Counter(relevansi_column)
    tipeakun_counter = Counter(tipeakun_column)

    # Hitung jumlah relevansi dan tidak relevan
    jumlah_relevan = relevansi_counter.get('relevan', 0)
    jumlah_tidak_relevan = relevansi_counter.get('notrelevan', 0)

    # Hitung persentase perbedaan relevansi
    total_data_relevansi = jumlah_relevan + jumlah_tidak_relevan
    if total_data_relevansi > 0:
        persentase_relevan = (jumlah_relevan / total_data_relevansi) * 100
        persentase_tidak_relevan = (jumlah_tidak_relevan / total_data_relevansi) * 100
        perbedaan_persentase_relevansi = abs(persentase_relevan - persentase_tidak_relevan)
    else:
        persentase_relevan = persentase_tidak_relevan = perbedaan_persentase_relevansi = 0

    # Hitung jumlah tipe akun individu dan media
    jumlah_individu = tipeakun_counter.get('individu', 0)
    jumlah_media = tipeakun_counter.get('media', 0)

    # Hitung persentase perbedaan tipe akun
    total_data_tipeakun = jumlah_individu + jumlah_media
    if total_data_tipeakun > 0:
        persentase_individu = (jumlah_individu / total_data_tipeakun) * 100
        persentase_media = (jumlah_media / total_data_tipeakun) * 100
        perbedaan_persentase_tipeakun = abs(persentase_individu - persentase_media)
    else:
        persentase_individu = persentase_media = perbedaan_persentase_tipeakun = 0

    # Ubah hasil ke format yang bisa dijadikan JSON
    kategori_json = [{"kategori": kategori, "jumlah": jumlah} for kategori, jumlah in kategori_counter.items()]
    relevansi_json = [{"relevansi": relevansi, "jumlah_relevansi": jumlah_relevansi} for relevansi, jumlah_relevansi in relevansi_counter.items()]
    tipeakun_json = [{"tipeakun": tipeakun, "jumlah_tipeakun": jumlah_tipeakun} for tipeakun, jumlah_tipeakun in tipeakun_counter.items()]

    # Membuat dictionary yang berisi data asli, kategori_json, relevansi_json, tipeakun_json, dan persentase perbedaan
    total = {
        "datas": data,
        "categories": kategori_json,
        "relevansi": relevansi_json,
        "tipeakun": tipeakun_json,
        "persentase_relevansi": persentase_relevan,
        "persentase_tidak_relevan": persentase_tidak_relevan,
        "perbedaan_persentase_relevansi": perbedaan_persentase_relevansi,
        "persentase_individu": persentase_individu,
        "persentase_media": persentase_media,
        "perbedaan_persentase_tipeakun": perbedaan_persentase_tipeakun
    }

    return jsonify(total)