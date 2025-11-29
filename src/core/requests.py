from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class ocb_request(BaseModel):
    start_date: datetime
    end_date: datetime
    storage_id: str
    filters: Dict

class filter_request(BaseModel):
    model: str
    filters: Dict

class block_date_request(BaseModel):
    new_block_date: datetime

class reference_get(BaseModel):
    type: str
    id: str

class reference(BaseModel):
    type: str
    properties: Dict