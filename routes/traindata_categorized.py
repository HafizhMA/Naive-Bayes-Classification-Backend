from flask import Blueprint, jsonify
from collections import Counter
from function.obj_converter import call_DatasetCleaned_obj, call_trainingdata_obj
from function.categorize_trainingdata import categorize_text
from models.model import db

traindata = Blueprint('traindata', __name__, template_folder='routes')

@traindata.route("/get-relevance-data")
def get_relevance():
    data = call_DatasetCleaned_obj()

    # Ambil kolom yang berisi kategori, relevansi, dan tipe akun
    kategori_column = [row['category'] for row in data]
    relevansi_column = [row['relevansi'] for row in data]
    tipeakun_column = [row['tipe_akun'] for row in data]

    # Hitung frekuensi setiap kategori, relevansi, dan tipe akun
    kategori_counter = Counter(kategori_column)
    relevansi_counter = Counter(relevansi_column)
    tipeakun_counter = Counter(tipeakun_column)

    # Hitung jumlah relevan dan notrelevan
    jumlah_relevan = relevansi_counter.get('relevan', 0)
    jumlah_notrelevan = relevansi_counter.get('notrelevan', 0)
    total_relevansi = jumlah_relevan + jumlah_notrelevan

    # Hitung persentase relevan dan notrelevan
    if total_relevansi > 0:
        persen_relevan = (jumlah_relevan / total_relevansi) * 100
        persen_notrelevan = (jumlah_notrelevan / total_relevansi) * 100
    else:
        persen_relevan = 0
        persen_notrelevan = 0

    # Hitung jumlah individu dan media
    jumlah_media = tipeakun_counter.get('media', 0)
    jumlah_individu = tipeakun_counter.get('individu', 0)
    total_tipeakun = jumlah_media + jumlah_individu

    # Hitung persentase relevan dan notrelevan
    if total_tipeakun > 0:
        persen_media = (jumlah_media / jumlah_individu) * 100
        persen_individu = (jumlah_individu / jumlah_media) * 100
    else:
        persen_media = 0
        persen_individu = 0

    # Ubah hasil ke format yang bisa dijadikan JSON
    kategori_json = [{"kategori": kategori, "jumlah": jumlah} for kategori, jumlah in kategori_counter.items()]
    relevansi_json = [{"relevansi": relevansi, "jumlah_relevansi": jumlah_relevansi} for relevansi, jumlah_relevansi in relevansi_counter.items()]
    tipeakun_json = [{"tipeakun": tipeakun, "jumlah_tipeakun": jumlah_tipeakun} for tipeakun, jumlah_tipeakun in tipeakun_counter.items()]

    # Membuat dictionary yang berisi data asli, kategori_json, relevansi_json, tipeakun_json, dan persentase relevansi
    total = {
        "data": data,
        "category": kategori_json,
        "relevansi": relevansi_json,
        "tipeakun": tipeakun_json,
        "persentase_relevansi": [{
            "relevan": persen_relevan,
            "notrelevan": persen_notrelevan,
            "perbedaan_relevansi": persen_relevan - persen_notrelevan
        }],
        "persentase_tipeakun": [{
            "media": persen_media,
            "individu": persen_individu,
            "perbedaan_tipeakun": persen_media - persen_individu
        }]
    }

    return jsonify(total)