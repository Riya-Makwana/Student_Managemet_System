import csv
import os

CSV_FILE = "students.csv"

# ---------- STUDENT CLASS ----------
class Student:
    def __init__(self, name, grade, cls, marks):
        self.name = name
        self.grade = grade
        self.cls = cls
        self.marks = marks

    def average_marks(self, term):
        return sum(self.marks[term].values()) / 3

    def science_marks(self, term):
        return self.marks[term]["Science"]


# ---------- CSV FUNCTIONS ----------
def save_to_csv(student):
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(
                ["Name", "Grade", "Class", "Term", "Maths", "Science", "Art"]
            )

        for term, marks in student.marks.items():
            writer.writerow([
                student.name,
                student.grade,
                student.cls,
                term,
                marks["Maths"],
                marks["Science"],
                marks["Art"]
            ])


def load_students():
    students = []

    if not os.path.isfile(CSV_FILE):
        return students

    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)
        data = {}

        for row in reader:
            name = row["Name"]
            if name not in data:
                data[name] = {
                    "grade": row["Grade"],
                    "class": row["Class"],
                    "marks": {}
                }

            data[name]["marks"][row["Term"]] = {
                "Maths": int(row["Maths"]),
                "Science": int(row["Science"]),
                "Art": int(row["Art"])
            }

        for name, info in data.items():
            students.append(
                Student(name, info["grade"], info["class"], info["marks"])
            )

    return students


# ---------- LOGIC ----------
students = load_students()


def add_student():
    name = input("Enter Student Name: ")
    grade = input("Enter Grade: ")
    cls = input("Enter Class: ")

    marks = {}

    for i in range(1, 4):
        print(f"\nEnter Term {i} Marks")
        maths = int(input("Maths: "))
        science = int(input("Science: "))
        art = int(input("Art: "))

        marks[f"Term {i}"] = {
            "Maths": maths,
            "Science": science,
            "Art": art
        }

    student = Student(name, grade, cls, marks)
    students.append(student)
    save_to_csv(student)

    print("Student added successfully ✅")


def display_students():
    if not students:
        print("No students found")
        return

    for i, s in enumerate(students, start=1):
        print(f"\nStudent {i}")
        print("Name:", s.name)
        print("Grade:", s.grade)
        print("Class:", s.cls)
        print("Marks:", s.marks)


def max_average_marks():
    term = input("Enter Term (1/2/3): ")
    term = f"Term {term}"

    top_student = max(students, key=lambda s: s.average_marks(term))
    print("\nTop Student:", top_student.name)
    print("Average Marks:", top_student.average_marks(term))


def lowest_science_marks():
    term = input("Enter Term (1/2/3): ")
    term = f"Term {term}"

    low_student = min(students, key=lambda s: s.science_marks(term))
    print("\nLowest Science Marks:")
    print("Student:", low_student.name)
    print("Marks:", low_student.science_marks(term))


# ---------- MAIN MENU ----------
def run_system():
    while True:
        print("\n----- Student Management System -----")
        print("1. Add Student")
        print("2. View Students")
        print("3. Maximum Average Marks")
        print("4. Lowest Science Marks")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            max_average_marks()
        elif choice == "4":
            lowest_science_marks()
        elif choice == "5":
            print("Thank you ")
            break
        else:
            print("Invalid choice ")

run_system()
