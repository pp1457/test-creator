"""load and split pdf"""
from langchain_community.document_loaders import PyPDFLoader

def load_and_split_pdf(filename):
    """main"""
    loader = PyPDFLoader(filename)
    data = loader.load_and_split()
    return data

if __name__ == "__main__":
    print(load_and_split_pdf("data/Segment_Tree.pdf"))
