# Import necessary modules and classes from various libraries.
from langchain.agents import AgentExecutor, AgentType, initialize_agent, load_tools
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.tools import Tool
from langchain_community.utilities import SerpAPIWrapper
from pydantic import BaseModel
from config import MAX_TOKENS, MODEL_NAME, TEMPERATURE

# Define the WebSearch class which will serve as the schema for web search queries.
class WebSearch(BaseModel):
    input: str

# Function to initialize the web search agent.
def initialize_search_agent(serp_api_key: str) -> AgentExecutor:
    # Initialize the SerpAPIWrapper with the provided API key.
    serp_api_wrapper = SerpAPIWrapper(serpapi_api_key=serp_api_key)  # type: ignore

    # Create a ChatOpenAI instance for the web search agent.
    web_search_llm = ChatOpenAI(
        model=MODEL_NAME,
        client=None,
        temperature=TEMPERATURE,
        streaming=False,
        max_tokens=MAX_TOKENS,
    )

    # Define the tools required by the web search agent.
    tools = [
        Tool(
            name="webSearch",
            description="Tool for searching queries from google.com"
            "Input is a string",
            args_schema=WebSearch,
            func=serp_api_wrapper.run,
        )
    ]

    # Initialize a conversation buffer memory for storing chat history.
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Add a system message to the memory to guide the web search agent's behavior.
    web_search_agent_system_message = (
        "You will be given a user query and you MUST call the webSearch tool to "
        "get back search results from google.com and provide a concise answer back to the user. You are only allowed to call the tools "
        "at most two times or less. You MUST NOT ask for clarifications, just make a reasonable choice yourself."
        "You MUST add the URL links to the search results in your response.")
    memory.chat_memory.add_message(
        SystemMessage(
            content=web_search_agent_system_message,
        )
    )

    # Initialize and return the web search agent.
    web_search_agent = initialize_agent(
        tools,
        web_search_llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        memory=memory,
        verbose=True,
    )

    return web_search_agent

# Function to initialize the finance search agent.
def initialize_finance_agent(serp_api_key: str) -> AgentExecutor:
    # Create a ChatOpenAI instance for the finance search agent.
    llm = ChatOpenAI(
       model=MODEL_NAME,
       temperature=TEMPERATURE,
       max_tokens=MAX_TOKENS,
    )

    # Load specific tools for finance-related queries.
    tools = load_tools(["google-scholar", "google-finance"], llm=llm, serp_api_key=serp_api_key)

    # Initialize a conversation buffer memory for storing chat history.
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Add a system message to guide the finance search agent's behavior.
    finance_agent_system_message = (
        "You will be provided with a user query related to financial information. You MUST call the financeSearch tool to retrieve relevant finance data or news. You are only allowed to call the tools "
        "at most two times or less. You MUST NOT ask for any clarifications; instead, make a reasonable choice based on the user's query. In your response, include pertinent data or news summaries. YOU MUST INCLUDE URL links to detailed financial reports or articles.")

    memory.chat_memory.add_message(
        SystemMessage(
            content=finance_agent_system_message,
        )
    )

    # Initialize and return the finance search agent.
    finance_search_agent = initialize_agent(
        tools,
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory, 
        verbose=True
    )
    return finance_search_agent

# Define JSON schemas for the web and finance search agent functions.
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
            "query": {"type": "string", "description": "The finance-related query to process."},
        },
        "required": ["query"],
    },
}


    
