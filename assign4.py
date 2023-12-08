import os
INPUT_DATA_FOLDER = "data/input/"
OUTPUT_DATA_FOLDER = "data/output/"
SCORE_THRESHOLD = 67
def main() -> None:
    """
    Orchestrates the execution of the program, taking user input for file names.
    Reads applicant data from the input file, identifies qualified applicants, and
    writes their data to the output file.
    """
    input_filename = input(f"Please provide the name of the input file (located in {INPUT_DATA_FOLDER}): ")
    output_filename = input(f"Please provide the name of the output file (to be placed in {OUTPUT_DATA_FOLDER}): ")
    applicant_list = open_and_convert_input_file_to_a_list(input_filename, "\t")
    qualified_applicants = get_qualified_applicants(applicant_list)
    print(f"\nThere were {len(qualified_applicants)} qualified applicants")
    write_qualified_applicants_to_file(output_filename, qualified_applicants)

def open_and_convert_input_file_to_a_list(filename: str, delimiter: str) -> list:
    absolute_path = os.path.dirname(__file__)
    relative_path = INPUT_DATA_FOLDER + filename
    full_path = os.path.join(absolute_path, relative_path)

    lines_list = []

    with open(full_path, 'r') as reader:
        line = reader.readline()
        while line != '':
            line = line.strip().split(delimiter)
            lines_list.append(line)
            line = reader.readline()

    return lines_list

def get_qualified_applicants(applicant_list: list) -> list:
    qualified_applicants = []

    for applicant in applicant_list[1:]:
        score = calculate_total_score(applicant)
        if score >= SCORE_THRESHOLD:
            qualified_applicants.append(applicant)

    return qualified_applicants

def calculate_total_score(applicant: list) -> int:
    language_skills_score = calculate_language_skills_score(applicant[4:8])
    education_score = calculate_education_score(applicant[9])
    work_experience_score = calculate_work_experience_score(applicant[11])
    age_score = calculate_age_score(int(applicant[2]))
    arranged_employment_score = calculate_arranged_employment_score(applicant[12])
    adaptability_scores = calculate_adaptability_score(applicant[13:19])

    total_score = (
        language_skills_score +
        education_score +
        work_experience_score +
        age_score +
        arranged_employment_score +
        adaptability_scores  # Fix: Sum the adaptability scores
    )

    print(f"Total Score for {applicant[0]} {applicant[1]}: {total_score}")

    return total_score

def calculate_language_skills_score(language_skills: list) -> int:
    speaking, listening, reading, writing = map(int, language_skills)

    if speaking >= 9 and listening >= 9 and reading >= 9 and writing >= 9:
        return 24
    elif speaking == 8 and listening == 8 and reading == 8 and writing == 8:
        return 20
    elif speaking == 7 and listening == 7 and reading == 7 and writing == 7:
        return 16
    else:
        return 0

def calculate_education_score(education: str) -> int:
    if "Secondary school" in education:
        return 5
    elif "One-year degree, diploma, or certificate" in education:
        return 15
    elif "Two-year degree, diploma, or certificate" in education:
        return 19
    elif "Bachelor's degree or other programs (three or more years)" in education:
        return 21
    elif "Two or more certificates, diplomas, or degrees" in education:
        return 22
    elif "Professional degree needed to practice in a licensed profession" in education:
        return 23
    elif "University degree at the Master's level" in education:
        return 23
    elif "University degree at the Doctoral (PhD) level" in education:
        return 25
    else:
        return 0

def calculate_work_experience_score(work_experience: str) -> int:
    if work_experience.lower() == 'no':
        return 0
    elif work_experience.isdigit():  # Check if the string is a non-negative integer
        experience_years = int(work_experience)
        if experience_years < 1:
            return 0
        elif experience_years == 1:
            return 9
        elif 2 <= experience_years <= 3:
            return 11
        elif 4 <= experience_years <= 5:
            return 13
        else:
            return 15
    else:
        return 0

def calculate_age_score(age: int) -> int:
    if 18 <= age <= 35:
        return 12
    elif age == 36:
        return 11
    elif age == 37:
        return 10
    elif age == 38:
        return 9
    elif age == 39:
        return 8
    elif age ==40:
        return 7
    elif age == 41:
        return 6
    elif age == 42:
        return 5
    elif age == 43:
        return 4
    elif age == 44:
        return 3
    elif age == 45:
        return 2
    elif age == 46:
        return 1
    elif age >= 47:
        return 0

def calculate_arranged_employment_score(arranged_employment: str) -> int:
    if arranged_employment.lower() == 'yes':
        return 10
    else:
        return 0
def calculate_adaptability_score(adaptability: list) -> int:
    if len(adaptability) < 6:
        return 0
    adaptability += [False] * (7 - len(adaptability))
    spouse_language, spouse_education, spouse_work, you_education, you_work, you_employment, relatives = adaptability

    # Handle 'N/A' for relatives
    if (relatives, bool):
        relatives = 'n/a'
    
    score = 0
    if spouse_language:
        score += 5
    if spouse_education:
        score += 5
    if spouse_work:
        score += 5
    if you_education:
        score += 5
    if you_work:
        score += 10
    if you_employment:
        score += 5
    if relatives.lower() in ['yes', 'n/a']:
        score += 5

    return score

def write_qualified_applicants_to_file(output_filename: str, qualified_applicants: list) -> None:
    absolute_path = os.path.dirname(__file__)
    relative_path = OUTPUT_DATA_FOLDER + output_filename
    full_path = os.path.join(absolute_path, relative_path)
    with open(full_path, 'w') as writer:
        # Assuming you want to write the qualified applicants to the file
        for applicant in qualified_applicants:
            writer.write(f"{', '.join(map(str, applicant))}\n")
main()
