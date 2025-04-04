# 🧘 Identificador de Poses de Yoga com MediaPipe

Este módulo identifica poses de yoga em tempo real usando a webcam, com o auxílio do **MediaPipe** e **OpenCV**.  
Também permite guardar novas poses com base nos ângulos articulares.

---

## 📦 Requisitos

- Python 3.11
- Webcam funcional
- Ficheiros:
  - `main.py` — identificação em tempo real
  - `extrair_pose_imagem.py` — extrair ângulos de imagens
  - `poses.json` — base de dados de poses
  - Pasta `imagens/` — imagens para registar novas poses

---

## 🔧 Instalação

```bash
pip install opencv-python mediapipe numpy
```

---

## 🚀 Como Usar

### 📍 1. Identificar poses com a webcam

```bash
python main.py
```

- ▶️ Pressiona `q` para sair  
- 💾 Pressiona `g` para guardar a pose atual no JSON  
- ✏️ O nome da pose será solicitado no terminal  
- 🖼️ O nome da pose identificada aparece no canto da imagem


### 📍 2. Extrair poses a partir de uma imagem

```bash
python extrair_pose_imagem.py
```

- Introduz o caminho da imagem (ex: `imagens/Tree.jpg`)
- Introduz o nome da pose (ex: `Tree Pose (direita)`)
- Os 8 ângulos da pose serão calculados e guardados no ficheiro `poses.json`

---

## 🧠 Estrutura dos ângulos guardados

Cada pose guarda **8 ângulos**:

| Índice | Ângulo entre...                    |
|--------|------------------------------------|
| [0]    | Ombro → Cotovelo → Pulso (direito) |
| [1]    | Ombro → Cotovelo → Pulso (esquerdo)|
| [2]    | Cotovelo → Ombro → Anca (direito)  |
| [3]    | Cotovelo → Ombro → Anca (esquerdo) |
| [4]    | Ombro → Anca → Joelho (direito)    |
| [5]    | Ombro → Anca → Joelho (esquerdo)   |
| [6]    | Anca → Joelho → Tornozelo (direito)|
| [7]    | Anca → Joelho → Tornozelo (esquerdo)|

---

## 📁 Exemplo de `poses.json`

```json
{
  "Warrior II (direita)": [169, 174, 95, 83, 89, 122, 98, 178],
  "Warrior II (esquerda)": [174, 169, 83, 95, 122, 89, 178, 98],
  "Tree Pose (direita)": [160, 160, 85, 85, 175, 125, 95, 170]
}
```

---

## 📌 Dicas

- Podes usar imagens para registar poses sem executá-las ao vivo
- O nome da pose deve indicar o lado (ex: `Tree Pose (esquerda)`)
- A tolerância angular pode ser ajustada no `main.py` (`tolerancia_angular`)
- Os ângulos atuais são mostrados a cada 10 segundos no terminal

---

## ✅ Conclusão

Este módulo é ideal para usar com sistemas de treino, avaliação ou feedback visual de posições corporais.
Ainda em execução.