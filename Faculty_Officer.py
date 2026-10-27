"""Faculty review of registration."""
class FacultyOfficer:
    def review_registration(self, registration, approved, note):
        if registration.finance_status != "VERIFIED":
            raise ValueError("Faculty review is locked until Finance verifies the payment.")
        if approved:
            registration.faculty_status = "APPROVED"
            registration.registration_status = "PENDING REGISTRY"
            result = "Faculty approved the registration."
        else:
            registration.faculty_status = "REJECTED"
            registration.registration_status = "RETURNED FOR CORRECTION"
            result = "Faculty returned the registration for correction."
        registration.approval_history.append(f"Faculty: {registration.faculty_status}. Note: {note or 'No note provided.'}")
        return result