import json
import re
from typing import List, Dict, Any, Optional

class ClassifierValidator:
    def __init__(self, allowed_categories: List[str]):
        self.allowed_categories = [cat.lower() for cat in allowed_categories]

    def parse_json(self, raw_response: str) -> Dict[str, Any]:
        """
        Extrai e limpa o JSON da resposta da IA, tratando Markdown blocks.
        """
        try:
            # Remove blocos de código markdown se existirem
            clean_content = re.sub(r'```json|```', '', raw_response).strip()
            return json.loads(clean_content)
        except json.JSONDecodeError as e:
            print(f"Erro de Parsing: JSON inválido detectado. {e}")
            raise ValueError("Falha ao processar estrutura JSON.")

    def validate_category(self, data: Dict[str, Any]) -> str:
        """
        Verifica se a categoria retornada está na lista permitida.
        """
        category = data.get("categoria", "").lower()
        
        if category in self.allowed_categories:
            return category
        
        raise ValueError(f"Categoria '{category}' não é permitida.")

    def fallback_mechanism(self, error_msg: str) -> Dict[str, str]:
        """
        Retorno seguro caso tudo falhe.
        """
        return {
            "categoria": "Nao_Classificado",
            "status": "erro",
            "log": error_msg
        }

    def execute_safe_classification(self, raw_response: str) -> Dict[str, Any]:
        """
        Orquestrador: Tenta processar e validar, senão aciona o fallback.
        """
        try:
            parsed_data = self.parse_json(raw_response)
            validated_cat = self.validate_category(parsed_data)
            
            return {
                "categoria": validated_cat,
                "status": "sucesso",
                "confianca": parsed_data.get("confianca", 0)
            }
        except Exception as e:
            return self.fallback_mechanism(str(e))