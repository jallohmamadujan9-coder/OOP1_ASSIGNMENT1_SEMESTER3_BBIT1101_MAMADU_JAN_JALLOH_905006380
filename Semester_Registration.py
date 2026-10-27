"""Semester registration and approval status."""

class Registration:
    def __init__(self, student, semester, module_names):
        self.student = student
        self.semester = semester.strip()
        self.module_names = list(module_names)
        self.bank_slip_reference = "Not submitted"
        self.finance_status = "NOT SUBMITTED"
        self.year_leader_approved = True  # Module assignment/progression is completed first
        self.year_leader_note = "Modules assigned by Year Leader."
        self.faculty_status = "PENDING"
        self.registry_status = "PENDING"
        self.registration_status = "PENDING FINANCE"
        self.approval_history = ["Year Leader: modules assigned before registration."]

    def submit_bank_slip_reference(self, reference):
        if not reference.strip():
            raise ValueError("Payment reference cannot be empty.")
        self.bank_slip_reference = reference.strip()
        self.finance_status = "PENDING VERIFICATION"
        self.registration_status = "PENDING FINANCE"
        self.approval_history.append("Student submitted a payment reference.")

    def create_printable_registration_form(self):
        modules = "\n".join(f"{i}. {name}" for i, name in enumerate(self.module_names, 1)) or "No modules assigned"
        history = "\n".join(f"- {entry}" for entry in self.approval_history)
        return f"""============================================================
        STUDENT SEMESTER REGISTRATION FORM (PROTOTYPE)
============================================================
Student ID:       {self.student.student_id}
Student Name:     {self.student.full_name}
Email:            {self.student.email}
Programme:        {self.student.programme}
Level:            {self.student.current_level}
Semester:         {self.semester}

MODULES
{modules}

APPROVALS
Year Leader:      {'APPROVED' if self.year_leader_approved else 'PENDING'}
Finance:          {self.finance_status}
Faculty:           {self.faculty_status}
Registry:          {self.registry_status}
Payment Reference: {self.bank_slip_reference}
Registration Status: {self.registration_status}

ACTIVITY HISTORY
{history}

Final signature: __________________________________________
Date: ____________________  Official stamp: _______________
============================================================
Educational prototype only; not an official university form.
"""