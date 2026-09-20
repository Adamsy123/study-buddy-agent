# tools.py - Tool definitions & schema for Study Buddy AI Agent
import requests

# ----------------------------------------------------------------------
# 1. Mock Database (Notes)
# ----------------------------------------------------------------------
STUDY_NOTES = {
    "python": "Python is a high-level programming language known for readability. Key topics: lists, dicts, OOP, decorators, and generators.",
    "llm": "Large Language Models (LLMs) use transformer architectures. Core concepts: tokens, embeddings, context windows, and tool calling.",
    "biology": "Cellular respiration produces ATP from glucose through glycolysis, the Krebs cycle, and oxidative phosphorylation.",
}


# ----------------------------------------------------------------------
# 2. Tool Implementations
# ----------------------------------------------------------------------
def search_notes(topic: str) -> str:
    """Search personal study notes for a specific topic."""
    key = topic.lower().strip()
    for note_key, content in STUDY_NOTES.items():
        if note_key in key or key in note_key:
            return f"📌 **Notes found for '{note_key}'**:\n{content}"
    return f"No local study notes found for '{topic}'. Try searching Wikipedia."


def make_flashcards(topic: str, count: int = 3) -> str:
    """Generate study flashcards with Term and Definition."""
    cards = {
        "python": [
            ("Variable", "A named storage location in memory."),
            ("Function", "A block of organized, reusable code."),
            ("List", "An ordered, mutable collection of elements.")
        ],
        "llm": [
            ("Token", "A chunk of text processed by an LLM."),
            ("Temperature", "A parameter controlling randomness in generation."),
            ("System Prompt", "Instructions guiding model behavior.")
        ]
    }
    
    key = topic.lower().strip()
    topic_cards = cards.get(key, [
        (f"{topic.capitalize()} Concept 1", f"Core explanation of {topic} topic."),
        (f"{topic.capitalize()} Concept 2", f"Secondary takeaway regarding {topic}."),
        (f"{topic.capitalize()} Concept 3", f"Key term related to {topic}.")
    ])
    
    selected = topic_cards[:int(count)]
    formatted = [f"🎴 **Flashcard {i+1}**\n- **Term:** {term}\n- **Def:** {defn}" 
                 for i, (term, defn) in enumerate(selected)]
    return "\n\n".join(formatted)


def quiz_me(topic: str, count: int = 2) -> str:
    """Generate multiple-choice quiz questions with answer key."""
    return (
        f"📝 **Quiz on {topic.title()} ({count} Questions)**\n\n"
        f"**Q1:** What is the fundamental concept behind {topic}?\n"
        f"A) Option 1  |  B) Option 2  |  C) Option 3\n"
        f"*Answer:* A\n\n"
        f"**Q2:** Which of the following best describes an advanced application of {topic}?\n"
        f"A) Option A  |  B) Option B  |  C) Option C\n"
        f"*Answer:* B"
    )


def search_wikipedia(query: str) -> str:
    """[REAL API TOOL] Query live Wikipedia search for a summary."""
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + requests.utils.quote(query)
        response = requests.get(url, headers={"User-Agent": "StudyBuddyAgent/1.0"}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"🌐 **Wikipedia Summary for '{query}'**:\n{data.get('extract', 'No summary available.')}"
        return f"Wikipedia article not found for '{query}'."
    except Exception as e:
        return f"Error reaching Wikipedia API: {e}"


# ----------------------------------------------------------------------
# 3. Tool Schemas
# ----------------------------------------------------------------------
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_notes",
            "description": "Search internal study notes database for stored notes on a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Subject or topic name (e.g., 'python', 'llm')"}
                },
                "required": ["topic"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "make_flashcards",
            "description": "Create study flashcards with terms and definitions for revision.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Topic for the flashcards"},
                    "count": {"type": "integer", "description": "Number of cards to make (default 3)"}
                },
                "required": ["topic"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "quiz_me",
            "description": "Generate a multiple-choice practice quiz with answers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Subject for the quiz"},
                    "count": {"type": "integer", "description": "Number of questions to ask"}
                },
                "required": ["topic"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_wikipedia",
            "description": "Fetch live summary from Wikipedia for broader subjects or facts missing in local notes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term or concept to query on Wikipedia"}
                },
                "required": ["query"],
            },
        },
    },
]


# ----------------------------------------------------------------------
# 4. Tool Router
# ----------------------------------------------------------------------
def call_tool(name: str, args: dict) -> str:
    if name == "search_notes":
        return search_notes(**args)
    elif name == "make_flashcards":
        return make_flashcards(**args)
    elif name == "quiz_me":
        return quiz_me(**args)
    elif name == "search_wikipedia":
        return search_wikipedia(**args)
    return f"Unknown tool called: {name}"


# Self-test block
if __name__ == "__main__":
    print(search_notes("python"))
    print(search_wikipedia("Artificial Intelligence"))