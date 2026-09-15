# Team Meeting Simulation - FitnessRAG Sprint 1 Review
Date: 2026-09-05

## Opening

**Karan (BA/Scrum Master):** Alright team, let's do a quick recap. From our last session, Checkpoints 1-3 are marked DONE in the SPRINT_TRACKER.md. Checkpoint 4 (AI & Knowledge Retrieval) is currently IN PROGRESS, which is Ravi's responsibility. We've got the LangGraph agent built in backend/app/ai/graph.py, conversation persistence working with the models and API endpoints, and the chat API endpoint at backend/app/api/v1/chat.py ready to go. The frontend is currently using MSW mocks as seen in frontend/src/mocks/handlers.ts, and we're planning to switch to real API calls soon.

**Priya (CPO):** Today's agenda is to review the code review results that were just shared and discuss Ravi's technical concerns about Checkpoint 4. We need to determine if the current approach is MVP-appropriate, if we need to re-evaluate our earlier architecture decisions (like LangGraph/Ollama), and what concrete actions we should take before moving forward.

**Founder (You):** Thanks, Karan and Priya. I've seen the code review results—three issues ranging from a potential crash bug to misleading error handling and a data-consistency edge case. I've also seen Ravi's detailed concerns about over-engineering the LangGraph pipeline for an MVP and the operational reality of relying on Ollama locally. My specific questions for the team are: Are those concerns valid? Do we need to roll back any of the decisions we made earlier on the tech stack, or can we address them with incremental improvements? Let's hear from everyone.

## Discussion

**Priya (CPO):** Let's start with the code review. The crash bug in ChatContainer.tsx is a clear reliability issue—if a user somehow has empty name/email fields, the chat UI blows up. That's unacceptable for an MVP; we need to fix it before we even think about switching off mocks. Looking at the code, line 65 tries to access [0] on what could be an empty string without checking. The API interceptor problem is more of a UX polish item, but it's confusing for users to see a 'backend not reachable' error when it's actually an auth issue. The conversation-title edge case is low risk, but we should guard against empty titles just in case—maybe default to 'New Conversation' or something similar.

**Arjun (CTO):** I agree with Priya on the crash bug—fix it now. On the interceptor, we can simply not reject the promise after redirecting, or better yet, throw a custom error that the UI can handle gracefully. As for Ravi's concerns: I share his worry about Ollama. Running local LLMs on limited dev/resources will bite us in concurrent scenarios. We need a fallback strategy—maybe a managed API (OpenAI/Anthropic) as a secondary provider, with circuit-breaker logic. That said, I don't think we should abandon LangGraph; it gives us a clean place to plug in fallback logic without rewriting the whole graph. Looking at the graph.py file, we already have a nice modular structure with separate nodes for safety_check, retrieve, generate, and output_safety. Adding fallback logic in the generate node or as a wrapper around the LLM call would be straightforward.

**Ravi (Tech Lead):** Thanks for hearing me out. Let me be clear: I'm not saying we should scrap LangGraph. What I'm saying is that for an MVP we might be *over-engineering* the retrieval layer. Right now we have hybrid search (vector + BM25 + RRF) in retrieval.py, a multi-node safety pipeline, and async/sync session juggling in chat.py. If the core user need is 'get a safe, cited fitness answer fast,' we could start with a simpler retrieval chain—say, just vector search with a basic safety check—and iterate. That would let us validate the value prop sooner and reduce cognitive load. Looking at retrieval.py, I see we're doing vector search, BM25, and then RRF fusion. For MVP, maybe we just need the vector search part to prove the concept.

On Ollama: I've looked at the latency numbers in my local tests—generation takes 1.5-2.5s on CPU, which is okay for a single user but will queue under load. We absolutely need a timeout wrapper and a fallback. I suggest we add a LLMProvider abstraction that tries Ollama first, then falls back to a cloud LLM if Ollama times out or returns an error. We can configure the fallback via env vars so we can toggle it in different environments. Looking at the _get_llm() function in graph.py, that's where we'd want to make this change.

**Meera (Backend):** I'll jump in on the DB side. The code review didn't flag it, but I noticed we're missing indexes on messages.conversation_id and messages.timestamp. Those will hurt as we scale. Looking at the message.py model, we have the foreign key but no explicit index. I'll add them in a migration. Also, Ravi's point about observability is spot-on—we should log retrieval latency, LLM call time, and token usage. That'll give us the data to decide when the fallback is needed. We could add this in the retrieve and generate nodes in graph.py.

