from neomodel import StructuredNode, StructuredRel, StringProperty, RelationshipTo, db
from models import *

# =============================
# DATA POPULATION
# =============================
def create_skabies_data():
    # Clear existing data
    db.cypher_query("MATCH (n) DETACH DELETE n")

    # Create Disease Node
    skabies = Disease(
        name="Skabies",
        icd10="B86",
        icpc2="S72",
        capability_level="4A",
        description="Penyakit yang disebabkan infestasi dan sensitisasi kulit oleh tungau Sarcoptes scabiei dan produknya"
    ).save()

    # Create Symptoms
    pruritus = Symptom(
        description="Pruritus nokturna (gatal hebat terutama malam hari)",
        location="Seluruh tubuh",
        time_pattern="Malam hari/saat berkeringat"
    ).save()
    
    lesi = Symptom(
        description="Lesi di stratum korneum",
        location="Sela jari, pergelangan tangan/kaki, aksila, umbilikus, areola mammae, genital eksterna",
        time_pattern="Kronis"
    ).save()

    # Create Risk Factors
    risk1 = RiskFactor(
        description="Masyarakat hidup dalam kelompok padat (asrama/pesantren)",
        category="Lingkungan"
    ).save()
    
    risk2 = RiskFactor(
        description="Higiene buruk",
        category="Perilaku"
    ).save()
    
    risk3 = RiskFactor(
        description="Sosial ekonomi rendah (panti asuhan)",
        category="Ekonomi"
    ).save()
    
    risk4 = RiskFactor(
        description="Hubungan seksual promiskuitas",
        category="Perilaku"
    ).save()

    # Create Physical Exams
    exam1 = PhysicalExam(
        finding="Terowongan (kanalikuli) berwarna putih/abu-abu panjang 1 cm",
        location="Tempat predileksi"
    ).save()
    
    exam2 = PhysicalExam(
        finding="Papul/vesikel di ujung terowongan",
        location="Tempat predileksi"
    ).save()
    
    exam3 = PhysicalExam(
        finding="Pustul/ekskoriasi (jika infeksi sekunder)",
        location="Area garukan"
    ).save()

    # Create Lab Tests
    lab1 = LabTest(
        name="Mikroskopis kerokan kulit",
        specimen="Kerokan kulit dari terowongan",
        result_expected="Ditemukan tungau Sarcoptes scabiei"
    ).save()

    # Create Diagnoses
    diag1 = Diagnosis(
        type="Klinis",
        criteria="Pruritus nokturna + lesi di tempat predileksi"
    ).save()
    
    diag2 = Diagnosis(
        type="Penunjang",
        criteria="Ditemukan tungau pada pemeriksaan mikroskopis"
    ).save()

    # Create Diagnosis Banding
    banding1 = DiagnosisBanding(
        name="Pioderma",
        notes="Infeksi bakteri kulit"
    ).save()
    
    banding2 = DiagnosisBanding(
        name="Impetigo",
        notes="Infeksi kulit superfisial"
    ).save()
    
    banding3 = DiagnosisBanding(
        name="Dermatitis",
        notes="Peradangan kulit"
    ).save()
    
    banding4 = DiagnosisBanding(
        name="Pedikulosis korporis",
        notes="Infestasi kutu badan"
    ).save()

    # Create Complications
    comp1 = Complication(
        name="Infeksi sekunder S. aureus",
        cause="Garukan",
        population="Anak-anak"
    ).save()
    
    comp2 = Complication(
        name="Penurunan kualitas hidup",
        cause="Gatal kronis",
        population="Semua usia"
    ).save()

    # Create Treatments
    # Systemic Treatment
    systemic = Treatment(
        type="Systemik",
        description="Antihistamin untuk gatal",
        route="Oral",
        dosage="Sesuai kebutuhan"
    ).save()
    
    # Topical Treatment
    topical = Treatment(
        type="Topikal",
        description="Kortikosteroid potensi sedang-kuat",
        route="Topikal",
        dosage="2 kali sehari selama 7 hari"
    ).save()
    
    # Create Medications
    med1 = Medication(
        name="Setirizin",
        dose="10 mg",
        duration="7 hari",
        route="Oral"
    ).save()
    
    med2 = Medication(
        name="Loratadin",
        dose="10 mg",
        duration="7 hari",
        route="Oral"
    ).save()
    
    med3 = Medication(
        name="Mometason furoat 0.1%",
        dose="Tipis",
        duration="7 hari",
        route="Topikal"
    ).save()
    
    med4 = Medication(
        name="Betametason valerat 0.5%",
        dose="Tipis",
        duration="7 hari",
        route="Topikal"
    ).save()

    # Create Counselings
    counsel1 = Counseling(
        point="Minum obat secara teratur",
        target="Pasien dan keluarga"
    ).save()
    
    counsel2 = Counseling(
        point="Menjaga kebersihan lingkungan",
        target="Pasien dan keluarga"
    ).save()

    # Create Referral Criteria
    refer1 = ReferralCriteria(
        condition="Memburuk (makin bertambah patch eritema, timbul bula)",
        type="Klinis"
    ).save()
    
    refer2 = ReferralCriteria(
        condition="Gejala sistemik atau komplikasi",
        type="Klinis"
    ).save()

    # Create Equipment
    equip1 = Equipment(
        name="Alat resusitasi",
        purpose="Penanganan emergensi"
    ).save()
    
    equip2 = Equipment(
        name="Tabung dan masker oksigen",
        purpose="Dukungan pernapasan"
    ).save()

    # Create Prognosis
    prog1 = Prognosis(
        category="Bonam",
        context="Prognosis umum"
    ).save()
    
    prog2 = Prognosis(
        category="Dubia ad malam",
        context="Reaksi tipe cepat/tidak biasa"
    ).save()

    # =============================
    # CREATE RELATIONSHIPS
    # =============================
    
    # Disease Relationships
    skabies.symptoms.connect(pruritus)
    skabies.symptoms.connect(lesi)
    
    skabies.risk_factors.connect(risk1)
    skabies.risk_factors.connect(risk2)
    skabies.risk_factors.connect(risk3)
    skabies.risk_factors.connect(risk4)
    
    skabies.physical_exams.connect(exam1)
    skabies.physical_exams.connect(exam2)
    skabies.physical_exams.connect(exam3)
    
    skabies.lab_tests.connect(lab1)
    
    skabies.diagnoses.connect(diag1)
    skabies.diagnoses.connect(diag2)
    
    skabies.diagnosis_bandings.connect(banding1)
    skabies.diagnosis_bandings.connect(banding2)
    skabies.diagnosis_bandings.connect(banding3)
    skabies.diagnosis_bandings.connect(banding4)
    
    skabies.complications.connect(comp1)
    skabies.complications.connect(comp2)
    
    skabies.treatments.connect(systemic)
    skabies.treatments.connect(topical)
    
    skabies.counselings.connect(counsel1)
    skabies.counselings.connect(counsel2)
    
    skabies.referral_criteria.connect(refer1)
    skabies.referral_criteria.connect(refer2)
    
    skabies.equipment.connect(equip1)
    skabies.equipment.connect(equip2)
    
    skabies.prognosis.connect(prog1)
    skabies.prognosis.connect(prog2)
    
    # Treatment-Medication Relationships
    systemic.medications.connect(med1)
    systemic.medications.connect(med2)
    topical.medications.connect(med3)
    topical.medications.connect(med4)

    print("Data Skabies berhasil dibuat!")


if __name__ == "__main__":
    # Configure database connection
    from neomodel import config
    config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'  # Ganti dengan password Neo4j Anda
    
    # Create the data
    create_skabies_data()
    # create_dermatitis_atopik()