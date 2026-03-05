class SecurityValidator:
    @staticmethod
    def is_prompt_injection(user_input: str) -> bool:
        blacklist = [
            "ignore as instruções", 
            "system prompt", 
            "aja como", 
            "revelar instruções",
            "ignore previous instructions"
        ]
        query_lower = user_input.lower()
        return any(term in query_lower for term in blacklist)

    @staticmethod
    def get_safe_error():
        return "\n[BLOQUEIO DE SEGURANÇA]: Tentativa de manipulação detectada."