**Zara (Frontend):** From my side, the API contract is solid. Once we fix the crash bug and the interceptor, switching from mocks to real calls should be smooth. Looking at the mock handler in frontend/src/mocks/handlers.ts, I notice it returns a fixed UUID for conversation_id, but the real API returns integers as seen in chat.py line 122. We'll need to adjust our frontend types to handle this. For the safety tier, I'll implement the subtle badge with tooltip and ARIA label as we discussed earlier in the MOM—maybe next to the timestamp as mentioned.

**Vikram (QA/DevOps):** I'll write property-based tests for the safety checker—covering edge cases like mixed safe/dangerous terms, medical terms not in our keyword lists, and Unicode/obfuscation attempts. Looking at the _DANGEROUS_KEYWORDS and _MEDICAL_KEYWORDS sets in graph.py lines 78-86, I see we're doing simple keyword matching. There are definitely edge cases we're missing. I'll also add a health check for the Ollama service in our Docker Compose (a simple /api/tags curl) and make sure our CI pipelines fail if Ollama isn't reachable in test mode. Looking at the docker-compose.yml, we don't currently have an Ollama service defined—we're relying on an external ollama:11434 host.

**Karan (BA/Scrum Master):** Let me capture the themes I'm hearing:

- The code review issues are real and need fixing before we go live with real API calls.
- Ravi's concerns about over-engineering and Ollama operational risk are valid, but they don't warrant scrapping LangGraph—they point to refinements: simplify retrieval for MVP, add observability, and implement a graceful LLM fallback.
- The team agrees we should keep the LangGraph orchestration as it provides a clean extension point for those refinements.

## Closing

**Karan (BA/Scrum Master):** Here's what we've decided:

✅ **Decisions Made:**
- Fix the three code-review issues immediately (crash bug in ChatContainer.tsx, API interceptor UX, empty title guard in chat.py).
- Keep LangGraph as the orchestration layer—it's the right abstraction for adding fallback logic and observability.
- Adopt a two-tier LLM strategy: primary = Ollama (local), secondary = managed cloud LLM (OpenAI/Anthropic) via env-configurable fallback.
- Simplify the retrieval pipeline for MVP to vector search + basic safety check; we can layer on hybrid search and RRF in later sprints after we validate user value.
- Add database indexes on messages.conversation_id and messages.timestamp.
- Add observability logging for retrieval latency, LLM call time, and token usage.

❓ **Open Questions:**
- What specific cloud LLM provider should we use as fallback (OpenAI vs Anthropic), and what are the cost/latency trade-offs? (Arjun/Ravi to spike)
- How aggressive should our Ollama timeout be before triggering fallback? (Vikram to propose based on load-test data)

🚫 **Rejected:**
- Completely removing LangGraph or switching to a plain retrieval chain—too much rework and loses extensibility.
- Delaying the switch from MSW mocks to real API calls until all concerns are resolved—we can fix the bugs and add fallbacks incrementally while still testing against the real endpoint.

📌 **Action Items:**
- [ ] **Zara**: Fix ChatContainer.tsx crash bug and update conversation_id types. (Due: EOD)
- [ ] **Zara**: Implement safety-tier badge with tooltip/ARIA labeling. (Due: Next sprint)
- [ ] **Frontend Team**: Adjust API interceptor to avoid showing misleading error on 401. (Due: EOD)
- [ ] **Meera**: Add DB indexes for conversation_id and timestamp in messages table. (Due: Tomorrow)
- [ ] **Vikram**: Write property-based tests for safety classifier edge cases. (Due: End of sprint)
- [ ] **Vikram**: Add Ollama health check to Docker Compose and CI. (Due: End of sprint)
- [ ] **Ravi**: Design LLMProvider abstraction with Ollama primary and cloud fallback; add timeout/retry logic. (Due: End of sprint)
- [ ] **Ravi**: Add observability logs for retrieval/LLM latency and token usage. (Due: End of sprint)
- [ ] **Arjun**: Spike cloud LLM fallback options (cost, latency, API keys). (Due: Next sync)
- [ ] **All**: Prepare to switch frontend from MSW mocks to real API calls after crash bug and interceptor fixes are deployed. (Target: Start of next sprint)

**Priya (CPO):** Looking ahead, next session we'll review the fixes, see the fallback design, and confirm the simplified MVP retrieval path is delivering user value.

--- 

*End of meeting.*