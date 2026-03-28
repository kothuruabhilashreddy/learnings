## Employee Onboarding Record Validation

### Validation layer that catches bad records before they enter any system, and produces a clean report of what passed and what failed using pydantic

#### Project structure:
employee-validator/
├── models/
│   ├── address.py
│   ├── bank_details.py
│   ├── employee.py
│   └── validation_report.py
├── data/
│   ├── valid_employees.json
│   └── invalid_employees.json
├── pipeline.py
└── README.md