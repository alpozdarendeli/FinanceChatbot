# Import necessary modules and classes.
from langchain.agents import AgentExecutor, AgentType, initialize_agent, load_tools
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.tools import Tool
from langchain_community.utilities import SerpAPIWrapper
from pydantic import BaseModel
from config import MAX_TOKENS, AGENT_MODEL_NAME, TEMPERATURE

# WebSearch class to handle the schema for web search queries.
class WebSearch(BaseModel):
    input: str

def initialize_search_agent(serp_api_key: str) -> AgentExecutor:
    """
    Initializes the web search agent.

    Args:
        serp_api_key (str): The API key for SerpAPI.

    Returns:
        AgentExecutor: An instance of the web search agent.
    """
    # Initialize the SerpAPIWrapper with the provided API key.
    serp_api_wrapper = SerpAPIWrapper(serpapi_api_key=serp_api_key)

    # Create a ChatOpenAI instance for the web search agent.
    web_search_llm = ChatOpenAI(
        model=AGENT_MODEL_NAME,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    # Define the tools required by the web search agent.
    tools = [Tool(
        name="webSearch",
        description="Tool for searching queries from google.com. Input should be detailed, including all relevant past conversation information.",
        args_schema=WebSearch,
        func=serp_api_wrapper.run,
    )]

    # Initialize a conversation buffer memory for storing chat history.
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # System message guiding the web search agent's behavior.
    system_message = (
        "You will be given a user query. You MUST call the webSearch tool to "
        "retrieve search results from google.com and provide a detailed and satisfactory answer. Call the tools only ONCE. Include URL links in your response."
    )
    memory.chat_memory.add_message(SystemMessage(content=system_message))

    # Initialize and return the web search agent.
    return initialize_agent(
        tools,
        web_search_llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        memory=memory,
        verbose=True,
    )

def initialize_finance_agent(serp_api_key: str) -> AgentExecutor:
    """
    Initializes the finance search agent.

    Args:
        serp_api_key (str): The API key for finance-related tools.

    Returns:
        AgentExecutor: An instance of the finance search agent.
    """
    # Create a ChatOpenAI instance for the finance search agent.
    llm = ChatOpenAI(
        model=AGENT_MODEL_NAME,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    # Load specific tools for finance-related queries.
    tools = load_tools(["google-scholar", "google-finance"], llm=llm, serp_api_key=serp_api_key)

    # Initialize a conversation buffer memory for storing chat history.
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # System message guiding the finance search agent's behavior.
    system_message = (
        "For user queries related to finance, use the financeSearch tool to retrieve relevant data or news. Call the tools only ONCE. Include URL links to financial reports or articles in your response."
    )
    memory.chat_memory.add_message(SystemMessage(content=system_message))

    # Initialize and return the finance search agent.
    return initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        memory=memory,
        verbose=True
    )

# JSON schemas for the web and finance search agent functions.
web_search_agent_func_schema = {
    "name": "webSearch",
    "description": "Tool for searching queries from google.com.",
    "parameters": {
        "type": "object",
        "properties": {
            "input": {"type": "string", "description": "The query to search for."},
        },
        "required": ["input"],
    },
}
finance_search_agent_func_schema = {
    "name": "financeSearch",
    "description": "Tool for fetching finance-related data and news.",
    "parameters": {
        "type": "object",
        "properties": {
            "input": {"type": "string", "description": "The finance-related query to process."},
        },
        "required": ["input"],
    },
}


    
