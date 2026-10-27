"""Role-based university registration prototype. All records are in memory only."""

import re
from datetime import datetime
from Student_Details import Student
from Year_Leader import YearLeader
from Finance_Officer import FinanceOfficer
from Faculty_Officer import FacultyOfficer
from Registry_Officer import RegistryOfficer
from Registration_Email import RegistrationEmail


ACCOUNTS = {
    "yearleader": ("Year Leader", "year123"),
    "finance": ("Finance Officer", "finance123"),
    "faculty": ("Faculty Officer", "faculty123"),
    "registry": ("Registry Officer", "registry123"),
}

PROGRAMMES = [
    "Software Engineering",
    "Information Technology",
    "Architecture",
    "Media",
    "Broadcasting",
    "Other",
]
FUNDING_TYPES = [
    "Self-sponsored",
    "Government-sponsored",
    "Family/individual sponsor",
    "Organisation/scholarship",
]

students = []
next_application_number = 1
year_leader = YearLeader()
finance_officer = FinanceOfficer()
faculty_officer = FacultyOfficer()
registry_officer = RegistryOfficer()


def line():
    print("-" * 68)


def pause():
    input("\nPress Enter to continue...")


def ask(prompt):
    """Read a trimmed console response."""
    return input(prompt).strip()


def ask_required(prompt):
    """Keep asking until the user enters a non-empty value."""
    while True:
        value = ask(prompt)
        if value:
            return value
        print("This field is required. Please try again.")


def ask_email(prompt="Email address: "):
    while True:
        value = ask(prompt)
        if re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", value):
            return value
        print("Invalid email. Enter an address like student@example.com.")


def ask_phone(prompt="Phone number: "):
    while True:
        value = ask(prompt)
        digits = re.sub(r"[ +()-]", "", value)
        if digits.isdigit() and 7 <= len(digits) <= 15:
            return value
        print("Invalid phone number. Use 7–15 digits; spaces, +, parentheses and hyphens are optional.")


def ask_date(prompt="Date of birth (DD/MM/YYYY): "):
    while True:
        value = ask(prompt)
        try:
            datetime.strptime(value, "%d/%m/%Y")
            return value
        except ValueError:
            print("Invalid date. Use a real date in DD/MM/YYYY format, e.g. 05/02/2005.")


def ask_number(prompt, minimum=1, maximum=None):
    while True:
        value = ask(prompt)
        if value.isdigit():
            number = int(value)
            if number >= minimum and (maximum is None or number <= maximum):
                return number
        if maximum is None:
            print(f"Enter a whole number of at least {minimum}.")
        else:
            print(f"Enter a whole number from {minimum} to {maximum}.")


def ask_level(prompt="Entry level/year (e.g. Year 1): "):
    while True:
        value = ask(prompt)
        match = re.fullmatch(r"(?:year\s*)?([1-6])", value, re.IGNORECASE)
        if match:
            return f"Year {match.group(1)}"
        print("Enter a valid year, e.g. Year 1 or 1.")


def ask_semester(prompt="Intended semester (e.g. Semester 1): "):
    while True:
        value = ask(prompt)
        match = re.fullmatch(r"(?:semester\s*)?([1-3])", value, re.IGNORECASE)
        if match:
            return f"Semester {match.group(1)}"
        print("Enter a valid semester, e.g. Semester 1 or 1.")


def find_student(identifier):
    identifier = identifier.strip().upper()
    return next((s for s in students if str(s.student_id).upper() == identifier), None)


def choose_student():
    if not students:
        print("No student applications or records exist yet.")
        return None
    for i, student in enumerate(students, 1):
        print(
            f"{i}. {student.student_id} - {student.full_name} "
            f"({student.programme}, {student.current_level}) [{student.application_status}]"
        )
    choice = ask_number("Choose student number (0 to cancel): ", 0, len(students))
    return None if choice == 0 else students[choice - 1]


def choose_registration():
    student = choose_student()
    if student and not student.registration:
        print("This student has not started a semester registration yet.")
        return None
    return student


def ask_approval(prompt):
    while True:
        answer = ask(prompt + " (A)pprove or (R)eturn/reject? ").lower()
        if answer in ("a", "r"):
            return answer == "a"
        print("Enter A to approve or R to return/reject.")


def choose_programme():
    print("Available programmes:")
    for i, programme in enumerate(PROGRAMMES, 1):
        print(f"{i}. {programme}")
    index = ask_number("Choose programme number: ", 1, len(PROGRAMMES)) - 1
    return PROGRAMMES[index]


