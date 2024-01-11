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
The required dependencies are listed in the requirements.txt file, including langchain, openai, and pydantic.

## Usage
Run main.py to start the chatbot application. This will initiate a GUI where users can input their queries, and the application will process and display the responses.

## Features
Web Search Agent: Handles general queries by performing web searches.
Finance Search Agent: Specifically designed to handle financial queries.
Dynamic Query Handling: Determines the type of query and routes it to the appropriate agent.
Customizable Agents: Agents can be initialized with different settings and tools.
## Dependencies
langchain and langchain_community: For agent functionalities and chat models.
openai: To interact with OpenAI's GPT models.
pydantic: For data validation and settings management.
## Configuration
The application requires configuration settings defined in config.py and keys.json:

MODEL_NAME, TEMPERATURE, MAX_TOKENS are set in config.py.
API keys for OpenAI and SERP are stored in keys.json.
