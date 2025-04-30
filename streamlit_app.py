import streamlit as st
from supabase import create_client, Client
import datetime

# 接続設定（secrets.tomlから取得）
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# ユーザー入力欄
st.title("📘 交換日記アプリ")

user_list = ["ikumi", "haruka", "hinami"]
name = st.selectbox("ユーザーを選んでください", user_list)

today = datetime.date.today()
event = st.text_area("今日あったこと")
good = st.text_area("Good News")
bad = st.text_area("Bad News")
worry = st.text_area("お悩みコーナー")
secret = st.text_area("ここだけの話")
recommend = st.text_area("最近のおすすめ")

if st.button("日記を提出"):
    data = {
        "user_name": name,
        "diary_date": today.isoformat(),
        "today_event": event,
        "good_news": good,
        "bad_news": bad,
        "worry": worry,
        "secret": secret,
        "recommend": recommend,
    }
    response = supabase.table("diary").insert(data).execute()
    st.success("提出しました！")

# 投稿の一覧表示

        
st.subheader("📖 みんなの日記")

# 1. カード用のCSSを追加（最初に1回だけ）
st.markdown("""
    <style>
    .diary-card {
        background-color: #f8f9fa;
        padding: 1.2em;
        margin-bottom: 1em;
        border-radius: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .diary-card h4 {
        margin-top: 0;
        margin-bottom: 0.5em;
        color: #333;
    }
    .diary-card p {
        margin: 0.3em 0;
        font-size: 0.95em;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Supabaseから日記データを取得して、HTMLで整形して表示
res = supabase.table("diary").select("*").order("timestamp", desc=True).limit(10).execute()

for row in res.data:
    st.markdown(f"""
    <div class="diary-card">
        <h4>{row['diary_date']} - {row['user_name']}</h4>
        <p><strong>📝 今日あったこと:</strong> {row['today_event']}</p>
        <p><strong>✅ Good News:</strong> {row['good_news']}</p>
        <p><strong>❌ Bad News:</strong> {row['bad_news']}</p>
        <p><strong>💭 お悩み:</strong> {row['worry']}</p>
        <p><strong>🤐 ここだけの話:</strong> {row['secret']}</p>
        <p><strong>🌟 最近のおすすめ:</strong> {row['recommend']}</p>
    </div>
    """, unsafe_allow_html=True)

