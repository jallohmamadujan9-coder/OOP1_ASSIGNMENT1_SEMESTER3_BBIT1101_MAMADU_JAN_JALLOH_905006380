"""Student account, personal details, funding information and academic records."""

class Student:
    university_name = "Limkokwing University of Creative Technology"

    def __init__(self, student_id, full_name, email, programme, current_level,
                 date_of_birth="", phone="", funding_type="Self-sponsored",
                 sponsor_name="", login_password="", application_status="REGISTERED"):
        self.student_id = student_id.strip().upper()
        self.full_name = full_name.strip()
        self.email = email.strip()
        self.programme = programme.strip()
        self.current_level = current_level.strip()
        self.date_of_birth = date_of_birth.strip()
        self.phone = phone.strip()
        self.funding_type = funding_type.strip()
        self.sponsor_name = sponsor_name.strip()
        self.login_password = login_password
        self.application_status = application_status
        self.results = {}
        self.assigned_modules = []
        self.module_semester = ""
        self.registration = None

    def add_module_result(self, module_name, grade):
        self.results[module_name] = grade.strip().upper()

    def display_student_details(self):
        return (f"ID/Application Ref: {self.student_id} | Name: {self.full_name} | Email: {self.email} | "
                f"Programme: {self.programme} | Level: {self.current_level} | "
                f"Funding: {self.funding_type} | Sponsor: {self.sponsor_name or 'Not applicable'} | "
                f"Application: {self.application_status}")

    def display_results(self):
        if not self.results:
            return "No results have been entered yet."
        return "\n".join(f"{module}: {grade}" for module, grade in self.results.items())

    def save_assigned_modules(self, module_names, semester=""):
        self.assigned_modules = list(module_names)
        self.module_semester = semester

    def start_semester_registration(self, semester):
        if not self.assigned_modules or self.module_semester.lower() != semester.strip().lower():
            raise ValueError("The correct modules have not been configured for your programme, level and semester. Contact your Year Leader.")
        from Semester_Registration import Registration
        self.registration = Registration(self, semester, self.assigned_modules)
        return self.registration