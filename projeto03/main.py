import os
from dotenv import load_dotenv
from openai import OpenAI
from retriever import Retriever
from validator import SecurityValidator

# Carrega as variáveis do .env
load_dotenv()

# Configuração específica para GROQ
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def main():
    # Inicializa o Retriever (agora não precisa do client para embeddings)
    retriever = Retriever("conhecimento/conhecimento.txt")
    
    print("\n--- Assistente GROQ com RAG e Segurança ---")
    user_query = input("Sua pergunta: ")

    # 1. Proteção contra Prompt Injection (Parte 2 do Desafio)
    if SecurityValidator.is_prompt_injection(user_query):
        print(SecurityValidator.get_safe_error())
        return

    # 2. RAG: Recuperação de contexto (Parte 1 do Desafio)
    context = retriever.get_relevant_context(user_query)

    # 3. Geração da Resposta usando Groq (ex: modelo Llama-3)
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Modelo comum na Groq
            messages=[
                {"role": "system", "content": f"Você é um assistente útil. Use o contexto abaixo para responder.\nContexto: {context}"},
                {"role": "user", "content": user_query}
            ],
            temperature=0
        )
        print("\nResposta:", response.choices[0].message.content)
    except Exception as e:
        print(f"Erro na Groq: {e}")

if __name__ == "__main__":
    main()