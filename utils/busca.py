def invalidar_busca_se_alterada(estado, criterios):
    """Resultados e período gravado pertencem exatamente aos filtros exibidos."""
    if estado.get("criterios_busca") != criterios:
        for chave in list(estado):
            if chave.startswith("busca_"):
                del estado[chave]
        estado["resultado_busca"] = None
        estado["criterios_busca"] = criterios
