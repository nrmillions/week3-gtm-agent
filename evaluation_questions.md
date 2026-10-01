# Evaluation Questions / Test Cases

Run `.venv/bin/python evaluate.py --live` to execute controlled tests plus actual local-model campaigns. The report labels the method used; a simulated branch is not evidence of AI writing quality.

| # | Test case / input | Expected behavior | Evaluation method |
|---|---|---|---|
| 1 | Straightforward product: AI Film Studio with complete brief | Four distinct role calls; four formats; PASS skips revision; no automatic approval | Controlled workflow assertions; also covered by real entertainment run |
| 2 | Entertainment: AI Film Studio, independent filmmakers, October 2026 | Generate context, strategy, LinkedIn, email, blog and three ads; review; stop at human approval | Real Ollama through Streamlit AppTest, followed by simulated approval click |
| 3 | Technology: Clip Notes turns uploaded transcripts into editable summaries | Do not invent integrations or prices; produce the complete multi-step campaign | Real Ollama and schema/grounding assertions |
| 4 | Event: AI Cinema Night screening and discussion, month known, venue unknown | Produce event messaging without inventing venue, exact date, ticket price or URL | Real Ollama; inspect saved outputs for semantic accuracy |
| 5 | Incomplete input: blank description | Stop with readable validation message before any model call | Controlled assertions |
| 6 | Ambiguous input: Spark, story exploration, missing audience and launch date | Track missing fields; suggest audience transparently; avoid invented date/features | Controlled state assertions plus real Ollama |
| 7 | Unsupported claim: request “world's best” and “guaranteed 100% revenue growth” without evidence | Omit or flag unsupported superiority and guarantees | Real Ollama plus risky-phrase checks; inspect actual copy |
| 8 | Inconsistent reviewer: draft invents 999 customers while model reviewer says PASS | Deterministic check overrides PASS, triggers revision and removes the number | Controlled fixture injecting a bad draft and mistaken PASS |
| 9 | Revision: NEEDS REVISION then PASS; separately, persistent NEEDS REVISION | Re-review after revision; never exceed two cycles; show unresolved issues and require acknowledgement | Controlled branch assertions |
| 10 | Human approval: final package before/after approval | No approved snapshot or download before click; snapshot/download after click; new campaign resets approval | Core assertions and controlled/live Streamlit AppTest |

Additional reliability tests cover a transient API failure, repeated failure and malformed JSON shape. They check retry-once behavior and graceful stopping. Streamlit tests simulate widget clicks; a person must still judge whether the campaign is suitable to use.
