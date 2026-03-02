"""
Compliance Transaction Review - Context Poisoning Demo
"""

import streamlit as st
from agentic_rag import run_compliance_check

st.set_page_config(
    page_title="Compliance Transaction Review",
    page_icon="🏦",
    layout="wide"
)

st.markdown("<style>.pending { color: #9ca3af; }</style>", unsafe_allow_html=True)

st.title("🏦 Compliance Transaction Review")
st.caption("Review and approve financial transactions")

TRANSACTIONS = [
    {"id": "TXN-001", "from_account": "US1101000000", "to_account": "DE1234000000", "amount": 75000,  "date": "2024-01-15"},
    {"id": "TXN-002", "from_account": "CY2109000000", "to_account": "GB9876000000", "amount": 120000, "date": "2024-01-16"},
    {"id": "TXN-003", "from_account": "RU9901000000", "to_account": "IR8201700000", "amount": 500000, "date": "2024-01-17"},
    {"id": "TXN-004", "from_account": "RU8801000000", "to_account": "IR4401000000", "amount": 250000, "date": "2024-01-18"},
]

if "results" not in st.session_state:
    st.session_state.results = {}

# --- Header ---
st.subheader("📋 Pending Transactions")
cols = st.columns([0.5, 1, 2, 2, 1.5, 1.5, 2])
for col, label in zip(cols, ["", "ID", "From", "To", "Amount", "Date", "Status"]):
    col.markdown(f"**{label}**")
st.divider()

# --- Rows ---
selected_ids = []
for tx in TRANSACTIONS:
    col_check, col_id, col_from, col_to, col_amount, col_date, col_status = st.columns([0.5, 1, 2, 2, 1.5, 1.5, 2])

    with col_check:
        if st.checkbox("Select", key=f"check_{tx['id']}", value=True, label_visibility="hidden"):
            selected_ids.append(tx["id"])
    with col_id:
        st.write(tx["id"])
    with col_from:
        st.write(tx["from_account"])
    with col_to:
        st.write(tx["to_account"])
    with col_amount:
        st.write(f"${tx['amount']:,}")
    with col_date:
        st.write(tx["date"])
    with col_status:
        result = st.session_state.results.get(tx["id"])
        if result is None:
            st.markdown('<span class="pending">⏳ PENDING</span>', unsafe_allow_html=True)
        elif result["decision"] == "APPROVED":
            st.success('✅ APPROVED')
        else:
            st.error('🚫 BLOCKED')

st.divider()

# --- Run button ---
if st.button("▶️ Run Compliance Check", type="primary", use_container_width=True):
    if not selected_ids:
        st.warning("No transactions selected.")
    else:
        progress = st.progress(0)
        for i, tx in enumerate([t for t in TRANSACTIONS if t["id"] in selected_ids]):
            with st.spinner(f"Checking {tx['id']}..."):
                result = run_compliance_check(tx, poisoned=True)
                st.session_state.results[tx["id"]] = result
            progress.progress((i + 1) / len(selected_ids))
        st.rerun()

# --- Expanded details ---
if st.session_state.results:
    st.divider()
    st.subheader("🔍 Transaction Details")

    for tx in TRANSACTIONS:
        result = st.session_state.results.get(tx["id"])
        if result is None:
            continue

        icon = "✓" if result["decision"] == "APPROVED" else "✗"
        with st.expander(f"{icon} {tx['id']} — {tx['from_account']} → {tx['to_account']} — ${tx['amount']:,}"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**Original Transaction**")
                st.json(tx)

            with col2:
                st.markdown("**Enriched Transaction**")
                enriched = result.get("enriched_transaction")
                if enriched:
                    st.json(enriched)
                else:
                    st.caption("Not available")

            with col3:
                st.markdown("**Decision**")
                if result["decision"] == "APPROVED":
                    st.success('✅ APPROVED')
                else:
                    st.error('🚫 BLOCKED')

                if result.get("policy_sources"):
                    st.markdown("**Policies Applied**")
                    for src in result["policy_sources"]:
                        st.caption(f"📄 {src}")

                st.markdown("**Reasoning**")
                st.write(result["reasoning"])

st.divider()
if st.button("🗑️ Clear Results"):
    st.session_state.results = {}
    st.rerun()