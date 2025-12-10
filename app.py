# app.py (updated)
import streamlit as st
from reddit_algorithm import generate_posts, generate_comments, score_calendar, export_csv
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
import traceback
import json

# ------------------------------
# Data directory (stores inputs)
# ------------------------------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Reddit Mastermind Planner", layout="wide")
st.title("Reddit Mastermind — Content Calendar Generator")

st.markdown("""
This app generates a weekly content calendar (posts + comments) for Reddit using:
- Company info (includes 'Number of posts per week')
- Personas
- Subreddits
- Keywords

Simply upload CSV / Excel files. Uploaded data is saved to `./data/`.
""")

# ------------------------------
# File paths
# ------------------------------
company_path = DATA_DIR / "company.json"
personas_path = DATA_DIR / "personas.json"
subreddits_path = DATA_DIR / "subreddits.json"
keywords_path = DATA_DIR / "keywords.json"

# ------------------------------
# JSON file helpers
# ------------------------------
def save_json_file(path: Path, data):
    try:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return True
    except Exception as e:
        st.error(f"Error saving {path.name}: {e}")
        st.error(traceback.format_exc())
        return False

# ------------------------------
# CSV/XLSX Upload
# ------------------------------
st.subheader("Upload CSV / Excel files")

uploaded_company = st.file_uploader("Upload company file", type=["csv", "xlsx"], key="up_company_csv")
uploaded_personas = st.file_uploader("Upload personas file", type=["csv", "xlsx"], key="up_personas_csv")
uploaded_subs = st.file_uploader("Upload subreddits file", type=["csv", "xlsx"], key="up_subs_csv")
uploaded_keywords = st.file_uploader("Upload keywords file", type=["csv", "xlsx"], key="up_keywords_csv")

def read_file(file):
    try:
        file.seek(0)
        name = file.name.lower()
        if name.endswith(".csv"):
            return pd.read_csv(file, dtype=str)
        return pd.read_excel(file, dtype=str)
    except Exception as e:
        st.error(f"Failed to read {file.name}: {e}")
        st.error(traceback.format_exc())
        return None

def first_nonempty_column(df):
    for col in df.columns:
        col_series = df[col].dropna().astype(str).str.strip()
        if not col_series.empty:
            return col_series.tolist()
    return []

# --- Upload Company ---
if uploaded_company:
    df = read_file(uploaded_company)
    if df is not None and not df.empty:
        df.columns = [c.strip() for c in df.columns]
        company_dict = df.to_dict(orient='records')[0]
        if save_json_file(company_path, company_dict):
            st.success("Uploaded company info successfully.")

# --- Upload Personas ---
if uploaded_personas:
    df = read_file(uploaded_personas)
    if df is not None and not df.empty:
        df.columns = [c.strip() for c in df.columns]
        personas_list = df.to_dict(orient='records')
        normalized = []
        for row in personas_list:
            norm = {}
            for k, v in row.items():
                keyname = k.strip().lower()
                if keyname in ("username", "user", "handle"):
                    norm["username"] = v.strip() if isinstance(v, str) else str(v)
                elif keyname in ("info", "background", "bio", "description"):
                    norm["background"] = v.strip() if isinstance(v, str) else str(v)
            if "username" not in norm:
                for k, v in row.items():
                    if isinstance(v, str) and len(v) <= 30:
                        norm["username"] = v.strip()
                        break
            if "username" not in norm:
                norm["username"] = f"user_{len(normalized)+1}"
            if "background" not in norm:
                norm["background"] = ""
            normalized.append(norm)
        if save_json_file(personas_path, normalized):
            st.success("Uploaded personas successfully.")

# --- Upload Subreddits ---
if uploaded_subs:
    df = read_file(uploaded_subs)
    if df is not None and not df.empty:
        df.columns = [c.strip() for c in df.columns]
        subs_list = first_nonempty_column(df)
        if save_json_file(subreddits_path, subs_list):
            st.success("Uploaded subreddits successfully.")

