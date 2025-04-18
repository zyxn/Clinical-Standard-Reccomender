import os
import fitz  # PyMuPDF

# Path ke file PDF
pdf_path = "Dataset\ppk-primer-idi-2017_unlocked.pdf"
output_folder = "./Dataset/output_ppk"


# Ini adalah versi lengkap daftar isi yang akan digunakan sebagai toc_list dengan bab/kelompoknya
toc_full = [
    # A. KELOMPOK UMUM
    ("KELOMPOK_UMUM/01_Tuberkulosis (TB) Paru", 7),
    ("KELOMPOK_UMUM/02_TB dengan HIV", 15),
    ("KELOMPOK_UMUM/03_Morbili", 17),
    ("KELOMPOK_UMUM/04_Varisela", 19),
    ("KELOMPOK_UMUM/05_Malaria", 21),
    ("KELOMPOK_UMUM/06_Leptospirosis", 23),
    ("KELOMPOK_UMUM/07_Filariasis", 25),
    ("KELOMPOK_UMUM/08_Infeksi pada Umbilikus", 29),
    ("KELOMPOK_UMUM/09_Kandidiasis Mulut", 30),
    ("KELOMPOK_UMUM/10_Lepra", 31),
    ("KELOMPOK_UMUM/11_Keracunan Makanan", 37),
    ("KELOMPOK_UMUM/12_Alergi Makanan", 39),
    ("KELOMPOK_UMUM/13_Syok", 40),
    ("KELOMPOK_UMUM/14_Reaksi Anafilaktik", 44),
    ("KELOMPOK_UMUM/15_Demam Dengue dan Demam Berdarah Dengue", 47),

    # B. DARAH, PEMBENTUKAN DARAH DAN SISTEM IMUN
    ("DARAH_DAN_IMUN/01_Anemia Defisiensi Besi", 52),
    ("DARAH_DAN_IMUN/02_HIV-AIDS tanpa Komplikasi", 54),
    ("DARAH_DAN_IMUN/03_Lupus Eritematosus Sistemik", 58),
    ("DARAH_DAN_IMUN/04_Limfadenitis", 62),

    # C. DIGESTIVE
    ("DIGESTIVE/01_Ulkus Mulut (Aftosa, Herpes)", 64),
    ("DIGESTIVE/02_Refluks Gastroesofageal", 67),
    ("DIGESTIVE/03_Gastritis", 69),
    ("DIGESTIVE/04_Intoleransi Makanan", 70),
    ("DIGESTIVE/05_Malabsorbsi Makanan", 71),
    ("DIGESTIVE/06_Demam Tifoid", 73),
    ("DIGESTIVE/07_Gastroenteritis (Kolera dan Giardiasis)", 78),
    ("DIGESTIVE/08_Disentri Basiler dan Disentri Amuba", 85),
    ("DIGESTIVE/09_Perdarahan Gastrointestinal", 87),
    ("DIGESTIVE/10_Hemoroid Grade 1-2", 90),
    ("DIGESTIVE/11_Hepatitis A", 92),
    ("DIGESTIVE/12_Hepatitis B", 94),
    ("DIGESTIVE/13_Kolesistisis", 96),
    ("DIGESTIVE/14_Apendisitis Akut", 97),
    ("DIGESTIVE/15_Peritinitis", 100),
    ("DIGESTIVE/16_Parotitis", 101),
    ("DIGESTIVE/17_Askariasis", 103),
    ("DIGESTIVE/18_Ankilostomiasis", 105),
    ("DIGESTIVE/19_Skistosomiasis", 107),
    ("DIGESTIVE/20_Taeniasis", 110),
    ("DIGESTIVE/21_Strongiloidasis", 111),

    # D. MATA
    ("MATA/01_Mata Kering", 114),
    ("MATA/02_Buta Senja", 116),
    ("MATA/03_Hordeolum", 117),
    ("MATA/04_Konjungtivitis", 118),
    ("MATA/05_Blefaritis", 120),
    ("MATA/06_Perdarahan Subkonjungtiva", 121),
    ("MATA/07_Benda Asing di Konjungtiva", 123),
    ("MATA/08_Astigmatisme", 124),
    ("MATA/09_Hipermetropia", 125),
    ("MATA/10_Miopia Ringan", 126),
    ("MATA/11_Presbiopia", 127),
    ("MATA/12_Katarak pada Pasien Dewasa", 129),
    ("MATA/13_Glaukoma Akut", 130),
    ("MATA/14_Glaukoma Kronis", 132),
    ("MATA/15_Trikiasis", 133),
    ("MATA/16_Episkleritis", 135),
    ("MATA/17_Trauma Kimia Mata", 137),
    ("MATA/18_Laserasi Kelopak Mata", 138),
    ("MATA/19_Hifema", 140),
    ("MATA/20_Retinopati Diabetik", 141),

    # E. TELINGA
    ("TELINGA/01_Otitis Eksterna", 143),
    ("TELINGA/02_Otitis Media Akut", 145),
    ("TELINGA/03_Otitis Media Supuratif Kronik", 147),
    ("TELINGA/04_Benda Asing di Telinga", 149),
    ("TELINGA/05_Serumen Prop", 150),

    # F. KARDIOVASKULER
    ("KARDIOVASKULER/01_Angina Pektoris Stabil", 152),
    ("KARDIOVASKULER/02_Infark Miokard", 155),
    ("KARDIOVASKULER/03_Takikardia", 157),
    ("KARDIOVASKULER/04_Gagal Jantung Akut dan Kronik", 159),
    ("KARDIOVASKULER/05_Cardiorespiratory Arrest", 161),
    ("KARDIOVASKULER/06_Hipertensi Esensial", 162),

    # G. MUSKULOSKELETAL
    ("MUSKULOSKELETAL/01_Fraktur Terbuka", 166),
    ("MUSKULOSKELETAL/02_Fraktur Tertutup", 168),
    ("MUSKULOSKELETAL/03_Polimialgia Reumatik", 169),
    ("MUSKULOSKELETAL/04_Artritis Reumatoid", 170),
    ("MUSKULOSKELETAL/05_Artritis, Osteoartritis", 174),
    ("MUSKULOSKELETAL/06_Vulnus", 175),
    ("MUSKULOSKELETAL/07_Lipoma", 178),

    # H. NEUROLOGI
    ("NEUROLOGI/01_Tension Headache", 179),
    ("NEUROLOGI/02_Migren", 182),
    ("NEUROLOGI/03_Vertigo", 185),
    ("NEUROLOGI/04_Tetanus", 190),
    ("NEUROLOGI/05_Rabies", 194),
    ("NEUROLOGI/06_Malaria Serebral", 197),
    ("NEUROLOGI/07_Epilepsi", 199),
    ("NEUROLOGI/08_Transient Ischemic Attack (TIA)", 204),
    ("NEUROLOGI/09_Stroke", 207),
    ("NEUROLOGI/10_Bell’s Palsy", 210),
    ("NEUROLOGI/11_Status Epileptikus", 215),
    ("NEUROLOGI/12_Delirium", 216),
    ("NEUROLOGI/13_Kejang Demam", 218),
    ("NEUROLOGI/14_Tetanus Neonatorum", 221),

    # I. PSIKIATRI
    ("PSIKIATRI/01_Gangguan Somatoform", 224),
    ("PSIKIATRI/02_Demensia", 228),
    ("PSIKIATRI/03_Insomnia", 230),
    ("PSIKIATRI/04_Gangguan Campuran Anxietas dan Depresi", 231),
    ("PSIKIATRI/05_Gangguan Psikotik", 234),

    # J. RESPIRASI
    ("RESPIRASI/01_Influenza", 237),
    ("RESPIRASI/02_Faringitis Akut", 239),
    ("RESPIRASI/03_Laringitis Akut", 242),
    ("RESPIRASI/04_Tonsilitis Akut", 245),
    ("RESPIRASI/05_Bronkitis Akut", 248),
    ("RESPIRASI/06_Asma Bronkial (Asma Stabil)", 251),
    ("RESPIRASI/07_Status Asmatikus", 258),
    ("RESPIRASI/08_Pneumonia Aspirasi", 261),
    ("RESPIRASI/09_Pneumonia, Bronkopneumonia", 262),
    ("RESPIRASI/10_Pneumotoraks", 268),
    ("RESPIRASI/11_PPOK", 269),
    ("RESPIRASI/12_Epistaksis", 273),
    ("RESPIRASI/13_Benda Asing di Hidung", 276),
    ("RESPIRASI/14_Furunkel pada Hidung", 278),
    ("RESPIRASI/15_Rinitis Akut", 279),
    ("RESPIRASI/16_Rinitis Vasomotor", 282),
    ("RESPIRASI/17_Rinitis Alergik", 284),
    ("RESPIRASI/18_Sinusitis (Rinosinusitis)", 286),

    # … (akan dilanjutkan jika kamu ingin bagian K s/d O juga)
]

