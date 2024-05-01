from datetime import datetime
from typing import List

from pydantic import BaseModel, validator


class DateRequest(BaseModel):
    dates: List[str]

    @validator('dates')
    def validate_date_format(cls, v):
        for date_str in v:
            try:
                datetime.strptime(date_str, "%d-%m-%Y")
            except ValueError:
                raise ValueError("Incorrect date format, should be dd-mm-yyyy")
        return v
