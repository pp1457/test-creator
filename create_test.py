"""create test"""
import os
from tqdm import tqdm
from load_and_split_pdf import load_and_split_pdf
from generate_question import generate_question
from write_to_csv import write_to_csv

def validate_pdf_file(filename):
    if not os.path.exists(filename):
        print(f"Error: The file {filename} does not exist.")
        return False

    _, ext = os.path.splitext(filename)

    if not ext.lower() == ".pdf":
        print(f"Error: The file {filename} is not a pdf file.")
        return False

    return True



def main():
    """main"""
    pdf_filename = "data/" + input("File you want to create test: ")

    if not validate_pdf_file(pdf_filename):
        return

    number_of_questions = int(input("The number of questions you want to generate on each page: "))

    chunks = load_and_split_pdf(pdf_filename)
    fields = ["question", "source", "file", "page"]
    rows = []

    pbar = tqdm(total=len(chunks) * number_of_questions)

    for chunk in chunks:
        for i in range(number_of_questions):
            question_source_list = generate_question(chunk.page_content)
            if not question_source_list:
                print(f"The model failed to generate question {i} of page {chunk.page}")
                continue

            question_source_list.append(chunk.metadata["source"])
            question_source_list.append(chunk.metadata["page"])
            rows.append(question_source_list)

            pbar.update(1)

    pbar.close()

    print("Generation Complete")
    result_filename = "result/" + input("File you want to save the result: ")

    write_to_csv(result_filename, fields, rows)

if __name__ == "__main__":
    main()
