from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# Tool to read a document
@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    return docs[doc_id]

# Tool to edit a document
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return f"Successfully updated document {doc_id}"

# Resource to return all document IDs
@mcp.resource(
    "docs://documents"
)
def list_docs():
    """Return a list of all document IDs"""
    return list(docs.keys())

# Resource to return the contents of a particular document
@mcp.resource(
    "docs://documents/{doc_id}"
)
def fetch_doc(doc_id: str):
    """Return the contents of a specific document"""
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]

# Prompt to rewrite a document in markdown format
@mcp.prompt(
    name="format_markdown",
    description="Rewrites the contents of the document in Markdown format."
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    content = docs[doc_id]
    prompt = f"""Your goal is to reformat the following document to be written with markdown syntax.

Document ID: {doc_id}
Current content:
{content}

Please rewrite this content using proper markdown formatting:
- Add headers where appropriate
- Use bullet points for lists
- Add emphasis with **bold** or *italic* text
- Structure the content logically
- Maintain the original meaning while improving readability

After formatting, use the 'edit_document' tool to update the document with the new markdown content."""
    
    # Return just the prompt text, not wrapped in message format
    return prompt

# Prompt to summarize a document
@mcp.prompt(
    name="summarize",
    description="Create a concise summary of the document content."
)
def summarize_document(
    doc_id: str = Field(description="Id of the document to summarize")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    content = docs[doc_id]
    prompt = f"""Please provide a concise summary of the following document:

Document ID: {doc_id}
Content:
{content}

Create a brief summary that captures the key points and main purpose of this document."""
    
    # Return just the prompt text, not wrapped in message format
    return prompt

if __name__ == "__main__":
    mcp.run(transport="stdio")