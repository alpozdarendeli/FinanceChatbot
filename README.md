# Financial Chatbot

## Introduction
This project is a chatbot application that leverages OpenAI's API, the SERP API, and Langchain tools to effectively manage user queries. Its primary objective is to distinguish between routine and financial inquiries and respond appropriately using specialized tools. The logic for distinguishing between routine and complex queries relies on OpenAI's API. When faced with routine queries, the chatbot performs web searches. In contrast, when dealing with intricate financial inquiries, it engages Langchain's agent, which conducts searches on Google Finance and Google Scholar to provide comprehensive responses.
## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)


## Installation
To set up this project, you need to install the required dependencies:

```bash
pip install -r requirements.txt
```
The required dependencies are listed in the requirements.txt file, including langchain, openai, and pydantic.

## Dependencies

- The required dependencies are listed in the `requirements.txt` file, including:
  - `langchain`
  - `openai`
  - `pydantic`
  - `google-search-results`

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

