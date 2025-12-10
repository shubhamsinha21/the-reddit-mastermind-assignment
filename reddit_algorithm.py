# reddit_algorithm.py
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Tuple

DATA_DIR = Path("data")

# ------------------------------
# Helpers / Normalizers
# ------------------------------
def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_company(raw: Any) -> Dict:
    if not raw or not isinstance(raw, dict):
        return {"name": "Company", "description": "", "subreddits": [], "num_posts_per_week": 3}
    c = {}
    name = raw.get("name") or raw.get("Name") or raw.get("Website") or raw.get("website") or raw.get("website_url")
    c["name"] = str(name) if name else "Company"
    desc = raw.get("Description") or raw.get("description") or raw.get("desc") or raw.get("about")
    c["description"] = str(desc) if desc else ""
    subs = raw.get("Subreddits") or raw.get("subreddits") or raw.get("subreddit")
    if subs is None:
        c["subreddits"] = []
    elif isinstance(subs, list):
        c["subreddits"] = [s.strip() for s in subs if isinstance(s, str) and s.strip()]
    elif isinstance(subs, str):
        parts = [p.strip() for p in (subs.replace(",", "\n").splitlines()) if p.strip()]
        c["subreddits"] = parts
    else:
        c["subreddits"] = []
    n = raw.get("Number of posts per week") or raw.get("number_of_posts_per_week") or raw.get("num_posts") or raw.get("num_posts_per_week")
    try:
        c["num_posts_per_week"] = max(1, int(n))
    except Exception:
        c["num_posts_per_week"] = 3
    return c

def normalize_personas(raw: Any) -> List[Dict]:
    if not raw:
        return []
    out = []
    if isinstance(raw, dict):
        raw = [raw]
    for idx, item in enumerate(raw, start=1):
        if isinstance(item, str):
            out.append({
                "username": item.strip(),
                "background": "",
            })
            continue
        if not isinstance(item, dict):
            continue
        username = item.get("username") or item.get("Username") or item.get("user") or item.get("handle")
        if not username:
            for k, v in item.items():
                if isinstance(v, str) and "@" not in v and len(v) <= 30:
                    username = v
                    break
        background = item.get("background") or item.get("Background") or item.get("Info") or item.get("info") or item.get("bio") or item.get("description") or ""
        out.append({
            "username": str(username).strip() if username else f"user_{idx}",
            "background": str(background).strip() if background else ""
        })
    return out

def normalize_subreddits(raw: Any) -> List[str]:
    if not raw:
        return []
    if isinstance(raw, list):
        return [s.strip() for s in raw if isinstance(s, str) and s.strip()]
    if isinstance(raw, str):
        parts = [p.strip() for p in (raw.replace(",", "\n").splitlines()) if p.strip()]
        return parts
    return []

def normalize_keywords(raw: Any) -> List[Dict]:
    if not raw:
        return []
    keywords = []
    if isinstance(raw, list):
        if raw and isinstance(raw[0], str):
            for idx, kw in enumerate(raw, start=1):
                keywords.append({"id": f"K{idx}", "text": kw})
            return keywords
        for idx, item in enumerate(raw, start=1):
            if isinstance(item, dict):
                kw_id = item.get("id") or item.get("keyword_id") or f"K{idx}"
                kw_text = item.get("text") or item.get("keyword") or item.get("label") or ""
                keywords.append({"id": kw_id, "text": kw_text})
            else:
                keywords.append({"id": f"K{idx}", "text": str(item)})
        return keywords
    if isinstance(raw, dict):
        for idx, (k, v) in enumerate(raw.items(), start=1):
            keywords.append({"id": f"K{idx}", "text": str(v)})
        return keywords
    return [{"id": "K1", "text": str(raw)}]

# ------------------------------
# Public getters with safe defaults
# ------------------------------
def get_company() -> Dict:
    company = normalize_company(load_json(DATA_DIR / "company.json"))
    if not company.get("name"):
        company["name"] = "Company"
    return company

def get_personas() -> List[Dict]:
    personas = normalize_personas(load_json(DATA_DIR / "personas.json"))
    if not personas:
        personas = [
            {"username": "jordan_consults", "background": "product consultant"},
            {"username": "emily_econ", "background": "marketing analyst"},
            {"username": "riley_ops", "background": "ops and presentations"},
            {"username": "alex_sells", "background": "sales"},
        ]
    for p in personas:
        if "voice" not in p:
            b = (p.get("background") or "").lower()
            if "consult" in b or "product" in b:
                p["voice"] = {"tone": "helpful", "brief": False, "quirk": ""}
            elif "marketing" in b or "sales" in b:
                p["voice"] = {"tone": "supportive", "brief": True, "quirk": "😊"}
            elif "ops" in b or "presentation" in b:
                p["voice"] = {"tone": "practical", "brief": True, "quirk": ""}
            else:
                p["voice"] = {"tone": "neutral", "brief": False, "quirk": ""}
    return personas

