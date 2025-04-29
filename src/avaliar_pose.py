# src/avaliar_pose.py

import json
import os
import sys
from datetime import datetime

# Se necessário garantir que src está no path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.historico_individual import guardar_historico_individual
from src.recorde_pessoal import atualizar_recorde_pessoal

def avaliar_pose(angulos_referencia, angulos_utilizador, nome_pose=None):
    """
    Avalia a precisão de uma pose com base nos ângulos de referência e do utilizador.
    Se nome_pose for fornecido, também guarda no histórico e atualiza recorde.

    Args:
        angulos_referencia (dict): Ângulos ideais da pose.
        angulos_utilizador (dict): Ângulos capturados do utilizador.
        nome_pose (str, optional): Nome da pose (para histórico e recorde).

    Returns:
        precisao (float): Precisão global da pose.
        feedback (list of str): Lista de correções sugeridas.
    """

    tolerancia = 10  # tolerância permitida em graus
    total = len(angulos_referencia)
    corretos = 0
    feedback = []

    for chave in angulos_referencia:
        angulo_ref = angulos_referencia[chave]
        angulo_user = angulos_utilizador.get(chave, None)

        if angulo_user is None:
            feedback.append(f"Não foi possível medir o ângulo de {chave}.")
            continue

        diferenca = abs(angulo_ref - angulo_user)

        if diferenca <= tolerancia:
            corretos += 1
        else:
            if "elbow" in chave:
                feedback.append("Ajuste o cotovelo " + ("direito" if "right" in chave else "esquerdo"))
            elif "shoulder" in chave:
                feedback.append("Ajuste o braço " + ("direito" if "right" in chave else "esquerdo"))
            elif "hip" in chave:
                feedback.append("Ajuste a anca " + ("direita" if "right" in chave else "esquerda"))
            elif "knee" in chave:
                feedback.append("Ajuste o joelho " + ("direito" if "right" in chave else "esquerdo"))

    precisao = (corretos / total) * 100
    precisao = round(precisao, 2)

    # 🆕 Guardar histórico e atualizar recorde se nome_pose for fornecido
    if nome_pose:
        print(f"📸 Avaliando pose: {nome_pose}")
        print(f"🎯 Precisão obtida: {precisao}%")
        
        guardar_historico_individual(nome_pose, precisao)
        print(f"📂 Histórico individual atualizado para a pose '{nome_pose}'.")
        
        atualizar_recorde_pessoal(nome_pose, precisao)
        print(f"🏆 Verificado/Atualizado recorde pessoal para a pose '{nome_pose}'.")
        print("-" * 60)

    return precisao, feedback