toc_full += [
    # K. KULIT
    ("KULIT/01_Miliaria", 291),
    ("KULIT/02_Veruka Vulgaris", 293),
    ("KULIT/03_Herpes Zoster", 294),
    ("KULIT/04_Herpes Simpleks", 296),
    ("KULIT/05_Moluskum Kontagiosum", 299),
    ("KULIT/06_Reaksi Gigitan Serangga", 300),
    ("KULIT/07_Skabies", 302),
    ("KULIT/08_Pedikulosis Kapitis", 304),
    ("KULIT/09_Pedikulosis Pubis", 306),
    ("KULIT/10_Dermatofitosis", 308),
    ("KULIT/11_Pitiriasis Versikolor", 310),
    ("KULIT/12_Pioderma", 312),
    ("KULIT/13_Erisipelas", 314),
    ("KULIT/14_Dermatitis Seboroik", 316),
    ("KULIT/15_Dermatitis Atopik", 318),
    ("KULIT/16_Dermatitis Numularis", 321),
    ("KULIT/17_Liken Simpleks Kronik", 323),
    ("KULIT/18_Dermatitis Kontak Alergik", 325),
    ("KULIT/19_Dermatitis Kontak Iritan", 327),
    ("KULIT/20_Napkin Eczema", 330),
    ("KULIT/21_Dermatitis Perioral", 332),
    ("KULIT/22_Pitiriasis Rosea", 334),
    ("KULIT/23_Eritrasma", 335),
    ("KULIT/24_Skrofuloderma", 337),
    ("KULIT/25_Hidradenitis Supuratif", 338),
    ("KULIT/26_Akne Vulgaris Ringan", 341),
    ("KULIT/27_Urtikaria", 344),
    ("KULIT/28_Exanthematous Drug Eruption", 347),
    ("KULIT/29_Fixed Drug Eruption", 348),
    ("KULIT/30_Cutaneus Larva Migrans", 350),
    ("KULIT/31_Luka Bakar Derajat I dan II", 352),
    ("KULIT/32_Ulkus pada Tungkai", 354),
    ("KULIT/33_Sindrom Stevens-Johnson", 357),

    # L. METABOLIK ENDOKRIN DAN NUTRISI
    ("METABOLIK/01_Obesitas", 360),
    ("METABOLIK/02_Tirotoksikosis", 362),
    ("METABOLIK/03_Diabetes Mellitus Tipe 2", 364),
    ("METABOLIK/04_Hiperglikemia Hiperosmolar Non Ketotik", 368),
    ("METABOLIK/05_Hipoglikemia", 370),
    ("METABOLIK/06_Hiperurisemia-Gout Arthritis", 372),
    ("METABOLIK/07_Dislipidemia", 374),
    ("METABOLIK/08_Malnutrisi Energi Protein (MEP)", 377),

    # M. GINJAL DAN SALURAN KEMIH
    ("GINJAL/01_Infeksi Saluran Kemih", 380),
    ("GINJAL/02_Pielonefritis Tanpa Komplikasi", 382),
    ("GINJAL/03_Fimosis", 385),
    ("GINJAL/04_Parafimosis", 386),

    # N. KESEHATAN WANITA
    ("WANITA/01_Kehamilan Normal", 388),
    ("WANITA/02_Hiperemesis Gravidarum", 393),
    ("WANITA/03_Anemia Defisiensi Besi pada Kehamilan", 396),
    ("WANITA/04_Pre-Eklampsia", 398),
    ("WANITA/05_Eklampsia", 401),
    ("WANITA/06_Abortus", 403),
    ("WANITA/07_Ketuban Pecah Dini (KPD)", 407),
    ("WANITA/08_Persalinan Lama", 409),
    ("WANITA/09_Perdarahan Post Partum", 412),
    ("WANITA/10_Ruptur Perineum Tingkat 1-2", 417),
    ("WANITA/11_Mastitis", 422),
    ("WANITA/12_Inverted Nipple", 424),
    ("WANITA/13_Cracked Nipple", 426),

    # O. PENYAKIT KELAMIN
    ("KELAMIN/01_Fluor Albus (Vaginal Discharge Non Gonore)", 428),
    ("KELAMIN/02_Sifilis", 431),
    ("KELAMIN/03_Gonore", 436),
    ("KELAMIN/04_Vaginitis", 438),
    ("KELAMIN/05_Vulvitis", 440)
]

