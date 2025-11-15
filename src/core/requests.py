from pydantic import BaseModel
from typing import Dict
from datetime import date

class ocb_request(BaseModel):
    start_date: date
    end_date: date
    filters: Dict

class filter_request(BaseModel):
    model: str
    filters: Dict