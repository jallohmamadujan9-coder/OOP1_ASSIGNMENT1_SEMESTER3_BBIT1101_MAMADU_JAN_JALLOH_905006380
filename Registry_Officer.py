"""Registry student-record management and final approval."""
class RegistryOfficer:
    def add_student(self, students, student):
        if any(existing.student_id == student.student_id for existing in students):
            raise ValueError("A student with that ID already exists.")
        students.append(student)
        return f"Student record created for {student.full_name}."

    def update_student_details(self, student, full_name, email, programme, level):
        student.full_name = full_name.strip()
        student.email = email.strip()
        student.programme = programme.strip()
        student.current_level = level.strip()
        return "Official student details updated."

    def give_final_approval(self, registration, approved, note):
        if registration.finance_status != "VERIFIED" or registration.faculty_status != "APPROVED":
            raise ValueError("Final approval requires verified Finance and approved Faculty reviews.")
        if approved:
            registration.registry_status = "APPROVED"
            registration.registration_status = "APPROVED"
            result = "Registry gave final approval. Registration is complete."
        else:
            registration.registry_status = "RETURNED"
            registration.registration_status = "RETURNED FOR CORRECTION"
            result = "Registry returned the registration for correction."
        registration.approval_history.append(f"Registry: {registration.registry_status}. Note: {note or 'No note provided.'}")
        return result