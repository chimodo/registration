import csv
from csv import DictReader
import os

# ---------- Student Class ----------
class Student:
    def __init__(self, student_id, name, password, registered_courses=None):
        self.student_id = student_id
        self.name = name
        self.password = password
        self.registered_courses = set(registered_courses) if registered_courses else set()

# ---------- Course Class ----------
class Course:
    def __init__(self, course_id, name, instructor, max_students=30, subject="General Education"):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.enrolled_students = set()
        self.max_students = max_students
        self.subject = subject

# ---------- Enrollment System ----------
class EnrollmentSystem:
    def __init__(self):
        self.students = {}  # g_number: Student object
        self.courses = {}
        self.load_data()

    def load_data(self):
        # Load students
        if os.path.exists("students.csv"):
            with open("students.csv", newline='') as f:
                reader = DictReader(f)
                for row in reader:
                    g_number = row["g_number"]
                    name = row["name"]
                    password = row["password"]
                    self.students[g_number] = Student(g_number, name, password)

        # Load enrollments
        if os.path.exists("enrollments.csv"):
            with open("enrollments.csv", newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        student_id, course_id = row
                        if student_id in self.students:
                            self.students[student_id].registered_courses.add(course_id)

        # Load courses
        if os.path.exists("courses.csv"):
            with open("courses.csv", newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    course_id, name, instructor, *students = row
                    course = Course(course_id, name, instructor)
                    course.enrolled_students = set(students)
                    self.courses[course_id] = course

    def save_data(self):
        # Save students
        with open("students.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["g_number", "name", "password"])
            for student in self.students.values():
                writer.writerow([student.student_id, student.name, student.password])

        # Save courses
        with open("courses.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for course in self.courses.values():
                writer.writerow([course.course_id, course.name, course.instructor] + list(course.enrolled_students))

        # Save enrollments
        with open("enrollments.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for student in self.students.values():
                for course_id in student.registered_courses:
                    writer.writerow([student.student_id, course_id])

    def add_course(self, course_id, name, instructor, subject="General Education"):
        if course_id in self.courses:
            print("⚠️ Course already exists.")
        else:
            self.courses[course_id] = Course(course_id, name, instructor, subject)
            print("✅ Course added.")
            self.save_data()

    def enroll_student(self, student_id, course_id):
        if student_id not in self.students or course_id not in self.courses:
            print("⚠️ Invalid student or course ID.")
            return

        student = self.students[student_id]
        course = self.courses[course_id]

        if len(course.enrolled_students) >= course.max_students:
            print("❌ Course is full.")
            return

        if course_id in student.registered_courses:
            print("⚠️ Student already enrolled.")
            return

        student.registered_courses.add(course_id)
        course.enrolled_students.add(student_id)
        print("✅ Enrollment successful.")
        self.save_data()

    def drop_course(self, student_id, course_id):
        if student_id not in self.students or course_id not in self.courses:
            print("⚠️ Invalid student or course ID.")
            return

        student = self.students[student_id]
        course = self.courses[course_id]

        if course_id in student.registered_courses:
            student.registered_courses.remove(course_id)
            course.enrolled_students.discard(student_id)
            print("✅ Course dropped.")
            self.save_data()
        else:
            print("⚠️ Student is not enrolled in this course.")

    def view_available_courses(self):
        print("\n📚 Available Courses:")
        for course_id, course in self.courses.items():
            print(f"{course_id} - {course.name} | Instructor: {course.instructor} | Enrolled: {len(course.enrolled_students)}/{course.max_students}")
        print()

    def register_student(self):
        while True:
            student_id = input("Enter your new g number: ").strip()
            if student_id in self.students:
                print("⚠️ That G# is already registered. Try a different one.")
            else:
                name = input("Enter your name: ").strip()
                password = input("Create a password: ").strip()
                new_student = Student(student_id, name, password)
                self.students[student_id] = new_student
                print(f"✅ Student {name} registered successfully.")
                self.save_data()
                return new_student

    def student_login(self):
        while True:
            g_number = input("Enter your g number: ").strip()
            password = input("Enter your password: ").strip()

            if g_number in self.students and self.students[g_number].password == password:
                student = self.students[g_number]
                print(f"✅  Welcome, {student.name}!")
                return student
            else:
                print("⚠️ Incorrect password or g number")

# ---------- CLI ----------
def main():
    system = EnrollmentSystem()

    while True:
        try:
            print("\n🎓 UNIVERSITY COURSE REGISTRATION SYSTEM")
            print("1. Register a new student")
            print("2. login")

            choice = int(input("Enter a valid choice (1-2):").strip())
            if choice == 1:
                system.register_student()
                break
            elif choice == 2: 
                student = system.student_login()
                break
            else:
                print("⚠️ Enter a valid number!")
        except ValueError:
            print("⚠️ Enter a valid number!")

    while True:
        print("\n🎓 UNIVERSITY COURSE REGISTRATION SYSTEM")
        print("1. Register a new student")
        print("2. Add a new course")
        print("3. Enroll a student in a course")
        print("4. Drop a course for a student")
        print("5. View all available courses")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            system.register_student

        elif choice == "2":
            course_id = input("Enter course ID: ").strip()
            name = input("Enter course name: ").strip()
            instructor = input("Enter instructor name: ").strip()
            system.add_course(course_id, name, instructor)

        elif choice == "3":
            student_id = student.student_id
            course_id = input("Enter course ID to enroll: ").strip()
            system.enroll_student(student_id, course_id)

        elif choice == "4":
            student_id = student.student_id
            course_id = input("Enter course ID to drop: ").strip()
            system.drop_course(student_id, course_id)

        elif choice == "5":
            system.view_available_courses()

        elif choice == "6":
            print("👋 Exiting system. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter a number from 1 to 6.")

# ---------- Run the CLI ----------
if __name__ == "__main__":
    main()
