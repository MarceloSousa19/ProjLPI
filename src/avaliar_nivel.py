

def avaliar_nivel(precisoes_poses):
    """
    Avalia se o utilizador passou o nível com base nas precisões das poses.

    Args:
        precisoes_poses (list of float): Lista com as precisões individuais das 10 poses.

    Returns:
        media (float): Média final das precisões.
        passou (bool): True se passou o nível, False caso contrário.
        feedback (str): Mensagem de resultado.
    """

    # Verifica se a lista tem 10 entradas
    if len(precisoes_poses) != 10:
        raise ValueError("São necessárias exatamente 10 avaliações de poses para concluir o nível.")

    # Calcula a média
    media = sum(precisoes_poses) / len(precisoes_poses)

    # Condições para passar:
    todas_acima_70 = all(p >= 70 for p in precisoes_poses)
    media_acima_80 = media >= 80

    if todas_acima_70 and media_acima_80:
        passou = True
        feedback = "✅ Parabéns! Passaste o nível!"
    else:
        passou = False
        feedback = "❌ Não passaste o nível. Continua a treinar!"

    return round(media, 2), passou, feedback
