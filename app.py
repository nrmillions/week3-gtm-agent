"""Run with: .venv/bin/python -m streamlit run app.py"""
import streamlit as st

from workflow import (EXAMPLE, OllamaClient, WorkflowError, approve_campaign,
                      campaign_markdown, new_state, run_workflow, validate_input)

st.set_page_config(page_title="AI GTM Content Agent", page_icon="🎬", layout="wide")
st.title("AI GTM Content Agent")
st.write("An agentic AI system that turns product ideas into a multi-format go-to-market campaign.")
st.caption("Local AI · Supplied-brief research · Human approval · No publishing or sending")

client = OllamaClient()
with st.sidebar:
    st.subheader("Local model")
    try:
        models = client.models()
        if not models:
            raise WorkflowError("No local models found. Run `ollama pull qwen2.5:3b` first.")
        selected = st.selectbox("Ollama model", models, index=models.index(client.model) if client.model in models else 0)
        client.model = selected
        st.success("Ollama connected")
        ready = True
    except WorkflowError as exc:
        st.warning(str(exc))
        ready = False
        if st.button("Try Again", key="reconnect"):
            st.rerun()
    st.caption("Uses separate context, strategy, content and review calls. Revision runs when needed, at most twice.")
    st.caption("First generation can take a few minutes while the local model loads.")
    st.write("Research source: your supplied brief. No external facts are fetched or verified.")

with st.form("product_form"):
    st.subheader("Your product, feature or event")
    left, right = st.columns(2)
    with left:
        name = st.text_input("Product / Feature Name", EXAMPLE["name"], max_chars=200)
        description = st.text_area("Description", EXAMPLE["description"], height=100, max_chars=4000)
        audience = st.text_input("Target Audience", EXAMPLE["audience"], max_chars=500)
    with right:
        launch = st.text_input("Launch Date", EXAMPLE["launch_date"], help="A month is fine. Leave blank if unknown.", max_chars=200)
        additional = st.text_area("Additional Context", EXAMPLE["additional_context"], height=150, max_chars=2500)
    generate = st.form_submit_button("Generate GTM Campaign", type="primary", disabled=not ready)

product = {"name": name.strip(), "description": description.strip(), "audience": audience.strip(),
           "launch_date": launch.strip(), "additional_context": additional.strip()}
progress = st.empty()


def render_progress(state):
    icons = {"running": "⏳", "complete": "✓", "retry": "↻", "failed": "❌", "waiting": "⏳", "warning": "⚠️", "skipped": "✓"}
    latest = {}
    for event in state["events"]:
        latest[event["stage"]] = event
    with progress.container():
        st.subheader("Agent workflow")
        for event in latest.values():
            st.write(f"{icons[event['status']]} **{event['stage']}** — {event['detail']}")


def start_campaign(brief):
    st.session_state.campaign = new_state(brief, client.model)
    # Never carry the acknowledgement of one campaign into the next.
    st.session_state.pop("acknowledge_issues", None)
    run_workflow(brief, client, st.session_state.campaign, render_progress)


if generate:
    try:
        validate_input(product)
    except WorkflowError as exc:
        st.error(str(exc))
    else:
        start_campaign(product)

state = st.session_state.get("campaign")
if state:
    if state["status"] == "failed":
        st.error(state["error"])
        st.info("Completed intermediate steps remain visible below. Try Again restarts from the saved original brief.")
        if st.button("Try Again", key="retry_campaign", disabled=not ready):
            start_campaign(state["original_input"])
            state = st.session_state.campaign
    render_progress(state)
    st.caption(f"Campaign: {state['original_input']['name']} · Model: {state['model']} · Revisions: {state['revision_count']}/2")
    with st.expander("Original brief and research/context", expanded=False):
        st.json(state["original_input"])
        if state["context"]:
            st.write(state["context"]["summary"])
            st.caption(state["context"]["source"])
            st.json({k: state["context"][k] for k in ("supplied_facts", "missing_fields", "unknowns", "claim_cautions")})
    if state["strategy"]:
        with st.expander("GTM strategy", expanded=True):
            for key, value in state["strategy"].items():
                st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
    if state["reviews"]:
        with st.expander("Review / critique and revision history", expanded=True):
            for index, review in enumerate(state["reviews"], 1):
                st.markdown(f"**Review {index} · {review['verdict']} · after {review['revision_count']} revision(s)**")
                st.write(review["summary"])
                for issue in review["issues"]:
                    st.warning(issue)
            if state["revision_count"] == 0:
                st.caption("Revision skipped because the reviewer passed the first draft.")
            with st.expander("Original draft (before any revisions)"):
                st.json(state["draft_content"])
    if state["current_content"]:
        st.subheader("Final content package" if state["status"] == "approved" else "Campaign preview — pending human review")
        content = state["current_content"]
        linkedin, email, blog, ads = st.tabs(["LinkedIn post", "Promotional email", "Short blog", "3 ad variations"])
        with linkedin:
            st.write(content["linkedin"])
        with email:
            st.markdown(f"**Subject:** {content['email']['subject']}")
            st.write(content["email"]["body"])
        with blog:
            st.subheader(content["blog"]["title"])
            st.write(content["blog"]["body"])
        with ads:
            for i, ad in enumerate(content["ads"], 1):
                st.markdown(f"**Ad {i}**")
                st.write(ad)
    if state["status"] == "awaiting_approval":
        st.subheader("Human Review Required")
        st.info("Read the strategy, all four formats and the critique. Approval confirms your review of this content. It does not publish or send anything.")
        unresolved = state["reviews"][-1]["verdict"] != "PASS"
        acknowledgement = False
        if unresolved:
            st.warning("The reviewer still found issues after two revisions. Review them carefully before approving, or generate a new campaign with a clearer brief.")
            acknowledgement = st.checkbox("I reviewed the remaining issues and accept this campaign.", key="acknowledge_issues")
        if st.button("Approve Final Campaign", type="primary", disabled=unresolved and not acknowledgement):
            approve_campaign(state, acknowledge_issues=acknowledgement)
            st.rerun()
    if state["status"] == "approved":
        st.success("Campaign Approved")
        st.caption("Approved content is ready to copy or download. No external content was posted or sent.")
        st.download_button("Download approved campaign (.md)", campaign_markdown(state),
                           file_name="approved_gtm_campaign.md", mime="text/markdown")
    with st.expander("Agent activity log / state"):
        st.json({"status": state["status"], "revision_count": state["revision_count"],
                 "approved": state["final_approved_content"] is not None, "events": state["events"]})
