import os
import io
import zipfile
import re
import streamlit as st
from dotenv import load_dotenv
from fpdf import FPDF

from langchain_community.document_loaders import YoutubeLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YT → Article & PDF",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 :red[_YouTube_] → Article & PDF Generator", text_alignment="center")
st.caption("Paste a YouTube URL → Get a professional article + PDF + downloadable webpage", text_alignment="center")

# ── Inputs ───────────────────────────────────────────────────────────────────
api_key     = st.text_input("🔑 Google API Key", type="password", placeholder="type your API key here")
youtube_url = st.text_input("🔗 YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
run_btn     = st.button("⚡ Generate Article", use_container_width=True)

# ── Chains ───────────────────────────────────────────────────────────────────
def get_chains(key):
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", api_key=key)

    article_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "You are a Professional Article Writer specializing in Medium, LinkedIn, and tech blogs."
        ),
        HumanMessagePromptTemplate.from_template("""
Transform the YouTube transcript below into an engaging professional article.

CRITICAL INSTRUCTIONS:
- IGNORE: "welcome", "In this video", channel names, "subscribe", "like", sponsors, affiliate links
- FOCUS ONLY on technical content, code, tutorials, actionable insights

ARTICLE STRUCTURE:
- First-person professional tone
- Bold subheadings and numbered lists
- Code snippets for technical content
- Actionable Steps (copy-paste ready)
- Short summary at the end

TRANSCRIPT:
{transcript}
""")
    ])

    webpage_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("""You are a Senior Frontend Developer.
Generate COMPLETE production-ready frontend code.

MANDATORY OUTPUT FORMAT:
--html--
[html code here]
--html--

--css--
[css code here]
--css--

--js--
[javascript code here]
--js--
"""),
        HumanMessagePromptTemplate.from_template("""
Create a production-ready Medium-style article webpage.

Requirements:
- Mobile-first responsive
- Google Fonts (NOT system fonts)
- Dark/light theme toggle
- Smooth animations
- SEO meta tags
- Accessible (ARIA labels)

ARTICLE CONTENT:
{article_content}
""")
    ])

    summarizer = (
        RunnableLambda(lambda url: "\n".join([doc.page_content for doc in YoutubeLoader.from_youtube_url(url, add_video_info=False).load()]))
        | RunnableLambda(lambda t: {"transcript": t})
        | article_prompt
        | llm
        | StrOutputParser()
    )

    webpage = (
        RunnableLambda(lambda a: {"article_content": a})
        | webpage_prompt
        | llm
        | StrOutputParser()
    )

    return summarizer, webpage

# ── Parse HTML/CSS/JS ────────────────────────────────────────────────────────
def parse_output(raw):
    def extract(tag):
        try:
            return raw.split(f"--{tag}--")[1].strip()
        except IndexError:
            return ""
    return extract("html"), extract("css"), extract("js")

# ── Generate PDF ─────────────────────────────────────────────────────────────
def generate_pdf(article_text: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(left=20, top=20, right=20)
    pdf.set_auto_page_break(auto=True, margin=20)

    def safe_text(text):
        return text.encode("latin-1", errors="replace").decode("latin-1")

    def wrap_long_words(text, max_len=60):
        words, result = text.split(), []
        for word in words:
            while len(word) > max_len:
                result.append(word[:max_len])
                word = word[max_len:]
            result.append(word)
        return " ".join(result)

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "YouTube Article Summary", align="C")
    pdf.ln(5)

    clean = article_text
    clean = re.sub(r"```.*?```", "", clean, flags=re.DOTALL)
    clean = clean.replace("**", "").replace("##", "").replace("#", "").replace("*", "").replace("`","")

    pdf.set_font("Helvetica", size=10)
    for line in clean.split("\n"):
        line = line.strip()
        if not line or re.search(r"<[^>]+>", line):
            pdf.ln(3)
            continue
        line = wrap_long_words(line)
        line = safe_text(line)
        try:
            if line.endswith(":") or line.isupper():
                pdf.set_font("Helvetica", "B", 11)
                pdf.multi_cell(0, 7, line)
                pdf.set_font("Helvetica", size=10)
            else:
                pdf.multi_cell(0, 6, line)
        except Exception:
            continue
    return bytes(pdf.output(dest="S"))

# ── Run App ────────────────────────────────────────────────────────────────
if run_btn:
    if not api_key:
        st.error("❌ Please enter your Google API Key.")
    elif not youtube_url:
        st.error("❌ Please enter a YouTube URL.")
    else:
        try:
            summarizer, webpage_chain = get_chains(api_key)

            with st.spinner("📝 Extracting transcript & generating article..."):
                article = summarizer.invoke(youtube_url)

            st.success("✅ Article generated!")

            # Article Preview
            with st.expander("📄 View Article", expanded=True):
                st.markdown(article)

            # PDF Download
            pdf_bytes = generate_pdf(article)
            st.download_button(
                label="📥 Download Article as PDF",
                data=pdf_bytes,
                file_name="article.pdf",
                mime="application/pdf",
                use_container_width=True
            )

            # Webpage
            with st.spinner("🎨 Building webpage..."):
                raw_webpage = webpage_chain.invoke(article)

            html, css, js = parse_output(raw_webpage)

            st.subheader("🌐 Webpage Preview")
            full_html = f"""<!DOCTYPE html><html><head><style>{css}</style></head><body>{html}<script>{js}</script></body></html>"""
            st.components.v1.html(full_html, height=600, scrolling=True)

            # ZIP Download
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("index.html", html)
                zf.writestr("style.css", css)
                zf.writestr("script.js", js)
            zip_buffer.seek(0)
            st.download_button(
                label="⬇️ Download Website (ZIP)",
                data=zip_buffer,
                file_name="website.zip",
                mime="application/zip",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")