def get_subreddits() -> List[str]:
    raw = normalize_subreddits(load_json(DATA_DIR / "subreddits.json"))
    if raw:
        return raw
    company_raw = load_json(DATA_DIR / "company.json")
    if company_raw:
        subs = normalize_subreddits(company_raw.get("Subreddits") or company_raw.get("subreddits"))
        if subs:
            return subs
    return ["r/PowerPoint", "r/Canva", "r/GoogleSlides", "r/AItools", "r/presentations"]

def get_keywords() -> List[Dict]:
    keywords = normalize_keywords(load_json(DATA_DIR / "keywords.json"))
    if not keywords:
        keywords = [
            {"id": "K1", "text": "best AI presentation maker"},
            {"id": "K2", "text": "ai slide deck tool"},
            {"id": "K3", "text": "pitch deck generator"},
            {"id": "K4", "text": "alternatives to PowerPoint"},
            {"id": "K5", "text": "how to make slides faster"},
            {"id": "K6", "text": "export Google Slides reliably"},
            {"id": "K7", "text": "slidesmart.ai efficiency"},
        ]
    return keywords

# ------------------------------
# Subreddit templates
# ------------------------------
SUBREDDIT_TEMPLATES = {
    "r/PowerPoint": {
        "titles": [
            "Best AI Presentation Maker?",
            "Slide tools for polished PowerPoint decks?",
            "Anyone automated PowerPoint slide design?"
        ],
        "bodies": [
            "Just like it says in the title, what is the best AI tool for producing editable PowerPoint slides? Looking for high-quality output I can tweak.",
            "Trying to speed up producing PowerPoint decks — any tools that generate slides I can edit afterwards?",
            "What do people use to generate PowerPoint slides quickly while keeping control over layout?"
        ],
        "comment_style": "practical"
    },
    "r/Canva": {
        "titles": [
            "Slideforge vs Canva for slides?",
            "How do you automate layouts in Canva?",
            "Can an AI generate Canva-ready slides?"
        ],
        "bodies": [
            "I love Canva but spend ages adjusting templates. Anyone tried tools that give a decent Canva import?",
            "Trying to combine AI + Canva for quick visual decks — what's your workflow?",
            "Looking for tools that output something I can drop into Canva and polish."
        ],
        "comment_style": "designer"
    },
    "r/ClaudeAI": {
        "titles": [
            "Claude vs Slideforge for slide creation?",
            "Using Claude to generate slides — any tips?",
        ],
        "bodies": [
            "Using Claude for brainstorming is great, but the slide outputs need a lot of cleanup. Does anyone have good workflows?",
            "Trying to pair Claude with a slide generator — recommendations?"
        ],
        "comment_style": "tech"
    },
    "r/GoogleSlides": {
        "titles": [
            "Slide outputs — how well do they import to Google Slides?",
            "Generating Google Slides automatically — what works?"
        ],
        "bodies": [
            "I export generated decks into Google Slides and adjust spacing. Any tips to reduce manual fixes?",
            "Which slide generators give the most reliable Google Slides output?"
        ],
        "comment_style": "practical"
    },
    "r/AItools": {
        "titles": [
            "Which AI slide maker actually saves time?",
            "Best AI slide tool for business decks?"
        ],
        "bodies": [
            "Testing new AI slide makers — which one saves the most time without making terrible layouts?",
            "Looking for AI tools that produce business-friendly decks. Experiences?"
        ],
        "comment_style": "tech"
    },
    "r/presentations": {
        "titles": [
            "How do you automate presentation design?",
            "Tips for faster slide creation?"
        ],
        "bodies": [
            "Trying to improve our presentation workflow — any tools or tips that cut design time?",
            "Looking for techniques to speed up making client-ready slides."
        ],
        "comment_style": "professional"
    }
}

GENERIC_TITLE_TEMPLATES = [
    "Anyone tried {company} for {kw}?",
    "{company} vs alternatives for {kw}",
    "Best tools for {kw}?",
    "How do people handle {kw}?"
]
GENERIC_BODY_TEMPLATES = [
    "I'm evaluating tools for {kw}. Any experiences with {company}?",
    "Trying to handle {kw} more efficiently. Would {company} help?",
    "Working on projects that require {kw}. Is {company} a good fit?"
]

