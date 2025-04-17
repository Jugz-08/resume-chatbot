from openai import OpenAI

class RetrieverAgent:
    def __init__(self, resume_text):
        self.resume_text = resume_text

    def get_context(self, query):
        return self.resume_text              # For demo: return full resume. For production, use vector search.

class ReasoningAgent:
    def __init__(self, openai_api_key, retriever_agent):
        self.openai_api_key = openai_api_key
        self.retriever_agent = retriever_agent

    def answer(self, query, history):
        context = self.retriever_agent.get_context(query)
        prompt = (
            "You are the candidate described in the following resume. "
            "Answer as yourself, using only the information in the resume.\n\n"
            f"Resume:\n{context}\n\n"
            "Conversation history:\n"
            + "\n".join([f"Q: {h['user']}\nA: {h['bot']}" for h in history[-5:]])
            + f"\nQ: {query}\nA:"
        )
        client = OpenAI(api_key=self.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content  
