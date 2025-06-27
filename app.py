from flask import Flask, render_template, jsonify, request
import requests
import json
import openai
import anthropic
import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()
app = Flask(__name__)

openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
anthropic_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
gemini_model = genai.GenerativeModel('gemini-pro')

PHILOSOPHERS = {
    "aristotle": {"name": "Aristotle", "style": "Systematic empiricism, virtue ethics", "voice": "Measured, categorizing", "key_concepts": ["virtue ethics", "golden mean"], "image": "🏛", "color": "from-amber-500 to-yellow-600", "era": "classical"},
    "plato": {"name": "Plato", "style": "Idealistic dialectics, forms theory", "voice": "Questioning, allegorical", "key_concepts": ["theory of forms", "philosopher king"], "image": "📖", "color": "from-blue-500 to-indigo-600", "era": "classical"},
    "kant": {"name": "Immanuel Kant", "style": "Transcendental idealism, duty ethics", "voice": "Rigorous, methodical", "key_concepts": ["categorical imperative", "autonomy"], "image": "⚖", "color": "from-gray-500 to-slate-600", "era": "classical"},
    "nietzsche": {"name": "Friedrich Nietzsche", "style": "Genealogical critique, value transvaluation", "voice": "Provocative, iconoclastic", "key_concepts": ["will to power", "übermensch"], "image": "⚡", "color": "from-purple-500 to-violet-600", "era": "classical"},
    "marx": {"name": "Karl Marx", "style": "Historical materialism, class dialectics", "voice": "Critical, revolutionary", "key_concepts": ["class struggle", "alienation"], "image": "🔨", "color": "from-red-500 to-rose-600", "era": "classical"},
    "mlk": {"name": "Martin Luther King Jr.", "style": "Moral urgency, nonviolent resistance", "voice": "Passionate, justice-demanding", "key_concepts": ["nonviolent resistance", "beloved community"], "image": "✊🏿", "color": "from-green-500 to-emerald-600", "era": "classical"},
    "jesus": {"name": "Jesus Christ", "style": "Transformative love, paradoxical wisdom", "voice": "Revolutionary gentleness", "key_concepts": ["universal love", "golden rule"], "image": "✝", "color": "from-sky-500 to-blue-600", "era": "classical"},
    "putin": {"name": "Vladimir Putin", "style": "Realpolitik, strategic patience", "voice": "Calculating, power-focused", "key_concepts": ["state sovereignty", "strategic patience"], "image": "🐻", "color": "from-gray-600 to-slate-700", "era": "contemporary"},
    "chomsky": {"name": "Noam Chomsky", "style": "Anti-imperial critique, media deconstruction", "voice": "Sharp, systematic", "key_concepts": ["manufacturing consent", "propaganda model"], "image": "📣", "color": "from-red-600 to-orange-600", "era": "contemporary"},
    "trump": {"name": "Donald Trump", "style": "Populist transactionalism, media manipulation", "voice": "Direct, combative", "key_concepts": ["America First", "deal-making"], "image": "🇺🇸", "color": "from-red-500 to-blue-500", "era": "contemporary"},
    "musk": {"name": "Elon Musk", "style": "Techno-optimism, first principles reasoning", "voice": "Ambitious, disruptive", "key_concepts": ["first principles", "sustainable energy"], "image": "🚀", "color": "from-purple-600 to-pink-600", "era": "contemporary"}
}

def fetch_news():
    try:
        import feedparser
        feed = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")
        stories = []
        for entry in feed.entries[:11]:
            stories.append({
                "title": entry.title,
                "description": getattr(entry, "summary", "No description available"),
                "url": entry.link,
                "source": "BBC",
                "publishedAt": getattr(entry, "published", "2025-06-27"),
                "id": hashlib.md5(entry.title.encode()).hexdigest()[:8]
            })
        return stories
    except Exception as e:
        return [{"title": "Global Climate Summit", "description": "World leaders meet", "source": "BBC", "publishedAt": "2025-06-27", "id": "climate01"}]

def generate_commentary(philosopher_id, story, debate_context=None):
    philosopher = PHILOSOPHERS[philosopher_id]
    
    base_prompt = f"""You are {philosopher['name']}. Analyze this 2025 news: {story['title']} - {story['description']}

Be provocative, bold, and uncompromising. Give a hot take that only you would give. Use your most extreme philosophical positions. Be controversial and memorable.

Structure exactly as:

STANCE: [Your most provocative, unfiltered position - be bold and extreme]
REASONING: [Connect to your core concepts: {', '.join(philosopher['key_concepts'])} - be radical in your interpretation]  
RELEVANCE: [What this reveals about 2025's deeper failures or opportunities - be blunt]
INSIGHTS: [Three shocking observations that others won't dare say]
CONCLUSION: [A statement so bold it will be quoted and remembered]

Don't hold back. Be the version of yourself that would shock people at a dinner party."""
    
    try:
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=450,
            messages=[{"role": "user", "content": base_prompt}]
        )
        return response.content[0].text
    except Exception as e:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                max_tokens=450,
                messages=[{"role": "user", "content": base_prompt}]
            )
            return response.choices[0].message.content
        except Exception as e2:
            return f"**{philosopher['name']}:** This development merits rigorous intellectual examination."

@app.route('/')
def index():
    return render_template('index.html', philosophers=PHILOSOPHERS)

@app.route('/api/news')
def get_news():
    return jsonify(fetch_news())

@app.route('/api/commentary/<philosopher_id>/<int:story_index>')
def get_commentary(philosopher_id, story_index):
    stories = fetch_news()
    if story_index < len(stories):
        story = stories[story_index]
        commentary = generate_commentary(philosopher_id, story)
        
        return jsonify({
            'philosopher': PHILOSOPHERS[philosopher_id]['name'],
            'commentary': commentary,
            'story': story,
            'color': PHILOSOPHERS[philosopher_id]['color'],
            'image': PHILOSOPHERS[philosopher_id]['image']
        })
    return jsonify({'error': 'Story not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)