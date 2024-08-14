""""generate question"""
import os
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "test-creator"
os.environ["LANGCHAIN_API_KEY"] = "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"

# Pydantic
class Question(BaseModel):
    """Question based on the context"""
    question: str = Field(description="Question based on excerpt or chunk from provided context, without relying on external knowledge or assumptions. Use only the information learned from the given context.")
    source: str = Field(description="The initial chunk or excerpt that the question is based on")


GENERATE_TEMPLATE = """{context}

-----------

Choose a chunk or excerpt from the preceding context, formulate a thoughtful question that builds upon the chunk or excerpt you chose. Please include both your inquiry and the original
excerpt in your response."""

GENERATE_PROMPT = ChatPromptTemplate.from_template(GENERATE_TEMPLATE)

def generate_question(context) -> [str]:
    """main"""
    model = ChatOllama(
        model="llama3-groq-tool-use",
        temperature=0.9,
        format="json"
    )
    structured_model = model.with_structured_output(Question)
    main_chain = GENERATE_PROMPT | structured_model

    output = []

    try:
        model_output = main_chain.invoke({'context': context})
        output.append(model_output.question)
        output.append(model_output.source)
    except Exception as e:
        print(f"Validation error: {e}")

    return output


if __name__ == "__main__":
    TEST_CONTEXT = """
    If we want the model to return a Pydantic object, we just need to pass in the desired Pydantic class. The key advantage of using Pydantic is that the model-generated output will be validated. Pydantic will raise an error if any required fields are missing or if any fields are of the wrong type.
    """
    print(generate_question(TEST_CONTEXT))
