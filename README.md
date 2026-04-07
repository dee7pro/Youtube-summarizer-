# 🎬 YouTube → Article & PDF Generator

A Generative AI that extracts insights from YouTube videos and transforms them into polished articles, PDFs, and web-ready content effortlessly.

### Streamlit : https://youtubesummariser1.streamlit.app/
---
## 🚀 Demo

<h3>App Screenshots</h3>
<div style="display:flex; gap:10px; flex-wrap:wrap;">
<img width="300" alt="Screenshot 1" src="https://github.com/dee7pro/Youtube-summarizer-/blob/efba6f9f99f023fe20682df14c362babf31a4570/assets/img_1.png" />
<img width="300" alt="Screenshot 2" src="https://github.com/dee7pro/Youtube-summarizer-/blob/efba6f9f99f023fe20682df14c362babf31a4570/assets/img_2.png" />
<img width="300" alt="Code Screenshot" src="https://github.com/dee7pro/Youtube-summarizer-/blob/efba6f9f99f023fe20682df14c362babf31a4570/assets/youtube_sum_code.png" />

</div>
---

## ✨ Features

- 📝 Extracts YouTube transcript automatically
- 🤖 Generates structured article using **gemini-3-flash-preview** (via Gemini aka Google)
- 📄 Downloads article as **PDF**
- 🌐 Generates a **full responsive webpage** (HTML/CSS/JS)
- ⬇️ Download website as **ZIP**
- 🌙 Dark/Light theme toggle on generated webpage

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | gemini-3-flash-preview |
| Framework | LangChain |
| UI | Streamlit |
| PDF | fpdf2 |
| Transcript | youtube-transcript-api |

---

## ⚙️ Setup & Run

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/YoutubeSummarizer.git
cd YoutubeSummarizer
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add API Key**

Create a `.env` file:
```
gemini_class = your_gemini_api_key_here
```

**5. Run**
```bash
streamlit run Youtube_sum.py
```

---

## 📁 Project Structure

```
YoutubeSummarizer/
├── Youtube_sum.py              # Main Streamlit app
├── requirements.txt    # Dependencies
├── .env.example        # API key template
└── README.md
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `gemini_class` | Gemini API key  |

---

## 📌 How It Works

```
YouTube URL
    ↓
Extract Transcript (YoutubeLoader)
    ↓
Generate Article (gemini-3-flash-preview via Gemini / Google)
    ↓
Generate Webpage (HTML/CSS/JS)
    ↓
PDF + ZIP Download
```

---

## 👨‍💻 Author

**Deepika A ** — Gen AI Engineer  

## License
MIT License © 2026 dee7pro

