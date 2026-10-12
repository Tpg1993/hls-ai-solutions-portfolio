from typing import List, Optional
from datetime import date
from pydantic import BaseModel

class LabItem(BaseModel):
    test_name: str
    result_value: float
    unit: str
    test_date: date

class BiomarkerItem(BaseModel):
    gene: str
    mutation_variant: str
    status: str

class PatientListItem(BaseModel):
    id: str
    synthetic_mrn: str
    age: int
    gender: str
    primary_diagnosis: str
    stage: str
    ecog_performance: int
    prior_therapies: Optional[str] = None
    clinical_notes: Optional[str] = None

class PatientDetail(PatientListItem):
    labs: List[LabItem] = []
    biomarkers: List[BiomarkerItem] = []
