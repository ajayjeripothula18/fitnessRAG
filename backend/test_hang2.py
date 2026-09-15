from app.ai.graph import node_safety_check
def _base_state(**kwargs):
    return {
        "user_query": "",
        "conversation_history": [],
        "db": None,
        "safety_tier": "",
        "safety_message": "",
        "retrieved_chunks": [],
        "response": "",
        "citations": [],
        "skip_generation": False,
        **kwargs,
    }

print("starting node_safety_check")
state = node_safety_check(_base_state(user_query="Best exercises for core strength?"))
print("done", state)