def student_application():
    """Allow a new student to submit their own application."""
    global next_application_number
    line()
    print("NEW STUDENT APPLICATION")
    line()

    name = ask_required("Full name (as on official documents): ")
    dob = ask_date()
    while True:
        email = ask_email()
        if any(student.email.lower() == email.lower() for student in students):
            print("An application with this email already exists. Enter another email or contact Registry.")
        else:
            break
    phone = ask_phone()
    programme = choose_programme()
    level = ask_level()
    semester = ask_semester()

    print("Funding options:")
    for i, item in enumerate(FUNDING_TYPES, 1):
        print(f"{i}. {item}")
    funding = FUNDING_TYPES[ask_number("Choose funding option number: ", 1, len(FUNDING_TYPES)) - 1]

    sponsor = ""
    if funding in ("Family/individual sponsor", "Organisation/scholarship", "Government-sponsored"):
        sponsor = ask_required("Sponsor/government scheme/organisation name: ")

    while True:
        password = ask_required("Create a password for your student account: ")
        confirm = ask_required("Confirm password: ")
        if password == confirm:
            break
        print("Passwords do not match. Please enter and confirm your password again.")

    app_ref = f"APP{next_application_number:05d}"
    next_application_number += 1
    student = Student(
        app_ref, name, email, programme, level, dob, phone,
        funding, sponsor, password, "AWAITING REGISTRY VERIFICATION"
    )
    students.append(student)
    student.intended_semester = semester

    print("\nApplication submitted successfully.")
    print(f"Your application reference is: {app_ref}")
    print("Keep this reference and your password. Registry must verify your details before official registration.")


def student_portal():
    line()
    print("STUDENT PORTAL")
    line()
    print("1. New student application\n2. Existing student login\n0. Back")
    action = ask("Choose: ")
    while action not in ("0", "1", "2"):
        print("Invalid choice. Enter 1, 2, or 0 to go back.")
        action = ask("Choose: ")

    if action == "1":
        student_application()
        return
    if action == "0":
        return

    student = None
    for attempt in range(1, 4):
        identifier = ask("Student ID or application reference: ").upper()
        password = ask("Password: ")
        candidate = find_student(identifier) if identifier else None
        if candidate and candidate.login_password == password:
            student = candidate
            break
        remaining = 3 - attempt
        if remaining:
            print(f"Login failed. Check your ID/reference and password. {remaining} attempt(s) remaining.")
        else:
            print("Too many failed attempts. Returning to the main menu; you can try again later.")
            return

    while True:
        line()
        print(f"STUDENT PORTAL — {student.full_name}")
        line()
        print(
            "1. View my details\n2. View my results\n3. View my assigned modules\n"
            "4. Start semester registration\n5. Submit payment/sponsorship reference\n"
            "6. Track application/registration\n7. Print registration form\n0. Log out"
        )
        choice = ask("Choose: ")

        if choice == "1":
            print(student.display_student_details())
            print(f"Date of birth: {student.date_of_birth}\nPhone: {student.phone}")
        elif choice == "2":
            print(student.display_results())
        elif choice == "3":
            if student.assigned_modules:
                print(f"Modules for {student.module_semester}:")
                for i, module in enumerate(student.assigned_modules, 1):
                    print(f"{i}. {module}")
            else:
                print("Modules are not configured for your programme, level and semester yet. Contact your Year Leader.")
        elif choice == "4":
            if student.application_status != "VERIFIED / ID ASSIGNED":
                print("Your details must be verified by Registry before you can start official semester registration.")
            else:
                semester = getattr(student, "intended_semester", "") or ask_semester()
                modules = year_leader.get_modules(student.programme, student.current_level, semester)
                if not modules:
                    print("No module list is configured for your programme, level and semester. Contact your Year Leader.")
                else:
                    student.save_assigned_modules(modules, semester)
                    try:
                        student.start_semester_registration(semester)
                        print(f"Registration started. {len(modules)} modules were assigned automatically.")
                    except ValueError as error:
                        print(error)
        elif choice == "5":
            registration = student.registration
            if not registration:
                print("Start registration after Registry verification and module assignment.")
            else:
                reference = ask_required("Payment receipt/reference or sponsorship clearance reference: ")
                try:
                    registration.submit_bank_slip_reference(reference)
                    print("Reference submitted for Finance verification.")
                except ValueError as error:
                    print(error)
        elif choice == "6":
            print(f"Application status: {student.application_status}")
            if student.registration:
                registration = student.registration
                print(
                    f"Registration: {registration.registration_status}\n"
                    f"Finance: {registration.finance_status}\n"
                    f"Faculty: {registration.faculty_status}\n"
                    f"Registry: {registration.registry_status}"
                )
            else:
                print("Semester registration has not started.")
        elif choice == "7":
            if not student.registration:
                print("No semester registration form is available yet.")
            else:
                form = student.registration.create_printable_registration_form()
                print(form)
                if ask("Save form as a text file? (y/n): ").lower() == "y":
                    filename = f"Registration_{student.student_id}.txt"
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(form)
                    print(f"Saved to {filename} in the current folder.")
        elif choice == "0":
            break
        else:
            print("Choose a listed option.")
        pause()


