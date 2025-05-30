# XAI ChatGPT CLI

A command-line interface for interacting with Grok AI, featuring streaming responses and conversation history.

## Features

- Interactive CLI chat interface with Grok AI
- Streaming responses for a more natural conversation experience
- Conversation history management
- System role configuration for specialized AI responses
- Error handling and graceful fallbacks
- Unit tests with mocked API calls

## Prerequisites

- Python 3.8 or higher
- XAI API Key (set in `.env` file)

## Installation

1. Clone the repository:
```bash
git clone git@github.com:addhe/xai-chatgpt-cli.git
cd xai-chatgpt-cli
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your XAI API key:
```bash
XAI_API_KEY=your_api_key_here
```

## Usage

Run the chat interface:
```bash
python main.py
```

- Type your message and press Enter to send
- The AI's response will be streamed character by character
- Type 'exit()' to end the conversation

## Running Tests

Run the test suite:
```bash
python -m pytest test_main.py -v
```

For coverage report:
```bash
python -m pytest test_main.py --cov=main
```

## Project Structure

- `main.py` - Main application code
- `test_main.py` - Unit tests
- `requirements.txt` - Project dependencies
- `.env` - Environment variables (not tracked in git)

## Author

Addhe Warman Putra (Awan)
