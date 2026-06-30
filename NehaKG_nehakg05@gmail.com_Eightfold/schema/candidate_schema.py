from pydantic import BaseModel
from typing import List, Optional


class Skill(BaseModel):
    name: str
    confidence: float


class CandidateProfile(BaseModel):

    candidate_id: str

    full_name: Optional[str]

    emails: List[str]

    phones: List[str]=[]

    headline: Optional[str]

    location: Optional[str]

    years_experience: Optional[int]=None

    skills: List[Skill]=[]
    
    links: list = []

    experience: list = []

    education: list = []

    provenance: dict

    overall_confidence: float