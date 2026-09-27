import sys

print("starting")
try:
    from app.ai.graph import build_graph

    print("imported build_graph")
except Exception as e:
    print("error", e)
print("done")
