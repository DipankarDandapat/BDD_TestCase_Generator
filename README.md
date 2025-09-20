# BDD Test Case Generator

A complete multi-agent system that transforms plain English requirements into comprehensive BDD (Behavior-Driven Development) test cases using AI-powered agents.

## Features

- **Multi-Agent System**: Powered by UserProxyAgent and BDD Writer Agent working together
- **AI-Powered**: Uses advanced language models to understand and generate test scenarios
- **Comprehensive Coverage**: Generates positive, negative, and edge case scenarios automatically
- **Interactive UI**: Modern, responsive web interface with real-time feedback
- **Download Support**: Generated feature files can be copied or downloaded

## Architecture

The system consists of two main agents:

1. **UserProxyAgent**: Orchestrates the conversation and executes tools
2. **BDD_TEST_CASE_CREATOR**: Specialized agent for generating BDD feature files

## Project Structure

```
bdd-generator/
├── app.py                 # Flask API + agent orchestration
├── agents.py              # Autogen agent definitions
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (OpenAI API key)
├── static/
│   ├── style.css          # Modern CSS styling
│   └── main.js            # Interactive JavaScript functionality
└── templates/
    └── index.html         # Main UI template
```

## Installation

1. Clone or extract the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```
   Or create a `.env` file with:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Enter your requirement in plain English in the textarea

4. Click "Generate BDD Test Cases"

5. View the generated Gherkin feature file

6. Copy the content or download the `.feature` file

## Example Input

```
As a user, I want to be able to login to the system using my email and password so that I can access my personal dashboard. The system should validate credentials and handle scenarios like invalid email format, wrong password, and account lockout.
```

## Example Output

The system will generate a complete Gherkin feature file with scenarios covering:
- Successful login
- Invalid email format
- Wrong password
- Account lockout
- Empty fields
- SQL injection attempts
- And more edge cases

## API Endpoints

- `GET /` - Main application page
- `POST /generate` - Generate BDD test cases from requirement
- `GET /download/<filename>` - Download generated feature file
- `GET /health` - Health check endpoint

## Technologies Used

- **Backend**: Flask, Python
- **AI Framework**: AutoGen (Microsoft)
- **Language Model**: OpenAI GPT-4o-mini
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Styling**: Modern CSS with gradients and animations

## Configuration

The system uses OpenAI's GPT-4o-mini model by default. You can modify the model configuration in `agents.py`:

```python
import os
config_list = [{
    "model": "gpt-4o-mini",  # Change this to use different models
    "api_key": os.getenv("OPENAI_API_KEY")
}]
```

## Troubleshooting

1. **Model not supported error**: Make sure you're using a supported OpenAI model name
2. **API key issues**: Verify your OpenAI API key is correctly set
3. **Port conflicts**: If port 5000 is in use, modify the port in `app.py`

## License

This project is provided as-is for educational and development purposes.

