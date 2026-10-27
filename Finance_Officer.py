"""Finance payment-reference verification."""
class FinanceOfficer:
    def verify_payment(self, registration, approved, note):
        if registration.bank_slip_reference == "Not submitted":
            raise ValueError("The student has not submitted a payment reference.")
        if approved:
            registration.finance_status = "VERIFIED"
            registration.registration_status = "PENDING FACULTY"
            result = "Finance verified the payment reference."
        else:
            registration.finance_status = "REJECTED"
            registration.registration_status = "RETURNED FOR CORRECTION"
            result = "Finance rejected the payment reference."
        registration.approval_history.append(f"Finance: {registration.finance_status}. Note: {note or 'No note provided.'}")
        return result