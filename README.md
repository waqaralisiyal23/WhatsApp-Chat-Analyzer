# WhatsApp Chat Analyzer

A Python-based web application built with [Streamlit](https://streamlit.io/) to analyze your WhatsApp chat data. It provides insights into your conversation patterns, including message statistics, user activity, word clouds, and emoji usage.

**Live Demo:** [https://whatsapp-chat-analyzer.waqaralisiyal.com](https://whatsapp-chat-analyzer.waqaralisiyal.com)

## 📊 Features

- **Top Statistics:** View total messages, words, media shared, and links.
- **Monthly & Daily Timelines:** Track message frequency over time.
- **Activity Maps:** Identify the busiest days and months.
- **Weekly Heatmap:** Visualize activity patterns across the week.
- **Most Busy Users:** See who contributes the most to the chat (for group chats).
- **Word Cloud:** Visual representation of the most frequently used words.
- **Emoji Analysis:** breakdown of emoji usage.

## 🛠️ Installation & Usage

Follow these steps to run the project locally on your machine.

### Prerequisites
- Python 3.7+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/waqaralisiyal23/WhatsApp-Chat-Analyzer.git
cd WhatsApp-Chat-Analyzer
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## 📱 How to Export WhatsApp Chat
1. Open a chat in WhatsApp on your phone.
2. Tap on the three dots (Android) or Contact Name (iOS).
3. Select **More > Export Chat**.
4. Choose **Without Media**.
5. Upload the generated `.txt` file to the app.

---
*Developed by [Waqar Ali Siyal](https://github.com/waqaralisiyal23)*
