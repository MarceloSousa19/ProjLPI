
from datetime import datetime

def mostrar_feedback_final(nivel, nomes_poses, precisoes_poses, media_final, passou):


    data_hoje = datetime.now().strftime("%Y-%m-%d")

    print("\n🏁 Resultado Final do Nível:", nivel.upper())
    print(f"Data: {data_hoje}")
    print("-" * 60)

    for nome, precisao in zip(nomes_poses, precisoes_poses):
        print(f"Pose: {nome} - Precisão: {precisao}%")

    print("-" * 60)
    print(f"🎯 Média Final: {media_final}%")

    if passou:
        print("✅ Resultado: Passou o nível!")
    else:
        print("❌ Resultado: Não passou o nível.")
    print("=" * 60)
