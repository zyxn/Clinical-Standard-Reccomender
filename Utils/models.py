from neomodel import StructuredNode, StructuredRel, StringProperty, RelationshipTo, db

# =============================
# RELATIONSHIP CLASSES
# =============================
class HasSymptom(StructuredRel): pass
class HasRiskFactor(StructuredRel): pass
class HasPhysicalExam(StructuredRel): pass
class HasLabTest(StructuredRel): pass
class HasDiagnosis(StructuredRel): pass
class HasDiagnosisBanding(StructuredRel): pass
class HasComplication(StructuredRel): pass
class HasTreatment(StructuredRel): pass
class UsesMedication(StructuredRel): pass
class HasCounseling(StructuredRel): pass
class HasReferralCriteria(StructuredRel): pass
class RequiresEquipment(StructuredRel): pass
class HasPrognosis(StructuredRel): pass

# =============================
# NODE CLASSES
# =============================
class Disease(StructuredNode):
    name = StringProperty(unique_index=True)
    icd10 = StringProperty()
    icpc2 = StringProperty()
    capability_level = StringProperty()
    description = StringProperty()

    symptoms = RelationshipTo('Symptom', 'HAS_SYMPTOM', model=HasSymptom)
    risk_factors = RelationshipTo('RiskFactor', 'HAS_RISK_FACTOR', model=HasRiskFactor)
    physical_exams = RelationshipTo('PhysicalExam', 'HAS_PHYSICAL_EXAM', model=HasPhysicalExam)
    lab_tests = RelationshipTo('LabTest', 'HAS_LAB_TEST', model=HasLabTest)
    diagnoses = RelationshipTo('Diagnosis', 'HAS_DIAGNOSIS', model=HasDiagnosis)
    diagnosis_bandings = RelationshipTo('DiagnosisBanding', 'HAS_DIAGNOSIS_BANDING', model=HasDiagnosisBanding)
    complications = RelationshipTo('Complication', 'HAS_COMPLICATION', model=HasComplication)
    treatments = RelationshipTo('Treatment', 'HAS_TREATMENT', model=HasTreatment)
    counselings = RelationshipTo('Counseling', 'HAS_COUNSELING', model=HasCounseling)
    referral_criteria = RelationshipTo('ReferralCriteria', 'HAS_REFERRAL_CRITERIA', model=HasReferralCriteria)
    equipment = RelationshipTo('Equipment', 'REQUIRES_EQUIPMENT', model=RequiresEquipment)
    prognosis = RelationshipTo('Prognosis', 'HAS_PROGNOSIS', model=HasPrognosis)

class Symptom(StructuredNode):
    description = StringProperty(unique_index=True)
    location = StringProperty()
    time_pattern = StringProperty()

class RiskFactor(StructuredNode):
    description = StringProperty(unique_index=True)
    category = StringProperty()

class PhysicalExam(StructuredNode):
    finding = StringProperty(unique_index=True)
    location = StringProperty()

class LabTest(StructuredNode):
    name = StringProperty(unique_index=True)
    specimen = StringProperty()
    result_expected = StringProperty()

class Diagnosis(StructuredNode):
    type = StringProperty()
    criteria = StringProperty(unique_index=True)

class DiagnosisBanding(StructuredNode):
    name = StringProperty(unique_index=True)
    notes = StringProperty()

class Complication(StructuredNode):
    name = StringProperty(unique_index=True)
    cause = StringProperty()
    population = StringProperty()

class Treatment(StructuredNode):
    type = StringProperty()
    description = StringProperty()
    route = StringProperty()
    dosage = StringProperty()
    medications = RelationshipTo('Medication', 'USES_MEDICATION', model=UsesMedication)

class Medication(StructuredNode):
    name = StringProperty(unique_index=True)
    dose = StringProperty()
    duration = StringProperty()
    route = StringProperty()

class Counseling(StructuredNode):
    point = StringProperty(unique_index=True)
    target = StringProperty()

class ReferralCriteria(StructuredNode):
    condition = StringProperty(unique_index=True)
    type = StringProperty()

class Equipment(StructuredNode):
    name = StringProperty(unique_index=True)
    purpose = StringProperty()

class Prognosis(StructuredNode):
    category = StringProperty()
    context = StringProperty(unique_index=True)