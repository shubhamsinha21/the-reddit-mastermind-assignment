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
        c["num_posts_per_week"] = int(n)
    except Exception:
        c["num_posts_per_week"] = 3
    return c

def normalize_personas(raw: Any) -> List[Dict]:
    if not raw:
        return []
    out = []
    if isinstance(raw, dict):
        raw = [raw]
    for item in raw:
        if isinstance(item, str):
            out.append({"username": item, "background": ""})
            continue
        if not isinstance(item, dict):
            continue
        username = item.get("username") or item.get("Username") or item.get("user") or item.get("handle")
        if not username:
            for k, v in item.items():
                if isinstance(v, str) and "@" not in str(v) and len(str(v)) <= 30:
                    username = v
                    break
        background = item.get("background") or item.get("Background") or item.get("Info") or item.get("info") or item.get("bio") or item.get("description") or ""
        out.append({
            "username": str(username).strip() if username else f"user_{len(out)+1}",
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
    keywords = []
    if not raw:
        return []
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
# Public getters
# ------------------------------
def get_company() -> Dict:
    company = normalize_company(load_json(DATA_DIR / "company.json"))
    if not company.get("name"):
        company["name"] = "Company"
    return company

def get_personas() -> List[Dict]:
    personas = normalize_personas(load_json(DATA_DIR / "personas.json"))
    if not personas:
        personas = [{"username": "anon_user", "background": ""}]
    return personas

def get_subreddits() -> List[str]:
    raw = normalize_subreddits(load_json(DATA_DIR / "subreddits.json"))
    if raw:
        return raw
    company_raw = load_json(DATA_DIR / "company.json")
    if company_raw:
        return normalize_subreddits(company_raw.get("Subreddits") or company_raw.get("subreddits"))
    return ["r/general"]

def get_keywords() -> List[Dict]:
    keywords = normalize_keywords(load_json(DATA_DIR / "keywords.json"))
    if not keywords:
        # fallback default keyword
        keywords = [{"id": "K1", "text": "general topic"}]
    return keywords

# ------------------------------
# Post & Comment Generators
# ------------------------------
def build_title(persona: Dict, keyword: Dict, company_name: str) -> str:
    templates = [
        "Has anyone tried {company} for {kw}?",
        "Any tips for using {company} in {kw}?",
        "{company} vs alternatives for {kw}",
        "Best practices for {kw} using {company}",
        "Looking for experiences with {company} on {kw}"
    ]
    return random.choice(templates).format(company=company_name, kw=keyword.get("text"))

def build_body(persona: Dict, keywords: List[Dict], company: Dict) -> str:
    uname = persona.get("username", "")
    background = persona.get("background", "").lower()
    company_name = company.get("name") if isinstance(company, dict) else str(company)
    kw_texts = ", ".join([kw.get('text') for kw in keywords]) if keywords else "general topic"

    templates = []
    if "student" in background:
        templates.extend([
            f"I'm a student trying to handle {kw_texts}. Has anyone used {company_name}?",
            f"Working on a project involving {kw_texts}. Is {company_name} reliable?",
            f"Not sure how to handle {kw_texts}, anyone tried {company_name}?"
        ])
    elif "consult" in background or "manager" in background:
        templates.extend([
            f"I'm managing client projects involving {kw_texts}. Curious if {company_name} scales well.",
            f"Has anyone applied {company_name} for client work on {kw_texts}?",
            f"Looking for best practices for {kw_texts} with {company_name}."
        ])
    else:
        templates.extend([
            f"I'm trying to improve {kw_texts} workflow. Thoughts on {company_name}?",
            f"Heard about {company_name}, wondering if it works for {kw_texts}.",
            f"Anyone using {company_name} to handle {kw_texts}?",
            f"Trying to automate {kw_texts}, {company_name} ok for that?"
        ])

    body = random.choice(templates)

    endings = ["\n\nAny tips appreciated!", "\n\nThanks in advance.", "\n\nWould love to hear your thoughts.", ""]
    body += random.choice(endings)

    if random.random() < 0.5:
        body += f"\n\n— {uname}"

    return body

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

    while len(posts) < num_posts and tries < num_posts * 50:
        tries += 1
        persona = personas[persona_index % len(personas)]
        persona_index += 1

        subreddit = random.choice(subreddits)
        # safe sample: at least one keyword
        if not keywords:
            post_keywords = [{"id": "K1", "text": "general topic"}]
        else:
            post_keywords = random.sample(keywords, min(2, len(keywords)))

        keyword_ids = [kw.get('id') for kw in post_keywords]

        pair = (subreddit, tuple(sorted(keyword_ids)))
        if pair in used_pairs:
            continue
        used_pairs.add(pair)

        title = build_title(persona, post_keywords[0], company.get("name", "Company"))
        body = build_body(persona, post_keywords, company)

        delta_days = random.randint(0, 6)
        delta_hours = random.randint(8, 22)
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

def generate_comments(posts: List[Dict], min_comments=2, max_comments=4) -> List[Dict]:
    personas = get_personas()
    company = get_company()
    comments = []
    counter = 1

    comment_templates = [
        "I've tried {company} for this and it saved a lot of time.",
        "Curious — does anyone double-check results before sharing?",
        "I tried {company} + exported to Google Slides and adjusted manually.",
        "+1 — good starting point, then polish in Canva.",
        "Not perfect but worth a try for drafts.",
        "Honestly, {company} does okay but requires tweaks.",
        "I love the default templates from {company}, saves my sanity!",
        "Worked well for me, though I adjusted some settings.",
        "Anyone else tried {company} for similar tasks?",
        "I think {company} is decent depending on use case.",
        "Slide outputs can be quirky, but manageable.",
        "Just sharing my two cents, {company} helped me here.",
        "Thanks for sharing! I used {company} and it worked well. 😊"
    ]

    used_texts = set()
    for post in posts:
        try:
            post_time = datetime.strptime(post.get("timestamp", ""), "%Y-%m-%d %H:%M")
        except:
            post_time = datetime.now()

        num_comments = random.randint(min_comments, max_comments)
        thread_comments = []

        for _ in range(num_comments):
            persona = random.choice(personas) if personas else {"username": "anon", "background": ""}
            parent_id = random.choice(thread_comments)["comment_id"] if thread_comments and random.random() < 0.6 else None
            text = random.choice(comment_templates).format(company=company.get("name", "Company"))

            if text in used_texts and random.random() < 0.7:
                text += "."  
            if thread_comments and random.random() < 0.4:
                text += " 😊"

            ts = post_time + timedelta(minutes=random.randint(10, 360) + len(thread_comments)*5)
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

def score_calendar(posts: List[Dict], comments: List[Dict]) -> Tuple[float, Dict]:
    score = 100.0
    details = {"duplicate_pairs": 0, "orphan_comments": 0, "persona_mismatch": 0}
    seen = set()
    personas = get_personas()
    persona_usernames = {p.get("username") for p in personas if isinstance(p, dict) and p.get("username")}

    for p in posts:
        pair = (p.get("subreddit"), p.get("keyword_ids"))
        if pair in seen:
            score -= 10
            details["duplicate_pairs"] += 1
        seen.add(pair)

    valid_comment_ids = {c.get("comment_id") for c in comments}
    for c in comments:
        if c.get("parent_comment_id") and c.get("parent_comment_id") not in valid_comment_ids:
            score -= 5
            details["orphan_comments"] += 1
        if c.get("username") not in persona_usernames:
            score -= 5
            details["persona_mismatch"] += 1

    final = max(0, min(10, round(score / 10, 1)))
    return final, details

def export_csv(posts: List[Dict], comments: List[Dict], out_dir: Path = Path(".")):
    import pandas as pd
    out_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(posts).to_csv(out_dir / "weekly_posts.csv", index=False)
    pd.DataFrame(comments).to_csv(out_dir / "weekly_comments.csv", index=False)
