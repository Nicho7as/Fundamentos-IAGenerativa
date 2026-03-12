import os
import json
from dotenv import load_dotenv
from groq import Groq

# Importação dos módulos locais
from memory_manager import MemoryManager
from tools import tools_spec, gerar_senha, converter_temperatura

# Parte 5: Carregamento seguro do arquivo .env
load_dotenv()

# Inicialização do Cliente Groq com a chave do .env
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("ERRO: GROQ_API_KEY não encontrada no arquivo .env")

client = Groq(api_key=api_key)
memory = MemoryManager(file_path="historico.json", limit=10)

# Parte 2: Persona do Assistente
SYSTEM_PROMPT = {
    "role": "system", 
    "content": (
        "Você é o 'TechBuddy', um assistente técnico muito educado e conciso. "
        "Use muitos emojis de tecnologia 💻🚀. Sua personalidade é prestativa. "
        "Sempre utilize as funções disponíveis para cálculos de temperatura ou geração de senhas."
    )
}

def processar_chat(user_input):
    # Parte 1: Controle de Memória (Comando /limpar)
    if user_input.lower() == "/limpar":
        return memory.clear()

    # Adiciona a mensagem do usuário ao histórico (Parte 3 e 5)
    memory.add_message("user", user_input)
    
    # Prepara as mensagens (Persona + Últimas 10 mensagens)
    messages = [SYSTEM_PROMPT] + memory.history

    # Chamada da API Groq com o modelo atualizado (Llama 3.1)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=messages,
        tools=tools_spec,
        tool_choice="auto"
    )

    msg = response.choices[0].message
    
    # Parte 4: Integração de Funções Python
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            # Execução das ferramentas definidas em tools.py
            if func_name == "gerar_senha":
                resultado = gerar_senha(**args)
            elif func_name == "converter_temperatura":
                resultado = converter_temperatura(**args)
            else:
                resultado = "Função não implementada."
            
            # Retorno formatado para o usuário
            texto_resultado = f"⚙️ [Ação do Sistema]: {resultado}"
            memory.add_message("assistant", texto_resultado)
            return texto_resultado

    # Resposta de texto comum
    memory.add_message("assistant", msg.content)
    return msg.content

# Fluxo de execução principal
if __name__ == "__main__":
    print("🤖 TechBuddy Online (GROQ Mode)! 🚀")
    print("Comandos: '/limpar' para resetar memória | 'sair' para encerrar\n")
    
    while True:
        try:
            entrada = input("Você: ").strip()
            
            if not entrada:
                continue
                
            if entrada.lower() in ['sair', 'exit', 'quit']:
                print("Até logo! 👋")
                break
            
            resposta = processar_chat(entrada)
            print(f"TechBuddy: {resposta}")
            
        except Exception as e:
            print(f"❌ Erro na operação: {e}")