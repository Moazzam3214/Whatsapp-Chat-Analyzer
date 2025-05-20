# 📊 WhatsApp Chat Analyzer

A Streamlit-based web application that lets you upload and analyze your WhatsApp chat exports. It provides detailed visual insights into chat activity, user engagement, word usage, emoji trends, and more.

---

## 🚀 Features

- 📂 Upload `.txt` format WhatsApp chat export
- 📅 Filter messages by custom date range
- 🧑‍🤝‍🧑 View stats for individual users or entire group
- 📈 Message timelines (daily, weekly, monthly)
- 📊 Busiest days and months
- 🔠 Word cloud of most used terms
- 😂 Emoji usage and distribution
- 🕒 Hourly activity heatmap

---

## 🗂️ File Structure

```bash
.
├── app.py               # Streamlit UI & logic
├── preprocessor.py      # Chat parsing & formatting
├── helper.py            # Stats, plots, emoji & word cloud generation
├── stop_hinglish.txt    # Stopwords used for word cloud
├── requirements.txt     # Python dependencies
├── stop_hinglish.txt    # Hindi-English stop words
````

---

## ▶️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

---

## 💡 How It Works

1. Upload your exported WhatsApp chat `.txt` file (without media).
2. The app processes the chat data to extract timestamps, users, and messages.
3. It displays visual summaries, charts, and activity breakdowns using:

   * Bar plots
   * Line charts
   * Pie charts
   * Heatmaps
   * Word clouds

---

## 📦 Requirements

* Python 3.7 or higher
* streamlit
* pandas
* matplotlib
* seaborn
* urlextract
* wordcloud
* emoji

Install all with:

```bash
pip install -r requirements.txt
```

---


## 🧾 License

This project is licensed under the MIT License.

---

## 🙋‍♂️ Author

Developed by Moazzam(https://github.com/moazzam3214)

