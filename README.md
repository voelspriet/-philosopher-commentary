# Philosophy Meets Current Events

A sophisticated web application that provides philosophical analysis of breaking news through the perspectives of history's greatest thinkers by Henk van Ess

## Overview

This tool transforms daily news into thoughtful philosophical discourse by generating AI-powered commentary from 11 different philosophical perspectives, ranging from ancient Greek philosophers to contemporary world leaders.

## Features

- **Real-time News Analysis**: Live BBC news feed with instant philosophical commentary
- **11 Philosophical Perspectives**: Classical thinkers (Aristotle, Plato, Kant, Nietzsche, Marx, MLK Jr., Jesus) and contemporary voices (Putin, Chomsky, Trump, Musk)
- **Academic Journal Design**: Elegant typography, serif fonts, and professional layout
- **Comparative Analysis**: Side-by-side perspectives from multiple philosophers
- **Dynamic Sentiment Analysis**: Context-aware interpretation of each philosopher's approach
- **Historical Context**: Connects current events to each thinker's historical era

## Screenshots

The interface features a prestigious journal aesthetic with:
- Editorial board selection with philosopher initials
- Clean article cards with academic styling
- Detailed analysis pages with pull quotes and structured sections

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/philosophy-current-events.git
cd philosophy-current-events
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=your_openai_key
# ANTHROPIC_API_KEY=your_anthropic_key
# GEMINI_API_KEY=your_gemini_key
```

4. Run the application:
```bash
python app.py
```

Visit `http://localhost:5001` to access the application.

## Usage

1. **Select Philosopher**: Choose from the Editorial Board on the left
2. **Analyze News**: Click "Analyze" on any current affairs article
3. **Compare Perspectives**: Use "Comparative Analysis" to see multiple viewpoints
4. **Read Analysis**: Enjoy structured philosophical commentary with:
   - Contemporary Analysis
   - Philosophical Position
   - Key Observations
   - Philosophical Framework
   - Historical Context

## API Structure

The application uses a simple Flask backend with three main endpoints:

- `GET /` - Main interface
- `GET /api/news` - BBC RSS feed integration
- `GET /api/commentary/<philosopher>/<story_index>` - Generate philosophical analysis

## Technologies

- **Backend**: Python Flask
- **Frontend**: Vanilla JavaScript with Tailwind CSS
- **AI Integration**: OpenAI GPT, Anthropic Claude, Google Gemini
- **News Source**: BBC RSS feed
- **Fonts**: SF Pro (Apple system fonts) and Crimson Text (serif)

## Philosophical Approach

Each philosopher provides analysis structured as:
- **STANCE**: Core philosophical position
- **REASONING**: Connection to key philosophical concepts
- **RELEVANCE**: Application to 2025 society
- **INSIGHTS**: Specific observations
- **CONCLUSION**: Memorable final thought

The prompts encourage bold, authentic takes that reflect each thinker's unique worldview.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- BBC News for RSS feed
- OpenAI, Anthropic, and Google for AI models
- Stanford Encyclopedia of Philosophy for biographical information