# ------------------------------
# Utilities
# ------------------------------
def choose_subreddit_template(subreddit: str) -> Dict:
    key = subreddit
    if key in SUBREDDIT_TEMPLATES:
        return SUBREDDIT_TEMPLATES[key]
    for k in SUBREDDIT_TEMPLATES.keys():
        if k.split("/")[1].lower() in subreddit.lower():
            return SUBREDDIT_TEMPLATES[k]
    return {
        "titles": GENERIC_TITLE_TEMPLATES,
        "bodies": GENERIC_BODY_TEMPLATES,
        "comment_style": "neutral"
    }

def persona_says(persona: Dict, text: str) -> str:
    voice = persona.get("voice", {"tone": "neutral", "brief": False, "quirk": ""})
    out = text
    if voice.get("brief") and random.random() < 0.4:
        out = out.split(".")[0]
    if voice.get("quirk") and random.random() < 0.5:
        out = out + " " + voice["quirk"]
    # add casual realism
    if random.random() < 0.3:
        out = out.replace("Any tips appreciated!", "Any tips appreciated? 🙂").replace("Thanks in advance.", "Thanks! 🙏")
        out = out.replace("Would love to hear your thoughts.", "Would love your thoughts!").replace("\n\n", " ")
    if random.random() < 0.2:
        out += f" (in my experience)"
    return out

def safe_sample(items: List, k: int):
    if not items:
        return []
    k = min(k, len(items))
    return random.sample(items, k)

# ------------------------------
# Post & Comment Generators (Improved)
# ------------------------------
def build_title(persona: Dict, keyword: Dict, company_name: str, subreddit: str) -> str:
    template_set = choose_subreddit_template(subreddit)
    t = random.choice(template_set["titles"]) if template_set.get("titles") else random.choice(GENERIC_TITLE_TEMPLATES)
    if "{kw}" in t or "{company}" in t:
        return t.format(company=company_name, kw=keyword.get("text"))
    if random.random() < 0.4:
        return f"{t} — {keyword.get('text')}"
    return t

def build_body(persona: Dict, keywords: List[Dict], company: Dict, subreddit: str) -> str:
    template_set = choose_subreddit_template(subreddit)
    body = random.choice(template_set.get("bodies", GENERIC_BODY_TEMPLATES))
    kw = keywords[0].get("text") if keywords else "this task"
    company_name = company.get("name") if isinstance(company, dict) else str(company)
    body = body.format(company=company_name, kw=kw)
    tails = [
        "\n\nAny tips appreciated!",
        "\n\nThanks in advance.",
        "\n\nWould love to hear your thoughts.",
        ""
    ]
    tail = random.choice(tails)
    if random.random() < 0.4:
        tail += f"\n\n— {persona.get('username')}"
    body = body + tail
    return persona_says(persona, body)

def generate_posts(num_posts: int = None, week_start: datetime = None) -> List[Dict]:
    company = get_company()
    personas = get_personas()
    subreddits = get_subreddits()
    keywords = get_keywords()

    if num_posts is None:
        num_posts = company.get("num_posts_per_week", 3)
    if week_start is None:
        week_start = datetime.now()

    posts: List[Dict] = []
    used_pairs = set()
    i = 1
    tries = 0
    persona_index = 0

    while len(posts) < num_posts and tries < num_posts * 80:
        tries += 1
        persona = personas[persona_index % len(personas)]
        persona_index += 1

        subreddit = random.choice(subreddits)
        post_keywords = safe_sample(keywords, k=min(2, len(keywords)))
        if not post_keywords:
            post_keywords = [{"id": "K1", "text": "general topic"}]
        keyword_ids = [kw.get("id") for kw in post_keywords]

        pair = (subreddit.lower(), tuple(sorted(keyword_ids)))
        if pair in used_pairs:
            continue
        used_pairs.add(pair)

        title = build_title(persona, post_keywords[0], company.get("name", "Company"), subreddit)
        body = build_body(persona, post_keywords, company, subreddit)

        delta_days = random.randint(0, 6)
        delta_hours = random.randint(9, 18) if random.random() < 0.8 else random.randint(0, 23)
        ts = week_start + timedelta(days=delta_days, hours=delta_hours)

        posts.append({
            "post_id": f"P{i}",
            "subreddit": subreddit,
            "title": title,
            "body": body,
            "author_username": persona.get("username", f"user{i}"),
            "timestamp": ts.strftime("%Y-%m-%d %H:%M"),
            "keyword_ids": ", ".join(keyword_ids)
        })
        i += 1

    return posts

