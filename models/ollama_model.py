from langchain_ollama import OllamaLLM

def load_llama_model(callbacks=None):
    return OllamaLLM(model="llama3.1", streaming=True, callbacks=callbacks)