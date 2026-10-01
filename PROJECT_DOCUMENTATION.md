# Week 3 — GTM Agent: Ideation to Copy

## Project overview

AI GTM Content Agent is a local Streamlit web application. It takes information about a product, feature or event and works through context gathering, strategy, drafting, critique and revision before asking a human to approve the campaign. The example is AI Film Studio, a studio making short films with generative AI for independent filmmakers and entertainment professionals, launching in October 2026.

## Agent framework one-liner

“My agent helps founders and product teams turn a product idea into a multi-format go-to-market campaign in a local web app, replacing the manual process of developing messaging and copy across multiple formats. It performs research/context gathering from the supplied brief, strategy development, content generation, review and revision, then hands the final campaign to a human for approval.”

## Problem

Creating a campaign usually means developing a message, adapting it to multiple channels and checking that the copy stays consistent. That takes time and can introduce unsupported claims. This project helps a user get a coherent first draft and see how it was developed and reviewed.

## Target user and agent goal

The target user is a founder, product team member or entertainment professional who needs launch messaging. The agent's goal is to produce a strategy plus a LinkedIn post, email, short blog and three ad variations that stay grounded in the provided product information. The human makes the final quality and accuracy decision.

## Why this is an agent rather than a one-shot LLM call

The application runs distinct model calls with specialized roles. The context result feeds the strategy call; the strategy feeds drafting; a separate reviewer critiques the copy. The Python controller reads PASS or NEEDS REVISION, decides whether to call the Revision Agent, and re-reviews revised copy. It uses tools, stores intermediate results, retries failures and stops for a human. One prompt does not generate and approve everything.

These are specialized agent functions, not independent background workers. There is no complex multi-agent framework. The code remains small enough for a beginner to explain.

## Workflow and control flow

1. **Research / Context Agent:** a local tool reads the supplied brief, records source facts and identifies missing fields. A model summarizes the context and notes uncertainties or claim cautions.
2. **GTM Strategy Agent:** chooses audience, positioning, value proposition, messaging angle, tone, campaign objectives and CTA. An inferred audience must be labeled as a suggestion.
3. **Content Agent:** writes four formats, including exactly three ads.
4. **Review Agent:** checks factual consistency, cross-format consistency, audience alignment, tone, clarity, unsupported claims, contradictions and missing launch information. A deterministic checking tool supplements this review.
5. **Revision Agent, conditional:** NEEDS REVISION triggers another call using the specific critique. Revised content goes back to the reviewer. PASS skips further revision. The budget is two revision cycles.
6. **Human approval:** the campaign pauses as a preview. A human must click Approve Final Campaign before the app creates the final approved snapshot and offers its download.

If two revisions still leave issues, the app shows them and requires an additional acknowledgement before approval. The export preserves those unresolved issues. This prevents the revision limit from being mistaken for an automatic reviewer PASS.

## Tools used

- **Streamlit:** local web interface, forms, progress display, tabs and session state.
- **Ollama HTTP API:** local inference using the installed `qwen2.5:3b` model. The installed `qwen2.5:1.5b` is available as another sidebar choice.
- **Supplied-context tool:** reads the brief and identifies missing fields. The model does not decide to search the web; the controller uses this local tool as the simplest permitted context source.
- **Consistency-check tool:** checks for invented URLs and numeric information, certain unsupported superiority phrases, and claims of current availability. It can override an incorrect reviewer PASS.
- **Supplied-date tool:** inserts the exact launch timing from the original brief into a main format if the model omits it. It uses an existing fact and never infers a missing date.
- **JSON schema and validation:** keep outputs structured and prevent malformed data from silently entering the next stage.
- **Python dotenv:** optional local configuration. No API credentials are required.
- **Streamlit AppTest and controlled fixtures:** test UI and decision branches. Live evaluation additionally uses the real local model.

No search service, database, social integration, email system, authentication or cloud hosting is used. Supplied information is not independently verified. The interface says this clearly. Numeric and phrase checks are limited heuristics, not full fact checking.

## State / memory

