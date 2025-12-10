# Reddit Mastermind – Automated Reddit Content Calendar Generator

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-WebApp-orange)

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

- Takes **company info, personas, subreddits and ChatGPT prompts(keywords)** as input.  
- Generates **weekly content calendars** and **simulates persona interactions**.  
- Ensures **contextual relevance, natural conversations, and Reddit-specific etiquette**.  
- Can generate subsequent weeks with a single click.  

---

## ⚡ Technical Highlights

- **Backend:** Python 3  
- **Web App:** Streamlit  

**Features Implemented:**

- Automated content calendar generation  
- Multi-persona simulation  
- Subreddit-aware posting  
- Realistic comment generation  
- Cron/button simulation for generating future weeks  
- Configurable number of posts per week  

---

## 📁 Project Structure

- reddit-mastermind/
  - app.py → Streamlit main app
  - reddit_algorithm.py → Core content planning algorithm
  - data → Contains JSON file for inputs (company.json | subreddits.json | keywords.json | personnas.json
  - mock data → Contains sample csv & excel file of all inputs -> You can upload this files for testing else, create your own file
  - requirements.txt → Python dependencies
  - README.md → Project documentation
  - .gitignore → Git ignore file
  - weekly_comments.csv → Generates csv file for comments
  - weekly_posts.csv → Generated csv file for posts

---

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


✅ Testing & Quality Assurance

Multiple personas tested for authentic back-and-forth conversations

Edge cases handled: overposting, topic overlap, subreddit rules

Output quality evaluated on a 3–10 scale


⚡ Business Impact

- Saves hours of manual content creation
- Increases visibility and inbound leads
- Helps businesses rank on Reddit and even Google/LLM references
- Fully trustable content: minimal oversight required
- Continuous testing with varying company info, subreddits, and prompts


🛠 Getting Started

**Prerequisites**

- Python 3.11+
- Streamlit
- Check requirements.txt file


Installation 

```
https://github.com/shubhamsinha21/the-reddit-mastermind-assignment.git
cd reddit-mastermind
pip install -r requirements.txt
streamlit run app.py
```
