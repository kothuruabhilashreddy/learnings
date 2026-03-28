from pydantic import BaseModel, computed_field
from typing import List
from datetime import datetime

class FailedRecord(BaseModel):
    record_index: int
    raw_data: dict
    errors: List[str]

class ValidationReport(BaseModel):
    total_records: int
    passed: int
    failed: int
    success_rate: int
    failed_records: List[FailedRecord]
    generated_at: datetime = datetime.now()

    @computed_field
    @property
    def summary(self) -> str:
        return (
            f'Processed {self.total_records} records | '
            f'Passed {self.passed} records | Failed {self.failed} records | '
            f'Success rate: {self.success_rate}'
        )




