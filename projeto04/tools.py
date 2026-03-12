import random
import string

def gerar_senha(tamanho=12):
    """Gera uma senha aleatória segura."""
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(int(tamanho)))

def converter_temperatura(valor, de="C", para="F"):
    """Converte entre Celsius e Fahrenheit."""
    if de.upper() == "C":
        res = (float(valor) * 9/5) + 32
        return f"{res:.2f} °F"
    else:
        res = (float(valor) - 32) * 5/9
        return f"{res:.2f} °C"

# Lista de definições para a API da OpenAI entender as funções
tools_spec = [
    {
        "type": "function",
        "function": {
            "name": "gerar_senha",
            "description": "Gera uma senha aleatória segura",
            "parameters": {
                "type": "object",
                "properties": {"tamanho": {"type": "integer"}},
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "converter_temperatura",
            "description": "Converte temperatura entre C e F",
            "parameters": {
                "type": "object",
                "properties": {
                    "valor": {"type": "number"},
                    "de": {"type": "string", "enum": ["C", "F"]},
                    "para": {"type": "string", "enum": ["C", "F"]}
                },
                "required": ["valor", "de", "para"]
            }
        }
    }
]