# Reddit Mastermind – Automated Reddit Content Calendar Generator

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-WebApp-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-teal)

---

## Automate Reddit Content Planning & Drive Engagement

**Reddit Mastermind** helps businesses scale their Reddit presence by automating content calendars, posts, and persona-driven comments — all designed to generate engagement, upvotes, and inbound leads.  

Instead of manually planning and posting content, this tool allows companies to simulate human-like Reddit interactions, save time, and focus on business growth.

---

## 📌 Who This Is For

- Marketing teams managing multiple Reddit accounts  
- Businesses aiming for increased engagement and inbound leads  
- Agencies handling Reddit content for clients  
- Anyone looking to automate content creation with **high-quality, human-like posts**  

---

## 🎯 Key Differentiator

**End-to-end planning algorithm for Reddit content**  

- Takes **company info, personas, subreddits, ChatGPT prompts, and post frequency** as input.  
- Generates **weekly content calendars** and **simulates persona interactions**.  
- Ensures **contextual relevance, natural conversations, and Reddit-specific etiquette**.  
- Can generate subsequent weeks with a single click.  

---

## ⚡ Technical Highlights

- **Backend:** Python 3  
- **Web App:** Streamlit  
- **AI:** OpenAI GPT-3.5/GPT-4 for content generation  
- **Data Processing:** pandas, numpy  

**Features Implemented:**

- Automated content calendar generation  
- Multi-persona simulation  
- Subreddit-aware posting  
- Realistic comment generation  
- Cron/button simulation for generating future weeks  
- Configurable number of posts per week  

---

## 📁 Project Structure

reddit-mastermind/
│
├── app.py # Streamlit main app
├── reddit_algorithm.py # Core content planning algorithm
├── helpers.py # Utility functions for input/output
├── requirements.txt # Python dependencies
├── sample_inputs/ # Sample input data
│ └── sample_input.json
├── sample_outputs/ # Sample generated content calendars
│ └── sample_calendar.json
├── README.md # Project documentation
└── .gitignore


**Folder Purpose:**

- `app.py` – Main Streamlit app, handles user inputs and output display.  
- `reddit_algorithm.py` – Contains the planning algorithm for generating calendars and comments.  
- `helpers.py` – Reusable helper functions (JSON handling, formatting, validations).  
- `sample_inputs/` – Example input files to test the algorithm.  
- `sample_outputs/` – Generated sample content calendars for reference.  

---

## 🚀 How It Works

1. **Provide Inputs**  
   - Company info  
   - Personas (2+)  
   - Subreddits  
   - ChatGPT prompts/queries  
   - Number of posts per week  

2. **Generate Weekly Content Calendar**  
   - Algorithm generates posts and comments based on inputs.  
   - Ensures **natural conversations** and avoids **overlapping topics**.  

3. **Simulate Future Weeks**  
   - Click **“Generate Next Week”** to produce subsequent weeks.  

---

### User Flow

```mermaid
flowchart TD
    A[User provides inputs] --> B[Algorithm generates post ideas]
    B --> C[Simulate persona comments]
    C --> D[Generate weekly content calendar]
    D --> E[Display in Streamlit app]
    E --> F[User can generate subsequent weeks]


{
  "week": 1,
  "posts": [
    {
      "title": "Which AI tools help create slides faster?",
      "subreddit": "r/AItools",
      "persona": "Alex_Marketing",
      "body": "Looking for AI tools that produce business-friendly slides efficiently.",
      "comments": [
        {
          "persona": "Sara_Consult",
          "comment": "I tried slidesmart.ai, and it saved me hours fixing slide layouts!"
        },
        {
          "persona": "John_Designer",
          "comment": "SlidesAI helped me structure slides faster while maintaining design quality."
        }
      ]
    }
  ]
}
```


✅ Testing & Quality Assurance

Multiple personas tested for authentic back-and-forth conversations

Edge cases handled: overposting, topic overlap, subreddit rules

Output quality evaluated on a 3–10 scale


⚡ Business Impact

Saves hours of manual content creation

Increases visibility and inbound leads

Helps businesses rank on Reddit and even Google/LLM references

Fully trustable content: minimal oversight required
Continuous testing with varying company info, subreddits, and prompts


🛠 Getting Started
Prerequisites

Python 3.11+

Streamlit

OpenAI API Key


Installation 

```
git clone https://github.com/<your-username>/reddit-mastermind.git
cd reddit-mastermind
pip install -r requirements.txt
streamlit run app.py
```

🙏 Acknowledgments

OpenAI – GPT-powered content generation

Streamlit – Web app interface

Python – Core backend

Reddit – Platform inspiration for content
