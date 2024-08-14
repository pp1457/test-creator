from langchain_community.document_loaders import PyMuPDFLoader

def load_and_split_pdf(filename) -> :
    loader = PyMuPDFLoader(filename)
    data = loader.load_and_split()
    return data