def year_leader_menu():
    while True:
        line()
        print("YEAR LEADER PORTAL")
        line()
        print(
            "1. List student applications/records\n2. Review results\n3. Enter/update a result\n"
            "4. Configure modules for a programme/year/semester\n5. View configured module lists\n0. Log out"
        )
        choice = ask("Choose: ")
        if choice == "0":
            break
        elif choice == "1":
            if students:
                for student in students:
                    print(student.display_student_details())
            else:
                print("No student applications or records yet.")
        elif choice in ("2", "3"):
            student = choose_student()
            if student:
                if choice == "2":
                    year_leader.review_results(student)
                else:
                    module = ask_required("Module name: ")
                    grade = ask_required("Grade/status (e.g. A, B, JNS): ")
                    print(year_leader.enter_or_update_result(student, module, grade))
        elif choice == "4":
            programme = choose_programme()
            level = ask_level("Academic year/level (e.g. Year 1): ")
            semester = ask_semester("Semester (e.g. Semester 1): ")
            modules = [m.strip() for m in ask_required("Enter module names separated by commas: ").split(",") if m.strip()]
            try:
                print(year_leader.configure_modules(programme, level, semester, modules))
            except ValueError as error:
                print(error)
        elif choice == "5":
            if not year_leader.module_catalogue:
                print("No module lists configured yet.")
            for (programme, level, semester), modules in year_leader.module_catalogue.items():
                print(f"{programme.title()} | {level.title()} | {semester.title()}: {', '.join(modules)}")
        else:
            print("Choose a listed option.")
        pause()


def finance_menu():
    while True:
        line()
        print("FINANCE OFFICER PORTAL")
        line()
        print("1. View registrations awaiting Finance\n0. Log out")
        choice = ask("Choose: ")
        if choice == "0":
            break
        elif choice == "1":
            pending = [s for s in students if s.registration and s.registration.finance_status == "PENDING VERIFICATION"]
            if not pending:
                print("No references are awaiting verification.")
            else:
                print("Registrations awaiting Finance:")
                for i, student in enumerate(pending, 1):
                    print(f"{i}. {student.student_id} - {student.full_name}: {student.registration.bank_slip_reference}")
                selected = ask_number("Choose pending registration number (0 to cancel): ", 0, len(pending))
                if selected:
                    student = pending[selected - 1]
                    approved = ask_approval("Verify payment/sponsorship reference?")
                    try:
                        print(finance_officer.verify_payment(student.registration, approved, ask("Finance note (optional): ")))
                    except ValueError as error:
                        print(error)
        else:
            print("Choose a listed option.")
        pause()


def faculty_menu():
    while True:
        line()
        print("FACULTY OFFICER PORTAL")
        line()
        print("1. View registrations awaiting Faculty\n0. Log out")
        choice = ask("Choose: ")
        if choice == "0":
            break
        elif choice == "1":
            pending = [
                s for s in students
                if s.registration and s.registration.finance_status == "VERIFIED"
                and s.registration.faculty_status == "PENDING"
            ]
            if not pending:
                print("No registrations are awaiting Faculty review.")
            else:
                for i, student in enumerate(pending, 1):
                    print(f"{i}. {student.student_id} - {student.full_name} ({student.registration.semester})")
                selected = ask_number("Choose pending registration number (0 to cancel): ", 0, len(pending))
                if selected:
                    student = pending[selected - 1]
                    approved = ask_approval("Approve this registration at Faculty stage?")
                    try:
                        print(faculty_officer.review_registration(student.registration, approved, ask("Faculty note (optional): ")))
                    except ValueError as error:
                        print(error)
        else:
            print("Choose a listed option.")
        pause()


