#RAG Simplificado

def load_conhecimento():
    with open("projeto03/conhecimento/conhecimento.txt", "r", encoding="utf-8") as f:
        return f.read()


def simple_retriever(query, conhecimento):
    query = query.lower()
    conhecimento = conhecimento.lower()

    relevant_chunks = []
    sections = conhecimento.split("\n\n")  # Supondo que cada seção seja separada por duas quebras de linha

    for section in sections:
        if query in section:
            relevant_chunks.append(section)
            print(f"Trecho relevante encontrado: {section[:100]}...")
    return "\n\n".join(relevant_chunks) if relevant_chunks else "Desculpe, não encontrei informações relevantes."
