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

# Enhanced philosopher data with bios and voice profiles
PHILOSOPHERS = {
   "aristotle": {"name": "Aristotle", "style": "Systematic empiricism, virtue ethics", "voice": "Measured, categorizing", "key_concepts": ["virtue ethics", "golden mean"], "image": "🏛️", "color": "from-amber-500 to-yellow-600", "era": "classical", "bio": "Ancient Greek polymath who founded formal logic and virtue ethics", "voice_style": "deep, authoritative"},
   "plato": {"name": "Plato", "style": "Idealistic dialectics, forms theory", "voice": "Questioning, allegorical", "key_concepts": ["theory of forms", "philosopher king"], "image": "📚", "color": "from-blue-500 to-indigo-600", "era": "classical", "bio": "Founded the Academy in Athens, student of Socrates", "voice_style": "thoughtful, questioning"},
   "kant": {"name": "Immanuel Kant", "style": "Transcendental idealism, duty ethics", "voice": "Rigorous, methodical", "key_concepts": ["categorical imperative", "autonomy"], "image": "⚖️", "color": "from-gray-500 to-slate-600", "era": "classical", "bio": "Enlightenment philosopher who revolutionized moral philosophy", "voice_style": "precise, German accent"},
   "nietzsche": {"name": "Friedrich Nietzsche", "style": "Genealogical critique, value transvaluation", "voice": "Provocative, iconoclastic", "key_concepts": ["will to power", "übermensch"], "image": "⚡", "color": "from-purple-500 to-violet-600", "era": "classical", "bio": "Challenged conventional morality and religion", "voice_style": "intense, dramatic"},
   "marx": {"name": "Karl Marx", "style": "Historical materialism, class dialectics", "voice": "Critical, revolutionary", "key_concepts": ["class struggle", "alienation"], "image": "🔨", "color": "from-red-500 to-rose-600", "era": "classical", "bio": "Revolutionary theorist who analyzed capitalism", "voice_style": "passionate, German accent"},
   "mlk": {"name": "Martin Luther King Jr.", "style": "Moral urgency, nonviolent resistance", "voice": "Passionate, justice-demanding", "key_concepts": ["nonviolent resistance", "beloved community"], "image": "✊", "color": "from-green-500 to-emerald-600", "era": "classical", "bio": "Civil rights leader who advocated nonviolent resistance", "voice_style": "preacher cadence, inspirational"},
   "jesus": {"name": "Jesus Christ", "style": "Transformative love, paradoxical wisdom", "voice": "Revolutionary gentleness", "key_concepts": ["universal love", "golden rule"], "image": "✝️", "color": "from-sky-500 to-blue-600", "era": "classical", "bio": "Central figure of Christianity, teacher of love and forgiveness", "voice_style": "gentle, Aramaic accent"},
   "putin": {"name": "Vladimir Putin", "style": "Realpolitik, strategic patience", "voice": "Calculating, power-focused", "key_concepts": ["state sovereignty", "strategic patience"], "image": "🐻", "color": "from-gray-600 to-slate-700", "era": "contemporary", "bio": "Russian leader focused on geopolitical power", "voice_style": "measured, Russian accent"},
   "chomsky": {"name": "Noam Chomsky", "style": "Anti-imperial critique, media deconstruction", "voice": "Sharp, systematic", "key_concepts": ["manufacturing consent", "propaganda model"], "image": "📢", "color": "from-red-600 to-orange-600", "era": "contemporary", "bio": "Linguist and political critic of media manipulation", "voice_style": "intellectual, Boston accent"},
   "trump": {"name": "Donald Trump", "style": "Populist transactionalism, media manipulation", "voice": "Direct, combative", "key_concepts": ["America First", "deal-making"], "image": "🇺🇸", "color": "from-red-500 to-blue-500", "era": "contemporary", "bio": "Business mogul turned politician", "voice_style": "brash, New York accent"},
   "musk": {"name": "Elon Musk", "style": "Techno-optimism, first principles reasoning", "voice": "Ambitious, disruptive", "key_concepts": ["first principles", "sustainable energy"], "image": "🚀", "color": "from-purple-600 to-pink-600", "era": "contemporary", "bio": "Tech entrepreneur pushing space exploration", "voice_style": "energetic, South African accent"}
}

