""""generate question"""
import os
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_ollama import ChatOllama
from pydantic import ValidationError

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "test-creator"
os.environ["LANGCHAIN_API_KEY"] = "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"

# Pydantic
class Question(BaseModel):
    """Question based on the context"""

    question: str = Field(
        description=(
            "A question generated based on key sentences selected from the provided context. "
            "The model identifies crucial information within the context, isolates the most relevant "
            "sentences, and crafts a question that can be answered using only the content of these "
            "key sentences. The generated question should be clear, specific, and directly related to "
            "the extracted key sentences, ensuring that no external knowledge or assumptions are required."
        )
    )

    key_sentences: List[str] = Field(
        description=(
            "A list of short, precise key sentences extracted from the provided context. Each sentence should be short, concise, "
            "clear, and directly relevant to the answer of the generated question. The selected sentences "
            "should collectively contain all the information necessary to infer the correct answer, without "
            "relying on additional context or external knowledge. These sentences should be carefully chosen "
            "to ensure they are short and precise, effectively supporting the question-answering task."
        )
    )


GENERATE_TEMPLATE = """
{context}

-----------

From the context provided above, carefully extract key sentences that encapsulate the most crucial information. These sentences should be as SHORT as possible, concise, clear, and directly relevant to the main ideas presented. Once you have identified these key sentences, formulate a well-considered and precise question that can be answered solely based on the information within these sentences. Ensure the question is specific, focused, and directly tied to the selected text. In your response, include both the question and the key sentences to ensure clarity and context.
"""

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

    try:
        model_output = main_chain.invoke({'context': context})
        output = []
        output.append(model_output.question)
        output.append('; '.join(sentence for sentence in model_output.key_sentences))
        return output
    except ValidationError as e:
        print(f"Validation error: {e}")
        return []


if __name__ == "__main__":
    TEST_CONTEXT = """
    If we want the model to return a Pydantic object, we just need to pass in the desired Pydantic class. The key advantage of using Pydantic is that the model-generated output will be validated. Pydantic will raise an error if any required fields are missing or if any fields are of the wrong type.
    """
    print(generate_question(TEST_CONTEXT))
