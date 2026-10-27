"""Year Leader responsibilities and module catalogue management."""
class YearLeader:
    def __init__(self):
        # Key: (programme, level/year, semester) -> list of module names.
        self.module_catalogue = {}

    def review_results(self, student):
        print(f"\nResults for {student.full_name} ({student.student_id})")
        print(student.display_results())
        review_codes = ("JNS", "ABS", "INC")
        flagged = [(m, g) for m, g in student.results.items() if g in review_codes]
        if flagged:
            print("\nThese results need human review:")
            for module, grade in flagged:
                print(f"- {module}: {grade}")
        else:
            print("No configured review codes found. Staff must still apply university rules.")

    def enter_or_update_result(self, student, module, grade):
        student.add_module_result(module, grade)
        return f"Result saved for {student.full_name}: {module} = {grade.upper()}"

    def configure_modules(self, programme, level, semester, modules):
        if not programme.strip() or not level.strip() or not semester.strip() or not modules:
            raise ValueError("Programme, level, semester and at least one module are required.")
        clean_modules = list(dict.fromkeys(m.strip() for m in modules if m.strip()))
        if not clean_modules:
            raise ValueError("Enter at least one valid module name.")
        key = (programme.strip().lower(), level.strip().lower(), semester.strip().lower())
        self.module_catalogue[key] = clean_modules
        return f"Configured {len(clean_modules)} module(s) for {programme}, {level}, {semester}."

    def get_modules(self, programme, level, semester):
        key = (programme.strip().lower(), level.strip().lower(), semester.strip().lower())
        return list(self.module_catalogue.get(key, []))

    def assign_modules(self, student, modules, semester):
        if not modules:
            raise ValueError("Enter at least one module.")
        student.save_assigned_modules(modules, semester)
        student.registration = None
        return f"Assigned {len(modules)} module(s) to {student.full_name} for {semester}."