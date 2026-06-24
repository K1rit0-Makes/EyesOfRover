from langchain_ollama import ChatOllama


USE_REMOTE_LLM = False 

REMOTE_IP = "100.98.144.54"

REMOTE_PORT = 14434


def get_llm():

    if USE_REMOTE_LLM:

        return ChatOllama(
            model="qwen3.5:latest",
            base_url=f"http://{REMOTE_IP}:{REMOTE_PORT}",
            temperature=0
        )

    return ChatOllama(
        model="qwen3.5:latest",
        temperature=0
    )