def generate_comments(posts: List[Dict], min_comments=2, max_comments=5) -> List[Dict]:
    personas = get_personas()
    company = get_company()
    comments = []
    counter = 1
    used_texts = set()

    for post in posts:
        raw_kwids = [k.strip() for k in str(post.get("keyword_ids", "")).split(",") if k.strip()]
        global_keywords = {k["id"]: k["text"] for k in get_keywords()}
        post_kw_texts = [global_keywords.get(kid, kid) for kid in raw_kwids] if raw_kwids else ["this"]
        try:
            post_time = datetime.strptime(post.get("timestamp", ""), "%Y-%m-%d %H:%M")
        except Exception:
            post_time = datetime.now()
        num_comments = random.randint(min_comments, max_comments)
        thread_comments = []

        for n in range(num_comments):
            persona = random.choice(personas)
            if thread_comments and random.random() < 0.55:
                parent = random.choice(thread_comments)
                parent_id = parent["comment_id"]
            else:
                parent_id = None

            kw_ref = random.choice(post_kw_texts)
            voice = persona.get("voice", {"tone": "neutral", "brief": False, "quirk": ""})
            comment_variants = [
                f"I've used {company['name']} for {kw_ref} and it saved me time.",
                f"For {kw_ref} I usually export and tweak — {company['name']} gives me a good starting point.",
                f"Not perfect, but {company['name']} helps with {kw_ref}. You'll need to adjust layouts.",
                f"+1 — {company['name']} worked well for {kw_ref} in my experience.",
                f"I tried exporting to Google Slides and then cleaned up spacing — quicker than starting from scratch.",
                f"Saved me a lot of time for {kw_ref} 😊",
                f"I hate fixing fonts but {company['name']} made the structure for {kw_ref}.",
                f"Depends on use-case — for simple {kw_ref} it's great, complex layouts need work."
            ]

            # add mild disagreement or variation
            if random.random() < 0.25:
                comment_variants.append(f"Hmm, I found {company['name']} a bit tricky for {kw_ref} though others might like it.")

            text = random.choice(comment_variants)
            if voice.get("brief") and random.random() < 0.5:
                text = text.split(".")[0]
            if voice.get("quirk") and random.random() < 0.5:
                text = text + " " + voice["quirk"]
            if text in used_texts:
                if random.random() < 0.6:
                    text += ". " + random.choice(["Worked for me.", "YMMV.", "Your mileage may vary."])
                else:
                    text += "."

            ts = post_time + timedelta(minutes=random.randint(5, 180) + len(thread_comments) * 4)
            comment = {
                "comment_id": f"C{counter}",
                "post_id": post.get("post_id"),
                "parent_comment_id": parent_id,
                "comment_text": text,
                "username": persona.get("username", f"user{counter}"),
                "timestamp": ts.strftime("%Y-%m-%d %H:%M")
            }
            comments.append(comment)
            thread_comments.append(comment)
            used_texts.add(text)
            counter += 1

    return comments

# ------------------------------
# Scoring / Quality checks
# ------------------------------
def score_calendar(posts: List[Dict], comments: List[Dict]) -> Tuple[float, Dict]:
    base = 100.0
    details = {"duplicate_pairs": 0, "orphan_comments": 0, "persona_mismatch": 0, "repeated_comments": 0}
    seen = set()

    personas = get_personas()
    persona_usernames = {p.get("username") for p in personas if p.get("username")}

    for p in posts:
        pair = (p.get("subreddit", "").lower(), p.get("keyword_ids", ""))
        if pair in seen:
            base -= 12
            details["duplicate_pairs"] += 1
        seen.add(pair)

    valid_comment_ids = {c.get("comment_id") for c in comments}
    for c in comments:
        if c.get("parent_comment_id") and c.get("parent_comment_id") not in valid_comment_ids:
            details["orphan_comments"] += 1
            base -= 6
        if c.get("username") not in persona_usernames:
            details["persona_mismatch"] += 1
            base -= 4

    texts = [c.get("comment_text") for c in comments]
    duplicates = len(texts) - len(set(texts))
    if duplicates > 0:
        details["repeated_comments"] = duplicates
        base -= min(20, duplicates * 2)

    final = max(0, min(10, round(base / 10, 1)))
    return final, details

# ------------------------------
# Export helper
# ------------------------------
def export_csv(posts: List[Dict], comments: List[Dict], out_dir: Path = Path(".")):
    try:
        import pandas as pd
    except Exception:
        raise RuntimeError("pandas required for export_csv - please install pandas")
    out_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(posts).to_csv(out_dir / "weekly_posts.csv", index=False)
    pd.DataFrame(comments).to_csv(out_dir / "weekly_comments.csv", index=False)

# ------------------------------
# Quick demo
# ------------------------------
if __name__ == "__main__":
    company = get_company()
    posts = generate_posts(num_posts=5)
    comments = generate_comments(posts)
    print("Posts:")
    for p in posts:
        print(p)
    print("\nComments:")
    for c in comments:
        print(c)
    score, details = score_calendar(posts, comments)
    print("\nScore:", score, details)
