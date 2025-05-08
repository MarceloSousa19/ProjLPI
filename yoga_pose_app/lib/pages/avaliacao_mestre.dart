import 'package:flutter/material.dart';
import 'package:yoga_pose_app/pages/feedback_final_page.dart';

class AvaliacaoMestrePage extends StatefulWidget {
  const AvaliacaoMestrePage({super.key});

  @override
  State<AvaliacaoMestrePage> createState() => _AvaliacaoMestrePageState();
}

class _AvaliacaoMestrePageState extends State<AvaliacaoMestrePage> {
  final List<String> poses = [
    'Koundinyasana',
    'Mayurasana',
    'Pungu_Mayurasana',
    'Tittibhasana',
    'Vrschikasana',
  ];

  int indiceAtual = 0;
  final List<double> precisoesObtidas = [];

  void avaliarPoseAtual() async {
    final pose = poses[indiceAtual];

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
            nivel: 'Mestre',
            precisoes: precisoesObtidas,
            nomesPoses: poses,
            mediaFinal: media,
            passou: passou,
          ),
        ),
      );
    } else {
      avaliarPoseAtual();
    }
  }

  Future<double> simularAvaliacao(String pose) async {
    await Future.delayed(const Duration(seconds: 1));
    return (60 + (pose.length % 40)).toDouble();
  }

  @override
  void initState() {
    super.initState();
    avaliarPoseAtual();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Avaliação - Mestre')),
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
