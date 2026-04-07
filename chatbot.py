import requests
from simulacoes import detectar_simulacao

OLLAMA_URL = "http://localhost:11434/api/generate"

def responder(pergunta, historico):

    pergunta_lower = pergunta.lower()

    # 🧠 PRIMEIRO tenta simulação (ANTES DE BLOQUEAR)
    resultado_simulacao, historico = detectar_simulacao(pergunta)

    if resultado_simulacao:
        return resultado_simulacao, historico

    # 🔒 BLOQUEIO DE ASSUNTOS FORA DE FINANÇAS
    palavras_financeiras = [
        "juros", "investimento", "investir", "dinheiro", "renda",
        "gasto", "guardar", "economizar", "finança",
        "cartão", "divida", "dívida", "emprestimo", "empréstimo", "salário"
    ]

    if not any(p in pergunta_lower for p in palavras_financeiras):
        return "Posso te ajudar apenas com assuntos financeiros 😊"

    # 🧠 RESPOSTA CONTROLADA
    if "juros composto" in pergunta_lower or "juros compostos" in pergunta_lower:
        return "Juros compostos são juros calculados sobre o valor inicial e também sobre os juros acumulados ao longo do tempo. Ou seja, são juros sobre juros."
    # 🔢 Simulação
    resultado_simulacao = detectar_simulacao(pergunta)
    
    if resultado_simulacao:
        return resultado_simulacao

    # 📚 Contexto
    contexto = ""
    for autor, msg in historico[-5:]:
        contexto += f"{autor}: {msg}\n"

    # 🧠 Prompt
    prompt = f"""
Você é um assistente financeiro brasileiro.

Responda SOMENTE em português do Brasil.

Nunca invente informações.
Se não souber, diga que não sabe.

Responda apenas perguntas relacionadas a finanças pessoais.

Se a pergunta não for sobre finanças, responda:
"Posso te ajudar apenas com assuntos financeiros 😊"

Explique de forma simples, clara e objetiva.

Contexto:
{contexto}

Pergunta:
{pergunta}

Resposta:
"""

    # 🔗 Chamada API
    response = requests.post(OLLAMA_URL, json={
        "model": "phi",
        "prompt": prompt,
        "stream": False
    })

    data = response.json()

    # 🛡️ Tratamento
    if "response" in data:
        return data["response"], None
    else:
        return f"Erro na resposta da IA: {data}", None