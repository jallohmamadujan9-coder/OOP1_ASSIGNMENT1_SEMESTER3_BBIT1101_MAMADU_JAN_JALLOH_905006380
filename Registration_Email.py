"""Creates sample email text; does not send a real email."""
class RegistrationEmail:
    @classmethod
    def create_registration_status_email(cls, registration):
        student = registration.student
        return (f"TO: {student.email}\nSUBJECT: Semester registration status\n\n"
                f"Hello {student.full_name},\nYour registration for {registration.semester} is "
                f"{registration.registration_status}.\nThis is sample text; no email was sent.")