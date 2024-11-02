import os
os.environ["OPENAI_API_KEY"] = "my-openai-api-key"

from llama_index import (
    SimpleDirectoryReader,
    ServiceContext,
    get_response_synthesizer,
)
from llama_index.indices.document_summary import DocumentSummaryIndex
from llama_index.llms import OpenAI

chatgpt = OpenAI(temperature=0, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(llm=chatgpt, chunk_size=1024)

response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize", use_async=True
)
docs = SimpleDirectoryReader(
    input_files=[f"C:/Users/dhapd/OneDrive/바탕 화면/빅토익 실전 3000제 TEST2 해설.pdf"]
).load_data()

doc_summary_index = DocumentSummaryIndex.from_documents(
    docs,
    service_context=service_context,
    response_synthesizer=response_synthesizer,
    show_progress=True,
)

doc_summary_index.get_document_summary()