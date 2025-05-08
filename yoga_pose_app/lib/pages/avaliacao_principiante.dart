import 'package:flutter/material.dart';
import 'package:yoga_pose_app/pages/feedback_final_page.dart';

class AvaliacaoPrincipiantePage extends StatefulWidget {
  const AvaliacaoPrincipiantePage({super.key});

  @override
  State<AvaliacaoPrincipiantePage> createState() => _AvaliacaoPrincipiantePageState();
}

class _AvaliacaoPrincipiantePageState extends State<AvaliacaoPrincipiantePage> {
  final List<String> poses = [
    'Adho_Mukha_Svanasana',
    'Balasana',
    'Bitilasana',
    'Marjaryasana',
    'Padmasana',
    'Phalakasana',
    'Setu_Bandha_Sarvangasana',
    'Sivasana',
    'Utkatasana',
    'Vrksasana',
  ];

  int indiceAtual = 0;
  final List<double> precisoesObtidas = [];

  void avaliarPoseAtual() async {
    final pose = poses[indiceAtual];

    // Simular avaliação (substituir com lógica real)
    final double precisao = await simularAvaliacao(pose);

    setState(() {
      precisoesObtidas.add(precisao);
      indiceAtual++;
    });

    if (indiceAtual >= poses.length) {
      final double media = precisoesObtidas.reduce((a, b) => a + b) / precisoesObtidas.length;
      final bool passou = precisoesObtidas.every((p) => p >= 70) && media >= 80;

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => FeedbackFinalPage(
            nivel: 'Principiante',
            precisoes: precisoesObtidas,
            nomesPoses: poses,
            mediaFinal: media,
            passou: passou,
          ),
        ),
      );
    } else {
      avaliarPoseAtual(); // Avaliação contínua
    }
  }

  Future<double> simularAvaliacao(String pose) async {
    await Future.delayed(const Duration(seconds: 1));
    return (60 + (pose.length % 40)).toDouble(); // Simulação simples
  }

  @override
  void initState() {
    super.initState();
    avaliarPoseAtual();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Avaliação - Principiante')),
      body: Center(
        child: indiceAtual < poses.length
            ? Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('📸 A preparar para avaliar a pose:'),
            const SizedBox(height: 20),
            Text(
              poses[indiceAtual].replaceAll('_', ' '),
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 40),
            const CircularProgressIndicator(),
          ],
        )
            : const Text('A terminar...'),
      ),
    );
  }
}
