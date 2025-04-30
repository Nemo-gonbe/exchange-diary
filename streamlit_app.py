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
res = supabase.table("diary").select("*").order("timestamp", desc=True).limit(10).execute()

for row in res.data:
    with st.expander(f"{row['diary_date']} - {row['user_name']}"):
        st.write(f"📝 今日あったこと: {row['today_event']}")
        st.write(f"✅ Good News: {row['good_news']}")
        st.write(f"❌ Bad News: {row['bad_news']}")
        st.write(f"💭 お悩み: {row['worry']}")
        st.write(f"🤐 ここだけの話: {row['secret']}")
        st.write(f"🌟 最近のおすすめ: {row['recommend']}")
