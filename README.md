# Multimodal AI Assistant

A versatile AI assistant that combines text, voice, and file input capabilities with Gemini AI and weather information integration.

## Features

- Text input for regular queries
- Voice input with speech-to-text conversion
- File upload and analysis support
- Google Gemini AI integration
- Real-time weather information
- Conversation history tracking

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))
- OpenWeatherMap API key (get it from [OpenWeatherMap](https://openweathermap.org/api))
- PyAudio (required for voice input)

### PyAudio Installation
- Windows: `pip install PyAudio`
- Linux: `sudo apt-get install python3-pyaudio`
- macOS: `brew install portaudio && pip install PyAudio`

## Installation

1. Clone and setup:
```bash
git clone <your-repository-url>
cd AI-HACK
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.sample .env
# Edit .env with your API keys
```

## Configuration

Required environment variables:
```plaintext
GEMINI_API_KEY=your_gemini_api_key_here
WEATHER_API_KEY=your_openweathermap_api_key_here
```

## Project Structure

```
AI-HACK/
├── .env.sample           # Template for environment variables
├── .gitignore           # Git ignore rules
├── config.py            # Configuration and API keys
├── utils/
│   ├── __init__.py
│   ├── api_handler.py   # API interaction handlers
│   └── context_manager.py # Conversation context management
├── app.py              # Main Streamlit application
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Usage

1. Launch the app:
```bash
streamlit run app.py
```

2. Open `http://localhost:8501`

3. Choose input mode:
   - Text: Type queries
   - Voice: Speak commands
   - File: Upload for analysis

4. For weather information, include "weather" in your query:
   Example: "What's the weather in London?"

## Error Handling

The application includes comprehensive error handling for:
- API failures
- File upload issues
- Voice recognition errors
- Missing API keys

## Logging

All operations are logged to `app.log` with timestamps and error details.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
