import 'dart:math';
import 'package:flutter/material.dart';
import 'package:yoga_pose_app/pages/feedback_final_page.dart';
import 'package:yoga_pose_app/widgets/live_pose_detector_page.dart';
import 'package:yoga_pose_app/services/pose_service.dart';

class AvaliacaoNivelPage extends StatefulWidget {
  final String nivel;

  const AvaliacaoNivelPage({Key? key, required this.nivel}) : super(key: key);

  @override
  State<AvaliacaoNivelPage> createState() => _AvaliacaoNivelPageState();
}

class _AvaliacaoNivelPageState extends State<AvaliacaoNivelPage> {
  List<String> poses = [];
  Map<String, double> precisoesPorPose = {};
  int indexAtual = 0;

  @override
  void initState() {
    super.initState();
    carregarPosesDoNivel();
  }

  Future<void> carregarPosesDoNivel() async {
    try {
      final todas = await PoseService().getPosesPorNivel(widget.nivel.toLowerCase());
      todas.shuffle(Random());

      final limite = widget.nivel.toLowerCase() == 'mestre' ? 5 : 10;

      setState(() {
        poses = todas.take(limite).toList();
      });
    } catch (e) {
      print('Erro ao carregar poses: $e');
    }
  }

  void _guardarResultado(String nomePose, double precisao) {
    setState(() {
      precisoesPorPose[nomePose] = precisao;
    });

    if (indexAtual + 1 < poses.length) {
      setState(() {
        indexAtual++;
      });
    } else {
      _irParaFeedbackFinal();
    }
  }

  void _irParaFeedbackFinal() {
    final media = precisoesPorPose.values.fold(0.0, (a, b) => a + b) / precisoesPorPose.length;
    final passou = media >= 70.0;

    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (_) => FeedbackFinalPage(
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

    return LivePoseDetectorPage(
      poseEsperada: poseAtual,
      onResultado: _guardarResultado,
    );
  }
}
