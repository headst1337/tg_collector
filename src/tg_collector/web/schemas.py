from datetime import datetime

from pydantic import BaseModel, field_validator


class DateRequest(BaseModel):
    dates: list[str]

    @field_validator('dates')
    def validate_date_format(cls, v):
        for date_str in v:
            try:
                datetime.strptime(date_str, "%d-%m-%Y")
            except ValueError:
                raise ValueError("Incorrect date format, should be dd-mm-yyyy")
        return v
