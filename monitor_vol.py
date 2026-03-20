import streamlit as st
import feedparser

st.set_page_config(page_title="Monitoring Vol Vietnam", layout="wide")

KEYWORDS = [
    "vietjet",
    "vietnam airlines",
    "fuel shortage",
    "flight cuts",
    "jet fuel"
]

RSS_FEEDS = [
    "https://www.reuters.com/world/asia-pacific/rss",
    "https://www.reuters.com/business/aerospace-defense/rss"
]

def check_news():
    risk = 0
    alerts = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:10]:
            title = entry.title.lower()

            for keyword in KEYWORDS:
                if keyword in title:
                    alerts.append(entry.title)

                    if "cut" in title or "shortage" in title:
                        risk += 2
                    else:
                        risk += 1

    return risk, alerts


def calculate_status(risk):
    if risk >= 4:
        return "🔴 ROUGE"
    elif risk >= 2:
        return "🟠 ORANGE"
    else:
        return "🟢 VERT"


# ---------------- UI ----------------

st.title("✈️ Monitoring Vol Vietnam")

risk, alerts = check_news()
status = calculate_status(risk)

st.subheader(f"Statut actuel : {status}")

if status == "🔴 ROUGE":
    st.error("Risque élevé de perturbation")
elif status == "🟠 ORANGE":
    st.warning("Situation instable")
else:
    st.success("Situation normale")

st.markdown("---")

st.subheader("📰 Actualités détectées")

if alerts:
    for alert in alerts:
        st.write(f"- {alert}")
else:
    st.write("Aucune alerte détectée")

st.markdown("---")

st.caption("Mise à jour en temps réel (rafraîchir la page)")
