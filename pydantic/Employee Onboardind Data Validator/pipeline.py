import json
from pydantic import ValidationError
from models.employee import Employee
from models.validation_report import ValidationReport, FailedRecord


def run_pipeline(data_path: str) -> ValidationReport:
    with open(data_path) as f:
        records = json.load(f)

        passed = []
        failed = []

        for i, record in enumerate(records):
            try:
                employee = Employee(**record)
                passed.append(employee)
            except ValidationError as e:
                errors = [err['msg'] for err in e.errors()]
                failed.append(FailedRecord(record_index = i, raw_data = record, errors = errors))
            
    return ValidationReport(
        total_records=len(records),
        passed=len(passed),
        failed=len(failed),
        success_rate=len(passed) / len(records),
        failed_records=failed
    )



if __name__ == '__main__':
    report = run_pipeline('data/invalid_employees.json')
    print(report.summary)
    print(report.model_dump_json())
