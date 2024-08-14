"""create test"""
from tqdm import tqdm
from load_and_split_pdf import load_and_split_pdf
from generate_question import generate_question
from write_to_csv import write_to_csv


def main():
    """main"""
    pdf_filename = "data/" + input("File you want to create test: ")
    chunks = load_and_split_pdf(pdf_filename)
    fields = ["question", "source", "file", "page"]
    rows = []

    pbar = tqdm(total=len(chunks))

    for chunk in chunks:
        question_source_list = generate_question(chunk.page_content)
        if not question_source_list:
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
