🎓 Study Buddy — Interactive AI Study Agent

An intelligent, tool-augmented learning assistant built with Streamlit and OpenAI's gpt-4o-mini. Study Buddy enables students to query study notes, create custom flashcards, generate quizzes, and search live facts on Wikipedia.

🌟 Features

🧠 - Autonomous Agent Loop: Uses OpenAI Function Calling to determine when and which tools to call in sequence.

📌 - Local Notes Search (search_notes): Instantly retrieves saved course concepts and explanations.

🎴 - Flashcard Creator (make_flashcards): Automatically formats key terms and definitions into study cards.

📝 - Quiz Generator (quiz_me): Generates interactive multiple-choice practice questions with answer keys.

🌐 - Live Wikipedia API (search_wikipedia): Queries live external data from Wikipedia for topics missing from local notes.

💬 - Conversation Memory & Streaming: Persists full chat context across turns and streams answers back with typewriter animation.

🔐 - Secure Key Management: Supports environment key configuration as well as dynamic user-supplied API key overrides in the sidebar.

🏗️ Project Architecture

study-buddy-agent/
├── app.py              # Main Streamlit application UI & agent execution loop
├── tools.py            # Custom agent tools, function schemas, and tool execution logic
├── requirements.txt    # Project dependencies for local run and Streamlit Cloud
├── pyproject.toml      # UV / Python environment config
├── .gitignore          # Git ignore rules protecting API keys and build artifacts
└── README.md           # Project documentation