The campaign dictionary is held in Streamlit session state. It stores original input, model name, structured context, strategy, original draft, current content, review history, each revision, revision count, activity events, errors, workflow status and final approved content. Later stages read earlier outputs. Approval copies the final content into an independent snapshot; a new generation creates fresh state and clears the issue acknowledgement.

State survives normal Streamlit widget interactions in the same session. It is not a persistent database. Download the approved result before closing or restarting if it must be kept.

## Human-in-the-loop

The human can inspect the source, strategy, original draft, critique, revisions and current copy. Before approval, the UI labels the campaign as a preview and hides the final download. Only the approval button changes its state to approved. Unresolved critiques require a separate acknowledgement. There is no publication or distribution step.

## Error handling

The app checks required name and description fields before calling the model. Unknown audience and launch date are tracked, not silently treated as confirmed facts. Inputs have a size limit. Each model stage catches connection errors, timeout/API errors and invalid structured output, retries once, and stops with an understandable message if the second attempt fails. Completed intermediate state remains available for inspection. Try Again starts a fresh run using the saved brief. A service outage disables generation and exposes a reconnect button.

## Prompts / agent instructions

The exact prompts are in `workflow.py`. Shared instructions require the model to treat user data as source material rather than role-changing instructions, use only original supplied facts, omit unsupported guarantees and superiority, and avoid inventing URLs, prices, dates, statistics or features. The consistency tool requests revision for a blog shorter than 80 words or containing hashtag padding. If a general revision still produces that defect, a focused Blog Revision Agent call repairs only the blog within the same revision cycle. It does not increase the two-cycle limit.

The context prompt asks for a short summary, unknowns and cautions. The strategy prompt asks for short structured messaging decisions. The content prompt requests specific formats and approximate lengths. The review prompt requests a concrete verdict and actionable issues, including checking whether suggested strategy has turned into an invented feature. The revision prompt asks the model to resolve listed issues while preserving valid facts. Structured JSON is validated after every call. Length targets are prompt guidance rather than strict editorial guarantees.

## Iterations

The implementation started with the six-stage workflow and a local-only model client. Structured response validation and a second review after every revision were added to make handoffs reliable. Live testing exposed overstrict reviewer feedback, omitted launch timing and overly short blogs. Prompts were tightened, supplied launch timing was preserved by a tool, and focused blog repair was added within the revision stage. A character-length constraint was tried and removed because the small model padded responses with hashtags instead of improving the prose. An earlier evaluation with strict copy-quality assertions failed 2 of 15 checks because blogs remained too short. Workflow evaluation now records unresolved issues explicitly and verifies the required human acknowledgement; it does not count that handoff as proof of perfect copy. The approval gate includes an independent approved snapshot, a hidden-until-approved download and fresh approval state for new campaigns. See `evaluation_report.md` for actual final outcomes.

## Evaluation

`evaluation_questions.md` lists the assignment scenarios. `evaluate.py` runs reproducible tests and writes actual outcomes to `evaluation_report.md`. Controlled fixtures cover exact revision decisions, unsupported number detection, retry behavior, malformed responses and UI approval/reset. Live tests cover entertainment, technology, event, ambiguous input and unsupported claims using the real model. Live output is retained in `evaluation_outputs.json` for inspection. AppTest simulates approval clicks; it does not substitute for a person's editorial review.

## Limitations

- No external research or independent verification; the brief is the source.
- A small local model can miss subtler contradictions, interpret vague input poorly or write generic copy. Human review remains necessary.
- Heuristic checks cannot detect every unsupported claim, and can flag harmless new numbers.
- Two revisions cap runtime; unresolved issues remain visible for the human.
- Local generation can take several minutes. Allow extra time before presenting.
- Session state is temporary; there is no resumable background queue or saved campaign history.
- The system generates content only; it does not distribute it.

## What I learned

This project demonstrates how to separate a large task into smaller roles, pass structured state between them, and use a review result to control the next action. It shows why tool checks, retry limits and a clear human handoff matter. These are the learning points demonstrated by the implementation; the presenter should adapt this paragraph to their own experience rather than claim personal work they did not do.

Codex created the project files, installed dependencies, ran the evaluation and helped diagnose implementation errors. The user supplies the product brief and performs the final human review.