# --- Upload Keywords ---
if uploaded_keywords:
    df = read_file(uploaded_keywords)
    if df is not None and not df.empty:
        df.columns = [c.strip() for c in df.columns]
        if "text" in df.columns:
            kw_list = df["text"].dropna().astype(str).str.strip().tolist()
        elif "keyword" in df.columns:
            kw_list = df["keyword"].dropna().astype(str).str.strip().tolist()
        else:
            kw_list = first_nonempty_column(df)
        keywords_list = [{"id": f"K{i+1}", "text": kw} for i, kw in enumerate(kw_list)]
        if save_json_file(keywords_path, keywords_list):
            st.success("Uploaded keywords successfully.")

# ------------------------------
# Display calendar & downloads
# ------------------------------
def show_calendar_and_downloads(posts, comments, label_prefix=""):
    st.subheader(f"Posts ({label_prefix}weekly calendar)" if label_prefix else "Posts (weekly calendar)")
    if posts:
        st.dataframe(posts)
    else:
        st.info("No posts generated.")

    st.subheader(f"Comments ({label_prefix}weekly)" if label_prefix else "Comments")
    if comments:
        st.dataframe(comments)
    else:
        st.info("No comments generated.")

    # Quality Preview Table (safe access)
    try:
        score, details = score_calendar(posts or [], comments or [])
    except Exception as e:
        st.error(f"Error scoring calendar: {e}")
        st.error(traceback.format_exc())
        score, details = 0, {}

    st.subheader("Quality Preview")
    st.markdown(f"**Overall quality score:** {score}/10")
    st.markdown(f"- Duplicate posts (same subreddit + keyword combo): {details.get('duplicate_pairs', 0)}")
    st.markdown(f"- Orphan comments (parent missing): {details.get('orphan_comments', 0)}")
    st.markdown(f"- Persona mismatches (comment author not in personas): {details.get('persona_mismatch', 0)}")

    # Prepare CSV downloads only if data exists
    posts_df = pd.DataFrame(posts) if posts else pd.DataFrame()
    comments_df = pd.DataFrame(comments) if comments else pd.DataFrame()

    if not posts_df.empty:
        csv_posts = posts_df.to_csv(index=False)
    else:
        csv_posts = ""

    if not comments_df.empty:
        csv_comments = comments_df.to_csv(index=False)
    else:
        csv_comments = ""

    col_a, col_b = st.columns(2)
    with col_a:
        if csv_posts:
            st.download_button(
                label="Download posts CSV",
                data=csv_posts,
                file_name=f"{label_prefix}weekly_posts_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No posts CSV to download.")
    with col_b:
        if csv_comments:
            st.download_button(
                label="Download comments CSV",
                data=csv_comments,
                file_name=f"{label_prefix}weekly_comments_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No comments CSV to download.")

# ------------------------------
# Generate actions
# ------------------------------
col1, col2 = st.columns(2)
with col1:
    if st.button("Generate Week"):
        week_start = datetime.now()
        try:
            posts = generate_posts(num_posts=None, week_start=week_start)
            comments = generate_comments(posts)
            show_calendar_and_downloads(posts, comments)
            # Save CSVs to project root
            try:
                export_csv(posts, comments, out_dir=Path('.'))
                st.success("Generated CSVs saved to project root (./weekly_posts.csv, ./weekly_comments.csv)")
            except Exception as e:
                st.error(f"Failed to export CSVs: {e}")
                st.error(traceback.format_exc())
        except Exception as e:
            st.error(f"Error generating week: {e}")
            st.error(traceback.format_exc())

with col2:
    if st.button("Generate Next Week (simulate)"):
        week_start = datetime.now() + timedelta(days=7)
        try:
            posts = generate_posts(num_posts=None, week_start=week_start)
            comments = generate_comments(posts)
            show_calendar_and_downloads(posts, comments, label_prefix="next_")
            try:
                export_csv(posts, comments, out_dir=Path('.'))
                st.success("Generated CSVs saved to project root (./weekly_posts.csv, ./weekly_comments.csv)")
            except Exception as e:
                st.error(f"Failed to export CSVs: {e}")
                st.error(traceback.format_exc())
        except Exception as e:
            st.error(f"Error generating next week: {e}")
            st.error(traceback.format_exc())

st.markdown("---")
st.info("Reminder: the planner **does not** post to Reddit — it only generates text you can use for posting.")
