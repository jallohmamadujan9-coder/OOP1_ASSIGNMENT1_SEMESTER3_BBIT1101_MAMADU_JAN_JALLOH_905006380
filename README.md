University Student Registration System

A role-based, console-driven prototype of a university registration workflow, written in Python. Students apply and register for a semester, and each registration moves through Year Leader, Finance, Faculty and Registry stages before it is approved.

Note: Educational prototype only. All records are stored in memory and are lost when the program exits. No real emails are sent.

Features
Student portal: apply as a new student, log in with an ID or application reference, view details and results, see assigned modules, start semester registration, submit a payment/sponsorship reference, track progress, and print or save a registration form.
Year Leader: configure module lists per programme, year and semester; enter and review student results.
Registry Officer: verify applications, assign official student IDs, update student details, give final approval, view approval history, and generate status email text.
Finance Officer: verify or reject submitted payment/sponsorship references.
Faculty Officer: approve or return registrations after Finance verification.
Input validation: email, phone, date of birth (DD/MM/YYYY), year and semester checks, plus three login attempts.
Registration Workflow
Student submits an application and receives a reference (e.g. APP00001).
Registry verifies the details and assigns an official student ID.
Student starts registration and modules are assigned automatically from the Year Leader's configuration.
Student submits a payment or sponsorship reference.
Finance verifies, then Faculty approves, then Registry gives final approval.
Any stage can return the registration for correction.
Project Structure
File	Purpose
main.py	Menus, input validation and program entry point
Student_Details.py	Student class (details, results, modules, registration)
Registration.py	Registration class (status tracking, printable form)
Year_Leader.py	YearLeader class (module catalogue, results)
Finance_Officer.py	FinanceOfficer class (payment verification)
Faculty_Officer.py	FacultyOfficer class (faculty review)
Registry_Officer.py	RegistryOfficer class (records, final approval)
Registration_Email.py	RegistrationEmail class (sample status email text)

Adjust file names to match your repository.

Getting Started

Requirements: Python 3.8 or newer. No external packages needed.

bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python main.py
Demo Staff Accounts
Role	Username	Password
Year Leader	yearleader	year123
Finance Officer	finance	finance123
Faculty Officer	faculty	faculty123
Registry Officer	registry	registry123

These are hard-coded demo credentials for testing only.

Suggested Test Run
Log in as yearleader and configure modules for a programme, year and semester.
In the student portal, submit a new application.
Log in as registry, verify the application and assign a student ID.
As the student, start registration and submit a payment reference.
Approve in order as finance, faculty, then registry.
As the student, print the registration form.

Author
Mamadu Jan Jalloh, Limkokwing University of Creative Technology, Sierra Leone.