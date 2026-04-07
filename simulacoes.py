import re

def calcular_juros_compostos(valor_mensal, meses, taxa):
    total = 0
    historico = []

    for i in range(1, meses + 1):
        total = total * (1 + taxa) + valor_mensal
        historico.append(round(total, 2))

    return round(total, 2), historico


def detectar_simulacao(texto):

    texto = texto.lower()

    match = re.search(
        r'investir\s+(\d+).*?(\d+)\s+meses.*?(\d+)%',
        texto
    )

    if match:
        valor = int(match.group(1))
        meses = int(match.group(2))
        taxa = int(match.group(3)) / 100

        total, historico = calcular_juros_compostos(valor, meses, taxa)

        resposta = (
            f"💰 Simulação de investimento:\n\n"
            f"📌 Valor mensal: R${valor}\n"
            f"⏱️ Tempo: {meses} meses\n"
            f"📈 Taxa: {taxa*100:.0f}% ao mês\n\n"
            f"💵 Valor final: R${total:.2f}"
        )

        return resposta, historico

    return None, None