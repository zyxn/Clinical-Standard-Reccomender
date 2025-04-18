from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import re
import os
from dotenv import load_dotenv
import pdfplumber

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# ==================== PYDANTIC MODELS ====================

def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug"""
    if not text:
        return ""
    text = text.strip().lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

class IdentifiableByDescription(BaseModel):
    id: str = Field(..., description="Auto-generated unique ID")

    @validator('id', always=True, pre=True)
    def generate_id(cls, v, values):
        if v:
            return v
            
        content_parts = []
        for field in ['description', 'name', 'finding', 'point', 'condition']:
            if field in values and values[field]:
                content_parts.append(str(values[field]))
        
        if not content_parts:
            return "id-" + str(hash(frozenset(values.items())))
        
        return slugify("-".join(content_parts))

class Symptom(IdentifiableByDescription):
    description: str
    location: Optional[str] = None
    time_pattern: Optional[str] = None

class RiskFactor(IdentifiableByDescription):
    description: str
    category: Optional[str] = None

class PhysicalExam(IdentifiableByDescription):
    finding: str
    location: Optional[str] = None

class LabTest(IdentifiableByDescription):
    name: str
    specimen: Optional[str] = None
    result_expected: Optional[str] = None

class Diagnosis(IdentifiableByDescription):
    type: str
    criteria: Optional[str] = None

class DiagnosisBanding(IdentifiableByDescription):
    name: str
    notes: Optional[str] = None

class Complication(IdentifiableByDescription):
    name: str
    cause: Optional[str] = None
    population: Optional[str] = None

class Medication(IdentifiableByDescription):
    name: str
    dose: Optional[str] = None
    duration: Optional[str] = None
    route: Optional[str] = None

class Treatment(IdentifiableByDescription):
    type: str
    description: Optional[str] = None
    route: Optional[str] = None
    dosage: Optional[str] = None
    medications: List[Medication] = Field(default_factory=list)

class Counseling(IdentifiableByDescription):
    point: str
    target: Optional[str] = None

class ReferralCriteria(IdentifiableByDescription):
    condition: str
    type: Optional[str] = None

class Equipment(IdentifiableByDescription):
    name: str
    purpose: Optional[str] = None

class Prognosis(BaseModel):
    category: str
    context: Optional[str] = None

class DiseaseSchema(BaseModel):
    disease_name: str
    icd10: str
    icpc2: str
    capability_level: str
    description: Optional[str] = None

    symptoms: List[Symptom] = Field(default_factory=list)
    risk_factors: List[RiskFactor] = Field(default_factory=list)
    physical_exams: List[PhysicalExam] = Field(default_factory=list)
    lab_tests: List[LabTest] = Field(default_factory=list)
    diagnosis: Optional[Diagnosis] = None
    diagnosis_bandings: List[DiagnosisBanding] = Field(default_factory=list)
    complications: List[Complication] = Field(default_factory=list)
    treatments: List[Treatment] = Field(default_factory=list)
    counselings: List[Counseling] = Field(default_factory=list)
    referral_criteria: List[ReferralCriteria] = Field(default_factory=list)
    equipment: List[Equipment] = Field(default_factory=list)
    prognosis: Optional[Prognosis] = None

# ==================== PDF PROCESSING ====================

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from PDF file"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

# ==================== LLM PROCESSING ====================

def setup_llm_pipeline():
    """Configure the LLM extraction pipeline"""
    parser = PydanticOutputParser(pydantic_object=DiseaseSchema)
    
    model = ChatOpenAI(
        model="gpt-4",
        temperature=0
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Anda adalah dokter ahli yang mampu mengekstrak informasi klinis dari teks SOP. 
        Hasilkan output JSON terstruktur dengan semua entitas yang memiliki ID unik."""),
        ("human", """Ekstrak informasi penyakit dari teks berikut:

{input_text}

Format output yang diharapkan:
{format_instructions}

Pastikan:
1. Semua entitas memiliki ID unik
2. Semua field required terisi
3. Format mengikuti schema yang ditentukan""")
    ])
    
    return parser, model, prompt

def extract_schema_from_text(text: str) -> DiseaseSchema:
    """Process text through LLM to extract structured data"""
    parser, model, prompt = setup_llm_pipeline()
    
    chain = prompt | model | parser
    
    try:
        result = chain.invoke({
            "input_text": text,
            "format_instructions": parser.get_format_instructions()
        })
        return result
    except Exception as e:
        print(f"Error processing text: {e}")
        raise

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    # Example usage
    pdf_path = r"Dataset\output_ppk\KULIT\07_Skabies.pdf"
    
    try:
        print(f"Processing PDF: {pdf_path}")
        
        # Step 1: Extract text from PDF
        raw_text = extract_text_from_pdf(pdf_path)
        print(f"Extracted {len(raw_text)} characters from PDF")
        
        # Step 2: Process through LLM
        print("Extracting structured data...")
        disease_schema = extract_schema_from_text(raw_text)
        
        # Step 3: Output results
        print("\nExtracted Disease Schema:")
        print(disease_schema.model_dump_json(indent=2))
        
        # You can save to file
        with open("extracted_disease.json", "w") as f:
            f.write(disease_schema.model_dump_json(indent=2))
        print("Results saved to extracted_disease.json")
        
    except Exception as e:
        print(f"Error in processing pipeline: {e}")