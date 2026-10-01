# 3–4 Minute Demo Script

## Before presenting

Start Ollama and the Streamlit app using the README command. Open http://localhost:8502 and check that the sidebar says Ollama connected with qwen2.5:3b selected. Generate the prefilled AI Film Studio campaign before the presentation and leave it **awaiting approval**. Read its copy and critique in advance.

Local generation adds waiting time. For a timed 3–4 minute presentation, use the completed preview to show the genuine stage log, source, strategy and review history. You can explain the Generate button without restarting the model. If a live generation is required, start it beforehand or allow additional time; do not imply that waiting was instantaneous.

## 0:00–0:30 — Introduce the app and input

“This is my Week 3 project, AI GTM Content Agent. It turns a product idea into a campaign across several formats. I focused on entertainment and AI products.

“Here are the inputs: product name, description, audience, launch date and additional context. My example is AI Film Studio, which creates short films with generative AI for independent filmmakers and entertainment professionals, launching in October 2026. I can replace this with another product, feature or event.”

Point to **Generate GTM Campaign**. If generating live, click it now and describe the next section while it works.

## 0:30–1:05 — Show the workflow

“This is a multi-step agent, rather than one prompt that writes everything. First, a context tool reads my supplied facts and identifies unknowns. Then a Research Agent analyzes that context, a Strategy Agent chooses the message and tone, and a Content Agent creates the copy.

“A separate Review Agent critiques it. The controller decides whether to revise. Each revision gets another review, up to two cycles. Finally, the app stops for me to approve the content.”

Point to the stage list and expand **Original brief and research/context**.

“For simple setup, research uses the brief I supplied. It does not search the web or claim independent fact verification.”

## 1:05–1:35 — Show strategy

Expand **GTM strategy**.

“Here the agent selects the audience, positioning, value proposition, messaging angle, tone and campaign objectives. It also chooses a consistent call to action. These decisions become input to the next agent.”

Read one actual positioning sentence and the actual tone from the current campaign. Do not read every field.

## 1:35–2:20 — Show the four formats

Open each tab briefly.

“This is the LinkedIn post. It introduces the studio in a professional social format.

“This is a promotional email with a subject and body.

“This is a short blog draft with a title and more room to explain the idea.

“And these are three ad variations. The formats use the same supplied facts and strategy.”

Read one short excerpt from the actual output. Point to launch timing and the CTA.

## 2:20–2:55 — Show critique and any revision

Expand **Review / critique and revision history**.

“The reviewer checks consistency, factual claims, audience alignment, tone and clarity. A Python tool also checks invented numbers and URLs. The review returns PASS or NEEDS REVISION.”

If a revision occurred:

“Here is an actual issue it found. The Revision Agent used that feedback, and this later review shows what happened after revision.”

If the first draft passed:

“This campaign passed its first review, so the controller correctly skipped revision. The revision branch is also tested in the evaluation report.”

If issues remain:

“The two-cycle limit stopped the loop. These remaining issues are shown explicitly, so I need to review them before accepting the copy.”

## 2:55–3:25 — Human approval and final result

Point to **Human Review Required**.

“It is still a preview. The agent cannot finish the campaign without my approval. I have read the copy and critique.”

Only if you accept the actual copy: acknowledge remaining issues if prompted, then click **Approve Final Campaign**.

“Now it says Campaign Approved, and I can download the package. This does not publish to social media or send email. Approval is only approval of the content.”

## 3:25–3:55 — State, reliability and build credit

Expand **Agent activity log / state** briefly.

“The app keeps the original brief, context, strategy, draft, reviews, revision count and approved content in session state. If a model request fails, it retries once and then stops with a clear message. I can click Try Again.

“The evaluation report separates real local-model runs from controlled tests of failures and decision branches. Codex was used to build and debug this application. I supplied the project requirements and product context, and I perform the final human review.”
