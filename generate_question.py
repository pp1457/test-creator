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


class Question(BaseModel):
    """Question based on the context"""

    question: str = Field(
        description=(
            "A concise, short answer question generated based on key sentences directly selected from the provided context. "
            "This question should be clear and specific, allowing it to be answered exclusively using the information contained within the key sentences. "
            "The question should not require any external knowledge or assumptions, ensuring that it can be addressed with a brief, precise response."
        )
    )

    key_sentences: List[str] = Field(
        description=(
            "A list of key sentences that are directly extracted from the provided context. These sentences should be short, clear, "
            "and collectively contain all the information necessary to answer the generated question. The selection of these sentences "
            "is crucial, as they must enable the question to be answered solely based on their content, without relying on any additional "
            "context or external information. The key sentences should be highly relevant and directly tied to the question and its answer."
        )
    )

    
    keywords: List[str] = Field(
        description=(
            "A list of critical keywords or phrases that are directly extracted from the key sentences. These keywords are essential "
            "for answering the short answer question and should encapsulate the most important concepts or information specifically related to the question. "
            "Avoid including broad or general terms that represent the main idea or topic of the entire document. "
            "The selection of these keywords is crucial, as they should represent the core elements required to accurately understand and answer the question, "
            "focusing solely on the specific details needed for the response."
        )
    )

    answer: str = Field(
        description=(
            "The correct and concise answer to the short answer question, which should be fully inferable from the key sentences. "
            "This answer must not rely on any information outside of what is provided in the key sentences, ensuring that the question "
            "can be answered solely based on the given context."
        )
    )


GENERATE_TEMPLATE = """

{context}

-----------

Based on the context provided above, perform the following steps:

1. **Extract Key Sentences**: Identify and extract key sentences directly from the context. These sentences should encapsulate the most crucial information, and they must be as SHORT as possible, concise, and clear. The selected sentences should collectively provide all the information necessary to answer a specific question. Ensure that these sentences are directly relevant to the main ideas presented and that no additional context or external knowledge is required.

2. **Formulate a Precise Question**: Using only the information from the extracted key sentences, craft a well-considered and precise short answer question. The question should be specific, focused, and clearly related to the key sentences. It should be answerable solely based on the information provided within these sentences, without the need for any outside knowledge or assumptions.

3. **Identify Critical Keywords**: Extract keywords from the key sentences that are essential for answering the short answer question. These keywords should represent the core elements of the key sentences and be critical to understanding and formulating the answer.

4. **Provide the Answer**: Based on the key sentences and keywords, provide a concise and accurate answer to the formulated question. Ensure that the answer is fully derived from the key sentences and does not rely on any external information.

In your response, include the following:

- **Question**: The well-considered, precise question that can be answered exclusively using the key sentences.
- **Key Sentences**: The short, concise sentences extracted directly from the context.
- **Keywords**: The critical keywords or phrases directly taken from the key sentences, which are necessary for answering the question.
- **Answer**: The concise and accurate answer to the question, fully derived from the key sentences.

Ensure clarity and consistency in your response, maintaining a strong connection between the context, key sentences, question, keywords, and answer.
"""

GENERATE_PROMPT = ChatPromptTemplate.from_template(GENERATE_TEMPLATE)

def generate_question(context) -> [str]:
    """main"""
    ollama_endpoint = "http://localhost:23456"
    model = ChatOllama(
        base_url=ollama_endpoint,
        model="llama3-groq-tool-use:70b",
        temperature=0.9,
        format="json",
    )
    structured_model = model.with_structured_output(Question)
    main_chain = GENERATE_PROMPT | structured_model

    try:
        model_output = main_chain.invoke({'context': context})
        if not model_output:
            return []
        output = []
        output.append(model_output.question)
        output.append('; '.join(sentence for sentence in model_output.key_sentences))
        output.append('; '.join(keyword for keyword in model_output.keywords))
        output.append(model_output.answer)
        return output
    except ValidationError as e:
        print(f"Validation error: {e}")
        return []


if __name__ == "__main__":
    TEST_CONTEXT = """
    If we want the model to return a Pydantic object, we just need to pass in the desired Pydantic class. The key advantage of using Pydantic is that the model-generated output will be validated. Pydantic will raise an error if any required fields are missing or if any fields are of the wrong type.
    """
    print(generate_question(TEST_CONTEXT))
