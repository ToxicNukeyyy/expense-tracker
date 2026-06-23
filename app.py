import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date

# ── Config ────────────────────────────────────────────────────────────────────
CSV_FILE = "expenses.csv"
CATEGORIES = ["Food", "Transport", "Health", "Entertainment", "Education", "Housing", "Other"]

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# ── Load / save ───────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, parse_dates=["date"])
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
        return df
    return pd.DataFrame(columns=["date", "category", "amount", "description"])

def save_data(df):
    df.to_csv(CSV_FILE, index=False, date_format="%Y-%m-%d")

# ── Main ──────────────────────────────────────────────────────────────────────
st.title("💰 Personal Expense Tracker")

df = load_data()

# ── Sidebar: add expense ──────────────────────────────────────────────────────
with st.sidebar:
    st.header("Add Expense")
    with st.form("add_form", clear_on_submit=True):
        exp_date     = st.date_input("Date", value=date.today())
        exp_category = st.selectbox("Category", CATEGORIES)
        exp_amount   = st.number_input("Amount (R$)", min_value=0.01, step=0.01, format="%.2f")
        exp_desc     = st.text_input("Description")
        submitted    = st.form_submit_button("Add", use_container_width=True, type="primary")

    if submitted:
        if exp_desc.strip() == "":
            st.error("Please add a description.")
        else:
            new_row = pd.DataFrame([{
                "date": pd.Timestamp(exp_date),
                "category": exp_category,
                "amount": exp_amount,
                "description": exp_desc.strip()
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success(f"Added R$ {exp_amount:.2f} — {exp_desc}")
            st.rerun()

# ── Empty state ───────────────────────────────────────────────────────────────
if df.empty:
    st.info("No expenses yet. Add your first one in the sidebar.")
    st.stop()

# ── Summary cards ─────────────────────────────────────────────────────────────
total        = df["amount"].sum()
by_category  = df.groupby("category")["amount"].sum().sort_values(ascending=False)
top_category = by_category.index[0]
biggest      = df.loc[df["amount"].idxmax()]

c1, c2, c3 = st.columns(3)
c1.metric("Total spent",     f"R$ {total:,.2f}")
c2.metric("Top category",    f"{top_category}  (R$ {by_category[top_category]:,.2f})")
c3.metric("Biggest expense", f"R$ {biggest['amount']:.2f} — {biggest['description']}")

st.divider()

# ── Chart + table ─────────────────────────────────────────────────────────────
col_chart, col_table = st.columns([1, 1], gap="large")

with col_chart:
    st.subheader("Spending by category")
    colors = ["#4F46E5","#0EA5E9","#10B981","#F59E0B","#EF4444","#8B5CF6","#EC4899"]
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(by_category.index, by_category.values,
           color=colors[:len(by_category)], edgecolor="none", width=0.6)
    for i, (cat, val) in enumerate(by_category.items()):
        ax.text(i, val + total * 0.01, f"R${val:.0f}",
                ha="center", va="bottom", fontsize=8, color="#374151")
    ax.set_ylabel("R$", fontsize=9)
    ax.spines[["top","right"]].set_visible(False)
    ax.spines[["left","bottom"]].set_color("#E5E7EB")
    ax.set_facecolor("#F9FAFB")
    fig.patch.set_facecolor("white")
    ax.tick_params(axis="x", labelsize=8)
    ax.tick_params(axis="y", labelsize=8)
    plt.tight_layout()
    st.pyplot(fig)

with col_table:
    st.subheader("All expenses")
    display_df = df.sort_values("date", ascending=False).copy()
    display_df["date"]   = display_df["date"].dt.strftime("%d/%m/%Y")
    display_df["amount"] = display_df["amount"].apply(lambda x: f"R$ {x:.2f}")
    display_df.columns   = ["Date", "Category", "Amount", "Description"]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ── Delete ────────────────────────────────────────────────────────────────────
with st.expander("🗑️ Delete an entry"):
    if not df.empty:
        df_reset = df.reset_index(drop=True)
        options  = {
            f"{row['date'].strftime('%d/%m/%Y')} — {row['description']} (R$ {row['amount']:.2f})": idx
            for idx, row in df_reset.iterrows()
        }
        selected = st.selectbox("Select entry to delete", list(options.keys()))
        if st.button("Delete", type="primary"):
            df = df_reset.drop(index=options[selected]).reset_index(drop=True)
            save_data(df)
            st.success("Entry deleted.")
            st.rerun()
