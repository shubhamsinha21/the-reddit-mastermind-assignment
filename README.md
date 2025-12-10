# Reddit Mastermind – Automated Reddit Content Calendar Generator

## Overview

**Reddit Mastermind** automates the creation of Reddit content calendars for businesses. By simulating human-like interactions across multiple personas and subreddits, it generates posts and comments that drive engagement, upvotes, and inbound leads — reducing the manual workload of content planning and posting.

The project was built to produce high-quality, realistic content that businesses can trust to post without extensive oversight.


## Features

1. Automated Weekly Content Calendar
2. Generates posts and comments based on company info, personas, target subreddits, ChatGPT queries, and number of posts per week.

3. Multiple Personas Simulation
4. Creates realistic conversations between 2+ personas for authenticity.

5. Subreddit-Aware Content
6. Avoids overposting and ensures contextually relevant posts.

7. Future Week Generation
8. Ability to generate content calendars for subsequent weeks with a single click.

9. Quality-Focused
10.Content is designed to look natural, business-friendly, and human-like.
   

## Technology

**Backend**: Python

**Web App**: Streamlit (quick deployment, fully functional)

- Built with flexibility in mind — the frontend can be extended to React/JS if needed.


## How to use

1. **Run the app**
```bash
git clone https://github.com/shubhamsinha21/the-reddit-mastermind-assignment.git
cd reddit-mastermind
pip install -r requirements.txt
streamlit run app.py
```

2. **Provide Inputs**: (CSV OR EXCEL FILE SUPPORTED)

   - Company info
   - Personas (2+)
   - Subreddits
   - Keywords

Note - The csv or excel data gets converted into JSON format and then the values are passed into the logic. 


3. **Generate Content Calendar**: Click “Generate Week” to produce posts/comments.

4. **Simulate Subsequent Weeks**: Click “Generate Next Week” to create future calendars.



