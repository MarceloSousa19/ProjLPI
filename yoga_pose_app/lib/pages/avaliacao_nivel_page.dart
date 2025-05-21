import 'dart:math';
import 'package:flutter/material.dart';
import 'package:yoga_pose_app/pages/feedback_final_page.dart';
import '../resultado_pose.dart';
import 'package:yoga_pose_app/widgets/live_pose_detector_page.dart';
import 'package:yoga_pose_app/services/pose_service.dart';
import 'package:http/http.dart' as http;
import '../config.dart';
import 'dart:convert';

class AvaliacaoNivelPage extends StatefulWidget {
  final String nivel;

  const AvaliacaoNivelPage({Key? key, required this.nivel}) : super(key: key);

  @override
  State<AvaliacaoNivelPage> createState() => _AvaliacaoNivelPageState();
}

class _AvaliacaoNivelPageState extends State<AvaliacaoNivelPage> {
  List<String> poses = [];
  Map<String, double> precisoesPorPose = {};
  List<ResultadoPose> resultados = [];
  int indexAtual = 0;
  bool iniciou = false;

  @override
  void initState() {
    super.initState();
    carregarPosesDoNivel();
  }

  Future<void> carregarPosesDoNivel() async {
    try {
      final mapaBackend = {
        'Intermédio': 'intermedio',
        'Avançado': 'avancado',
        'Mestre': 'mestre',
        'Principiante': 'principiante',
      };
      final nivelApi = mapaBackend[widget.nivel] ?? widget.nivel.toLowerCase();

      final todas = await PoseService().getPosesPorNivel(nivelApi);

      todas.shuffle(Random());

      final limite = widget.nivel.toLowerCase() == 'mestre' ? 5 : 10;

      setState(() {
        poses = todas.take(limite).toList();
      });
    } catch (e) {
      print('Erro ao carregar poses: $e');
    }
  }

  void _guardarResultado(ResultadoPose resultado) {
    setState(() {
      iniciou = false;
      precisoesPorPose[resultado.nomePose] = resultado.precisao;
      resultados.add(resultado);
    });

    if (indexAtual + 1 < poses.length) {
      setState(() {
        indexAtual++;
      });
    } else {
      _irParaFeedbackFinal();
    }
  }

  Future<void> _irParaFeedbackFinal() async {
    final media = precisoesPorPose.values.fold(0.0, (a, b) => a + b) / precisoesPorPose.length;
    final passou = media >= 70.0;

    await PoseService().guardarHistoricoIndividual(resultados);
    await PoseService().guardarHistoricoParticipacao(
      widget.nivel,
      precisoesPorPose.values.toList(),
      precisoesPorPose.keys.toList(),
      passou,
      media,
    );

    if (passou) {
      await http.post(
        Uri.parse('${AppConfig.baseUrlBackend1}/atualizar_progresso'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'nivel': widget.nivel}),
      );
    }

    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (_) => FeedbackFinalPage(
          resultados: resultados,
          nivel: widget.nivel,
          mediaFinal: media,
          nomesPoses: precisoesPorPose.keys.toList(),
          precisoes: precisoesPorPose.values.toList(),
          passou: passou,
          onRepetir: () {
            setState(() {
              precisoesPorPose.clear();
              indexAtual = 0;
              carregarPosesDoNivel();
            });
          },
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (poses.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text('Avaliação ${widget.nivel}')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    final poseAtual = poses[indexAtual];

    return Scaffold(
      appBar: AppBar(title: Text('Avaliação ${widget.nivel}')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Pose ${indexAtual + 1} de ${poses.length}',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            Text(
              poseAtual,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 16),
            FutureBuilder<Map<String, dynamic>>(
              future: PoseService().obterImagemDaPose(poseAtual),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const CircularProgressIndicator();
                } else if (snapshot.hasError || !snapshot.hasData) {
                  return const Icon(Icons.image_not_supported);
                } else {
                  final data = snapshot.data!;
                  final pasta = data['pasta'];
                  final ficheiro = data['ficheiro'];
                  final imagemUrl = '${AppConfig.baseUrlBackend1}/images_test/$pasta/$ficheiro';

                  return Image.network(
                    imagemUrl,
                    height: 250,
                    errorBuilder: (context, error, stackTrace) => const Icon(Icons.image_not_supported),
                  );
                }
              },
            ),
            const SizedBox(height: 24),
            if (!iniciou)
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    iniciou = true;
                  });
                },
                child: const Text('Iniciar Avaliação'),
              )
            else
              Expanded(
                child: LivePoseDetectorPage(
                  poseEsperada: poseAtual,
                  onResultado: _guardarResultado,
                ),
              ),
          ],
        ),
      ),
    );
  }
}