# Hitung halaman akhir tiap bab berdasarkan awal bab berikutnya
offset = 19
structured_toc = []
for i, (title, start_page) in enumerate(toc_full):
      # Karena halaman 1 = halaman PDF ke-26
    start = int(start_page) + offset
    end = int(toc_full[i + 1][1]) + offset - 1 if i + 1 < len(toc_full) else None

    structured_toc.append((title, start, end))

# Buka dokumen PDF
doc = fitz.open(pdf_path)

# Buat output folder
os.makedirs(output_folder, exist_ok=True)

# Proses per bagian
for entry in structured_toc:
    title_path, start_page, end_page = entry
    folder_name, filename = title_path.split("/", 1)

    # Folder berdasarkan bab
    full_folder_path = os.path.join(output_folder, folder_name)
    os.makedirs(full_folder_path, exist_ok=True)

    # File output
    output_file = os.path.join(full_folder_path, f"{filename.replace(' ', '_')}.pdf")

    # Ambil halaman dari PDF
    new_doc = fitz.open()
    start_idx = start_page - 1
    end_idx = (end_page - 1) if end_page else start_idx + 2  # Jika tidak tahu akhir, ambil 2 halaman

    for i in range(start_idx, end_idx + 1):
        if i < len(doc):  # Safety check
            new_doc.insert_pdf(doc, from_page=i, to_page=i)

    new_doc.save(output_file)
    new_doc.close()
    print(f"✅ Disimpan: {output_file}")

print("\n✅ Semua PDF berhasil dipisahkan per penyakit dan bab.")