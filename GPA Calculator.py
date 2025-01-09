def calculate_hs_gpa():
    """
    This program calculates a weighted GPA for grades 10, 11, or 12.

    Changes made:
      - All PBL courses (PBL Core, PBL AI, PBL Research, PBL Track, etc.) are set to required
        because everyone needs to take them.
      - There is at least one “other” elective in each grade that is truly optional;
        you can choose whether you take it or not.
    """

    # 1. Define the letter-grade-to-base-GPA mapping (Regular level).
    #    We add +0.5 if "Honor" (max_points = 4.5), +1.0 if "Advanced" (max_points = 5.0).
    letter_grade_map = {
        "A": 4.0,
        "A-": 3.7,
        "B+": 3.3,
        "B": 3.0,
        "B-": 2.7,
        "C+": 2.3,
        "C": 2.0,
        "C-": 1.7,
        "D+": 1.3,
        "D": 1.0,
        "F": 0.0
    }

    # 2. Define each grade’s courses.
    #
    # Fields:
    #   - name        (string)
    #   - credit      (float)
    #   - max_points  (float: 4.0=Regular, 4.5=Honors, 5.0=Advanced)
    #   - elective    (bool) -> False = required, True = optional

    # ----------------
    # GRADE 10 Courses
    # ----------------
    #   According to your structure:
    #     - Chinese Culture 10, History & Geography, English 10/Honor English, Chemistry/Honor Chemistry,
    #       Physics/AP Physics 1, Algebra 2/AP Pre-Calculus, PE & Health 10, PBL Core/AP Seminar,
    #       PBL Track, and an optional "Elective".
    #   For demonstration, we will reflect something close to your chart:
    courses_g10 = [
        # Required courses
        {"name": "Chinese", "credit": 0.5, "max_points": 4.0, "elective": False},
        {"name": "HAG (History & Geography)",
         "credit": 1.0, "max_points": 4.5, "elective": False},
        {"name": "English 10", "credit": 1.0, "max_points": 4.5, "elective": False},
        {"name": "Chemistry", "credit": 1.0, "max_points": 4.5, "elective": False},
        {"name": "Physics1", "credit": 1.0, "max_points": 5.0, "elective": False},
        {"name": "Pre-calculus", "credit": 1.0, "max_points": 5.0, "elective": False},
        {"name": "PE & Health 10", "credit": 0.5, "max_points": 4.0, "elective": False},
        # PBL = required
        {"name": "PBL Core (Seminar)",
         "credit": 0.5, "max_points": 5.0, "elective": False},
        {"name": "PBL AI", "credit": 0.5, "max_points": 5.0, "elective": False},

        # One optional elective
        {"name": "G10 Additional Elective",
         "credit": 1.0, "max_points": 4.0, "elective": True},
    ]

    # ----------------
    # GRADE 11 Courses
    # ----------------
    #   From your chart:
    #     - Chinese Culture 11, AP World History, AP English/Honor English, Honor Biology,
    #       AP Science Elective, AP Math Elective, PE & Health 11,
    #       PBL Research/AP Research, PBL Track, an optional Elective, etc.
    #   We'll keep the concept that PBL courses are required,
    #   and add one purely optional elective (CSA or “Other Elective”).
    courses_g11 = [
        # Required courses
        {"name": "Chinese 11", "credit": 0.5, "max_points": 4.0, "elective": False},
        {"name": "World History (AP)", "credit": 1.0, "max_points": 5.0, "elective": False},
        {"name": "English (AP/Honor)", "credit": 1.0, "max_points": 4.5, "elective": False},
        {"name": "Biology (Honor/AP)", "credit": 1.0, "max_points": 5.0, "elective": False},
        {"name": "Chemistry (AP)", "credit": 1.0, "max_points": 5.0, "elective": False},
        {"name": "Statistics (AP)", "credit": 1.0, "max_points": 5.0, "elective": False},
        {"name": "PE & Health 11", "credit": 0.5, "max_points": 4.0, "elective": False},

        # PBL courses = required
        {"name": "PBL Research", "credit": 0.5, "max_points": 5.0, "elective": False},
        {"name": "PBL AI", "credit": 0.5, "max_points": 5.0, "elective": False},

        # Optional elective
        {"name": "CSA (or Other Elective)",
         "credit": 1.0, "max_points": 5.0, "elective": True},
    ]

    # ----------------
    # GRADE 12 Courses
    # ----------------
    #   From your chart:
    #     - Chinese Culture 12, AP Humanities Elective, AP/Advance English Elective,
    #       AP Science Elective, AP/Advance Math Elective, PE and Health 12,
    #       PBL Track, and 2 additional electives.
    #   PBL = required; “Elective 1” and “Elective 2” remain optional.
    courses_g12 = [
        # Required
        {"name": "Chinese Culture 12", "credit": 0.5, "max_points": 4.0, "elective": False},
        {"name": "AP Humanities Elective", "credit": 1.0, "max_points": 5.0, "elective": False},
        {"name": "AP/Adv English Elective", "credit": 1.0, "max_points": 5.0, "elective": False},
        {"name": "AP Science Elective", "credit": 1.0, "max_points": 5.0, "elective": False},
        {"name": "AP/Adv Math Elective", "credit": 1.0, "max_points": 5.0, "elective": False},
        {"name": "PE & Health 12", "credit": 0.5, "max_points": 4.0, "elective": False},
        {"name": "PBL Track", "credit": 0.5, "max_points": 5.0, "elective": False},

        # Two optional electives
        {"name": "Elective 1", "credit": 1.0, "max_points": 4.5, "elective": True},
        {"name": "Elective 2", "credit": 1.0, "max_points": 4.5, "elective": True},
    ]

    # 3. Ask which grade to calculate
    grade_choice = input("Which grade’s GPA do you want to calculate? (10, 11, or 12): ").strip()
    if grade_choice == "10":
        courses = courses_g10
    elif grade_choice == "11":
        courses = courses_g11
    elif grade_choice == "12":
        courses = courses_g12
    else:
        print("Invalid choice. Please enter 10, 11, or 12.")
        return

    # 4. Prompt user for grades; handle required vs. optional courses
    total_quality_points = 0.0
    total_credits = 0.0

    print(f"\nEntering grades for Grade {grade_choice}...\n")
    for course in courses:
        if course["elective"]:
            # Ask if the user is taking this elective
            take_elective = input(f"Are you taking the elective '{course['name']}'? (Y/N): ").upper().strip()
            if take_elective not in ["Y", "YES"]:
                print(f"Skipping '{course['name']}'.\n")
                continue

        # Prompt for a letter grade
        while True:
            grade_input = input(
                f"Enter your letter grade for {course['name']} "
                f"(A, A-, B+, B, B-, C+, C, C-, D+, D, F): "
            ).upper().strip()

            if grade_input in letter_grade_map:
                base_gpa = letter_grade_map[grade_input]

                # Adjust if Honors (4.5) or Advanced (5.0)
                if abs(course["max_points"] - 4.0) < 0.001:
                    final_gpa = base_gpa  # Regular
                elif abs(course["max_points"] - 4.5) < 0.001:
                    final_gpa = base_gpa + 0.5  # Honors
                else:
                    final_gpa = base_gpa + 1.0  # Advanced

                # Accumulate
                total_quality_points += final_gpa * course["credit"]
                total_credits += course["credit"]
                break
            else:
                print("Invalid letter grade. Please try again.\n")

    # 5. Compute final GPA
    if total_credits > 0:
        final_gpa = total_quality_points / total_credits
    else:
        final_gpa = 0.0

    print(f"\nYour weighted GPA for Grade {grade_choice} is: {final_gpa:.2f}\n")


if __name__ == "__main__":
    calculate_hs_gpa()