def registry_menu():
    while True:
        line()
        print("REGISTRY OFFICER PORTAL")
        line()
        print(
            "1. View applications awaiting verification\n2. Verify application and assign official student ID\n"
            "3. Update student details\n4. List all records\n5. Final registration approval\n"
            "6. View approval history\n7. Generate registration status email text\n0. Log out"
        )
        choice = ask("Choose: ")
        if choice == "0":
            break
        elif choice == "1":
            pending = [s for s in students if s.application_status == "AWAITING REGISTRY VERIFICATION"]
            if not pending:
                print("No applications are awaiting verification.")
            for student in pending:
                print(student.display_student_details())
        elif choice == "2":
            student = choose_student()
            if student:
                if student.application_status != "AWAITING REGISTRY VERIFICATION":
                    print("This application has already been reviewed.")
                else:
                    print(student.display_student_details())
                    if ask("Have you checked the student's identity and documents? (y/n): ").lower() == "y":
                        official_id = ask_required("Assign official student ID: ").upper()
                        if any(s is not student and str(s.student_id).upper() == official_id for s in students):
                            print("That ID is already in use.")
                        else:
                            student.student_id = official_id
                            student.application_status = "VERIFIED / ID ASSIGNED"
                            print(f"Application verified. Official student ID {official_id} assigned to {student.full_name}.")
        elif choice == "3":
            student = choose_student()
            if student:
                student.full_name = ask(f"Full name [{student.full_name}]: ") or student.full_name
                new_email = ask(f"Email [{student.email}] (leave blank to keep): ")
                if new_email:
                    if re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", new_email):
                        student.email = new_email
                    else:
                        print("Invalid email; previous email kept.")
                new_phone = ask(f"Phone [{student.phone}] (leave blank to keep): ")
                if new_phone:
                    digits = re.sub(r"[ +()-]", "", new_phone)
                    if digits.isdigit() and 7 <= len(digits) <= 15:
                        student.phone = new_phone
                    else:
                        print("Invalid phone; previous phone kept.")
                print("Available programmes:")
                for i, programme in enumerate(PROGRAMMES, 1):
                    print(f"{i}. {programme}")
                programme_choice = ask("Programme number (leave blank to keep): ")
                if programme_choice:
                    if programme_choice.isdigit() and 1 <= int(programme_choice) <= len(PROGRAMMES):
                        student.programme = PROGRAMMES[int(programme_choice) - 1]
                    else:
                        print("Invalid programme choice; previous programme kept.")
                new_level = ask(f"Level [{student.current_level}] (leave blank to keep): ")
                if new_level:
                    match = re.fullmatch(r"(?:year\s*)?([1-6])", new_level, re.IGNORECASE)
                    if match:
                        student.current_level = f"Year {match.group(1)}"
                    else:
                        print("Invalid year; previous level kept.")
                print("Student details updated by Registry.")
        elif choice == "4":
            if not students:
                print("No records yet.")
            for student in students:
                print(student.display_student_details())
        elif choice == "5":
            student = choose_registration()
            if student:
                registration = student.registration
                print(
                    f"Current status: {registration.registration_status}; "
                    f"Finance: {registration.finance_status}; Faculty: {registration.faculty_status}"
                )
                approved = ask_approval("Give final Registry approval?")
                try:
                    print(registry_officer.give_final_approval(registration, approved, ask("Registry note (optional): ")))
                except ValueError as error:
                    print(error)
        elif choice == "6":
            student = choose_registration()
            if student:
                print("\n".join(student.registration.approval_history))
        elif choice == "7":
            student = choose_registration()
            if student:
                print(RegistrationEmail.create_registration_status_email(student.registration))
        else:
            print("Choose a listed option.")
        pause()


def staff_login():
    """Allow three attempts; blank passwords also count as attempts."""
    for attempt in range(1, 4):
        username = ask("Staff username: ").lower()
        password = ask("Password: ")
        account = ACCOUNTS.get(username)
        if account and password and password == account[1]:
            role = account[0]
            print(f"Welcome to the {role} portal.")
            menus = {
                "Year Leader": year_leader_menu,
                "Finance Officer": finance_menu,
                "Faculty Officer": faculty_menu,
                "Registry Officer": registry_menu,
            }
            menus[role]()
            return
        remaining = 3 - attempt
        if remaining:
            print(f"Login failed. Check your username and password. {remaining} attempt(s) remaining.")
        else:
            print("Too many failed attempts. Returning to the main menu; you can try again later.")


def main():
    while True:
        line()
        print("LIMKOKWING UNIVERSITY — STUDENT REGISTRATION SYSTEM")
        line()
        print("1. Student portal\n2. Staff login\n0. Exit")
        choice = ask("Choose: ")
        if choice == "1":
            student_portal()
        elif choice == "2":
            staff_login()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 0.")


if __name__ == "__main__":
    main()