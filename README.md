# Financial Chatbot

## Introduction
This project is a  chatbot application that utilizes OpenAI's GPT models and SERP APIs to handle user queries. It is designed to differentiate between trivial and financial queries and responds using relevant tools.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation
To set up this project, you need to install the required dependencies:

```bash
pip install -r requirements.txt
```
The required dependencies are listed in the requirements.txt file, including langchain, openai, and pydantic.

## Usage

- To run the chatbot application, execute `main.py`. This will launch a graphical user interface (GUI) where users can input their queries, and the application will process and display responses.

## Features

- **Web Search Agent:** Handles general queries by performing web searches.
- **Finance Search Agent:** Specifically designed to handle financial queries.
- **Dynamic Query Handling:** Determines the type of query and routes it to the appropriate agent.
- **Customizable Agents:** Agents can be initialized with different settings and tools.

## Configuration

- The application requires configuration settings defined in two files:
  - `config.py`: Contains settings like `MODEL_NAME`, `TEMPERATURE`, and `MAX_TOKENS`.
  - `keys.json`: Stores API keys for OpenAI and SERP.

## Documentation

- The codebase is well-structured and includes comments explaining key functionalities. For detailed understanding, refer to each file and the inline comments.

## Examples

- Here's an example of initializing and using a search agent:

```python
web_search_agent = initialize_search_agent(serp_api_key="your-serp-api-key")
response = web_search_agent.invoke({"input": "your query"})
****
response = web_search_agent.invoke({"input": "your query"})

