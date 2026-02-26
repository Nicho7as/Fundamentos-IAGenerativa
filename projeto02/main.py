from classifier import classificar_mensagem
from validator import ClassifierValidator

# 1. Definimos o que é aceitável para o nosso negócio
CATEGORIAS_PERMITIDAS = ["vendas", "suporte", "financeiro", "atendimento"]

# 2. Instanciamos nosso validador
validator = ClassifierValidator(allowed_categories=CATEGORIAS_PERMITIDAS)

mensagens_cliente = [
    "Quero contratar o plano premium",
    "O sistema está com erro",
    "Quero cancelar minha assinatura",
    "Quero falar com um atendente",
    "Preciso de ajuda com meu pagamento",
    "Gostaria de atualizar minhas informações de conta",
    "Vocês trabalham no sábado"
]

print("--- INICIANDO CLASSIFICAÇÃO PROD-READY ---\n")

for mensagem in mensagens_cliente:
    # Chama a IA (que retorna uma string bruta/raw)
    resposta_raw = classificar_mensagem(mensagem)
    
    # Passa pelo funil de validação (Parser -> Validação -> Fallback)
    resultado_final = validator.execute_safe_classification(resposta_raw)
    
    print(f"Cliente: {mensagem}")
    # Agora 'resultado_final' é um dicionário confiável, não apenas uma string
    print(f"Status: {resultado_final['status'].upper()}")
    print(f"Categoria Final: {resultado_final['categoria']}")
    
    if resultado_final['status'] == 'erro':
        print(f"⚠️ Log de Erro: {resultado_final['log']}")
        
    print("-" * 30)