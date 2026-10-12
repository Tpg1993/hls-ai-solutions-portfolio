from sqlalchemy import Column, String, Integer, Float, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class Patient(Base, TimestampMixin):
    __tablename__ = "patients"

    id = Column(String(50), primary_key=True, index=True)
    synthetic_mrn = Column(String(50), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    primary_diagnosis = Column(String(100), nullable=False, index=True)
    stage = Column(String(20), nullable=False) # Stage IIIB, Stage IV
    ecog_performance = Column(Integer, default=0, nullable=False)
    prior_therapies = Column(String(255), nullable=True) # "Pembrolizumab, Cisplatin"
    last_treatment_date = Column(Date, nullable=True)
    clinical_notes = Column(Text, nullable=True)

    labs = relationship("PatientLab", back_populates="patient", cascade="all, delete-orphan")
    biomarkers = relationship("PatientBiomarker", back_populates="patient", cascade="all, delete-orphan")
    matches = relationship("PatientTrialMatch", back_populates="patient", cascade="all, delete-orphan")

class PatientLab(Base, TimestampMixin):
    __tablename__ = "patient_labs"

    id = Column(String(50), primary_key=True, index=True)
    patient_id = Column(String(50), ForeignKey("patients.id"), nullable=False, index=True)
    test_name = Column(String(100), nullable=False) # Platelets, Hemoglobin, ANC, Creatinine
    result_value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    test_date = Column(Date, nullable=False)

    patient = relationship("Patient", back_populates="labs")

class PatientBiomarker(Base, TimestampMixin):
    __tablename__ = "patient_biomarkers"

    id = Column(String(50), primary_key=True, index=True)
    patient_id = Column(String(50), ForeignKey("patients.id"), nullable=False, index=True)
    gene = Column(String(50), nullable=False) # EGFR, KRAS, BRAF, HER2, PDL1
    mutation_variant = Column(String(100), nullable=False) # "Exon 20 Insertion", "G12C", "V600E"
    status = Column(String(50), default="POSITIVE", nullable=False)

    patient = relationship("Patient", back_populates="biomarkers")
