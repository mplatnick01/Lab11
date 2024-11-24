import matplolib.pyplot as plt


# Data containers
students = {}
assignments = {}
submissions = {}

# Paths to data
data_dir = "data"
students_file = os.path.join(data_dir, "students.txt")
assignments_file = os.path.join(data_dir, "assignments.txt")
submissions_dir = os.path.join(data_dir, "submissions")


# Function to load student data
def load_students(file_path):
    with open(file_path, "r") as f:
        for line in f:
            student_id = line[:3]
            student_name = line[3:].strip()
            students[student_id] = student_name


# Function to load assignment data
def load_assignments(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            assignment_id = lines[i + 1].strip()
            points = int(lines[i + 2].strip())
            assignments[assignment_id] = {"name": name, "points": points}


# Function to load submissions data
def load_submissions(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        with open(file_path, "r") as f:
            for line in f:
                student_id, assignment_id, percentage = line.strip().split(",")
                percentage = float(percentage)
                if assignment_id not in submissions:
                    submissions[assignment_id] = []
                submissions[assignment_id].append((student_id, percentage))


# Menu Option 1: Calculate student grade
def calculate_student_grade():
    student_name = input("What is the student's name: ").strip()
    student_id = None

    # Find student ID
    for id, name in students.items():
        if name.lower() == student_name.lower():
            student_id = id
            break

    if student_id is None:
        print("Student not found")
        return

    # Calculate grade
    total_score = 0
    for assignment_id, scores in submissions.items():
        for sid, percentage in scores:
            if sid == student_id:
                points = assignments[assignment_id]["points"]
                total_score += (percentage / 100) * points

    grade_percentage = round((total_score / 1000) * 100)
    print(f"{grade_percentage}%")


# Menu Option 2: Assignment statistics
def assignment_statistics():
    assignment_name = input("What is the assignment name: ").strip()
    assignment_id = None

    # Find assignment ID
    for aid, details in assignments.items():
        if details["name"].lower() == assignment_name.lower():
            assignment_id = aid
            break

    if assignment_id is None:
        print("Assignment not found")
        return

    # Calculate statistics
    scores = [score for _, score in submissions[assignment_id]]
    min_score = round(min(scores))
    avg_score = round(sum(scores) / len(scores))
    max_score = round(max(scores))

    print(f"Min: {min_score}%")
    print(f"Avg: {avg_score}%")
    print(f"Max: {max_score}%")


# Menu Option 3: Generate histogram
def generate_histogram():
    assignment_name = input("What is the assignment name: ").strip()
    assignment_id = None

    # Find assignment ID
    for aid, details in assignments.items():
        if details["name"].lower() == assignment_name.lower():
            assignment_id = aid
            break

    if assignment_id is None:
        print("Assignment not found")
        return

    # Generate histogram
    scores = [score for _, score in submissions[assignment_id]]
    plt.hist(scores, bins=[0, 25, 50, 75, 100], edgecolor="black")
    plt.title(f"Score Distribution for {assignment_name}")
    plt.xlabel("Score Ranges")
    plt.ylabel("Frequency")
    plt.show()


# Main menu
def main():
    # Load data
    load_students(students_file)
    load_assignments(assignments_file)
    load_submissions(submissions_dir)

    # Display menu
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    choice = input("Enter your selection: ").strip()

    if choice == "1":
        calculate_student_grade()
    elif choice == "2":
        assignment_statistics()
    elif choice == "3":
        generate_histogram()
    else:
        print("Invalid selection")


if __name__ == "__main__":
    main()