# In-memory storage for debates and saved analyses
saved_analyses = {}
debate_sessions = {}

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
       print(f"RSS Error: {e}")
       return [
           {"title": "Global Climate Accords Reshape International Relations", "description": "Diplomatic frameworks evolve as nations recalibrate environmental commitments", "source": "BBC", "publishedAt": "2025-06-27", "id": "climate01"},
           {"title": "Artificial Intelligence Governance Framework Emerges", "description": "Legislative apparatus addresses algorithmic accountability", "source": "Reuters", "publishedAt": "2025-06-27", "id": "ai01"}
       ]

def generate_commentary(philosopher_id, story, debate_context=None):
   philosopher = PHILOSOPHERS[philosopher_id]
   
   base_prompt = f"""You are {philosopher['name']}. Analyze: {story['title']} - {story['description']}

{f"Responding to this debate context: {debate_context}" if debate_context else ""}

Craft sophisticated, non-formulaic commentary. Structure:

Bold philosophical stance reflecting your unique framework
Explain reasoning - connect to foundational concepts
Contemporary relevance for 2025 audiences  
Three substantive observations (no numbering)
Sharp, unconventional final observation that challenges assumptions

Reject formulaic phrases. Use unexpected angles, precise language, provocative insights. 280 words maximum."""
   
   try:
       response = openai_client.chat.completions.create(
           model="gpt-3.5-turbo",
           max_tokens=450,
           messages=[{"role": "user", "content": base_prompt}]
       )
       return response.choices[0].message.content
   except Exception as e:
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
       
       # Save analysis
       analysis_id = f"{philosopher_id}_{story['id']}"
       saved_analyses[analysis_id] = {
           'philosopher': PHILOSOPHERS[philosopher_id]['name'],
           'commentary': commentary,
           'story': story,
           'timestamp': datetime.now().isoformat()
       }
       
       return jsonify({
           'philosopher': PHILOSOPHERS[philosopher_id]['name'],
           'commentary': commentary,
           'story': story,
           'color': PHILOSOPHERS[philosopher_id]['color'],
           'image': PHILOSOPHERS[philosopher_id]['image'],
           'voice_style': PHILOSOPHERS[philosopher_id]['voice_style'],
           'analysis_id': analysis_id
       })
   return jsonify({'error': 'Story not found'}), 404

@app.route('/api/debate/<philosopher1>/<philosopher2>/<story_id>')
def start_debate(philosopher1, philosopher2, story_id):
   stories = fetch_news()
   story = next((s for s in stories if s['id'] == story_id), None)
   if not story:
       return jsonify({'error': 'Story not found'}), 404
   
   # Generate initial responses
   response1 = generate_commentary(philosopher1, story)
   response2 = generate_commentary(philosopher2, story, f"{PHILOSOPHERS[philosopher1]['name']} argues: {response1}")
   
   debate_id = f"{philosopher1}_{philosopher2}_{story_id}"
   debate_sessions[debate_id] = {
       'philosophers': [philosopher1, philosopher2],
       'story': story,
       'exchanges': [
           {'philosopher': philosopher1, 'response': response1},
           {'philosopher': philosopher2, 'response': response2}
       ]
   }
   
   return jsonify({
       'debate_id': debate_id,
       'exchanges': debate_sessions[debate_id]['exchanges'],
       'philosophers': [PHILOSOPHERS[philosopher1], PHILOSOPHERS[philosopher2]]
   })

@app.route('/api/search/<query>')
def search_analyses(query):
   results = []
   for analysis_id, analysis in saved_analyses.items():
       if query.lower() in analysis['commentary'].lower() or query.lower() in analysis['story']['title'].lower():
           results.append(analysis)
   return jsonify(results)

@app.route('/api/related/<story_id>')
def get_related_stories(story_id):
   # Simple related story logic based on keywords
   stories = fetch_news()
   current_story = next((s for s in stories if s['id'] == story_id), None)
   if not current_story:
       return jsonify([])
   
   # Extract keywords from title
   keywords = current_story['title'].lower().split()
   related = []
   
   for story in stories:
       if story['id'] != story_id:
           story_words = story['title'].lower().split()
           if any(word in story_words for word in keywords if len(word) > 4):
               related.append(story)
   
   return jsonify(related[:3])

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001, debug=True)
