import retriever
from retriever import run_similarity_search
from langchain.agents import tool

# Tool 1 : Get the Context from the database
class GetTools():
    @tool("Get Context Tool")
    def context(query: str) -> str:
        """Search Pinecone DB for relevant information based on a query."""
        retriever = run_similarity_search(query)
        return retriever
    

    def tools():
        return [
        GetTools.context
        ]
        
