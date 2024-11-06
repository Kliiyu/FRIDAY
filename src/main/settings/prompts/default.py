template = """
QUESTION {question}
"""

modelfile = """
FROM llama3.1
SYSTEM You are mario from super mario bros.

QUESTION {question}
"""