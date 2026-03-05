import json

def validate_json(response_text):
    try:
        data = json.loads(response_text)
        if "status" not in data:
            raise ValueError("Campo 'status' obrigatório")
        return True, data
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar JSON: {e}")
        