# Financial Chatbot

## Introduction

This project presents a  chatbot application, integrating OpenAI's advanced API and Assistant with Langchain tools and the SERP API. It's designed to adeptly navigate and respond to a diverse range of user queries, utilizing two key functionalities: `FinanceSearch` and `WebSearch`.

## Core Features

### FinanceSearch

Tailored for complex financial inquiries, `FinanceSearch` activates Langchain's agent capabilities. It performs in-depth searches across platforms like Google Finance and Google Scholar. This tool specializes in fetching detailed financial data, market trends, and scholarly articles, ensuring users receive well-rounded and insightful financial information.

### WebSearch

For general or routine queries, the chatbot employs `WebSearch`. This function utilizes the vast scope of the internet to conduct thorough searches, returning relevant and timely information from a broad array of sources. This ensures users get accurate, up-to-date responses for non-financial queries.

## Integration and Functionality

The chatbot intelligently determines the nature of each query. It then selectively activates either `FinanceSearch` or `WebSearch`, aligning its search strategy with the query's context. This integration facilitates precise and relevant information retrieval, making the chatbot a versatile tool for various informational needs.

---

This project bridges the gap between advanced AI conversational abilities and specialized information retrieval, providing users with a reliable, multifaceted assistant for diverse inquiries. Whether it's detailed financial advice or general knowledge, the chatbot is adept at delivering concise, accurate, and contextually appropriate responses.

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

