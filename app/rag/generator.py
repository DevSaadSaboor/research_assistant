from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings

llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key)
summary_llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=settings.openai_api_key,
    max_tokens=8192,
)

# One-pass summarization works for short docs; longer PDFs use map-reduce below.
_SINGLE_PASS_LIMIT = 40_000
_MAP_CHUNK_SIZE = 50_000
_MAP_CHUNK_OVERLAP = 500


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
    You are an AI research assistant.
    Use only the provided context to answer the question.

    Context:
    {context}

    Question:
    {question}
    """
    response = llm.invoke(prompt)
    return response.content


def _summarize_section(text: str, section_number: int, section_total: int) -> str:
    prompt = f"""
    You are a research assistant.

    Summarize section {section_number} of {section_total} from a longer document.
    Write concise bullet points covering:
    - Main topics in this section
    - Important concepts
    - Key takeaways

    Use plain text only. Do not use markdown formatting.

    Section:
    {text}
    """
    return summary_llm.invoke(prompt).content


def _summarize_combined(text: str) -> str:
    prompt = f"""
    You are a research assistant.

    Combine the following section summaries into one cohesive document summary.

    Include:
    - Main topics (group related ideas; avoid repeating the same topic)
    - Important concepts
    - Key takeaways

    Use plain text with short paragraphs and simple dashes for lists.
    Do not use markdown formatting such as **bold** or headings with #.
    Finish every sentence completely.

    Section summaries:
    {text}
    """
    return summary_llm.invoke(prompt).content


def summarize_document(content: str) -> str:
    if not content.strip():
        return "No document content found."

    if len(content) <= _SINGLE_PASS_LIMIT:
        return _summarize_combined(content)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=_MAP_CHUNK_SIZE,
        chunk_overlap=_MAP_CHUNK_OVERLAP,
    )
    sections = splitter.split_text(content)
    section_summaries = [
        _summarize_section(section, index, len(sections))
        for index, section in enumerate(sections, start=1)
    ]
    combined = "\n\n".join(section_summaries)

    if len(combined) > _SINGLE_PASS_LIMIT:
        return summarize_document(combined)

    return _summarize_combined(combined)
