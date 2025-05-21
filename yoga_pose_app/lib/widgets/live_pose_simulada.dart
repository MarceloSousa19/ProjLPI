import 'dart:convert';
import 'dart:math';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:yoga_pose_app/config.dart';
import 'package:http/http.dart' as http;
import '../resultado_pose.dart';

class LivePoseDetectorSimuladaPage extends StatefulWidget {
  final String poseEsperada;
  final void Function(ResultadoPose resultado) onResultado;

  const LivePoseDetectorSimuladaPage({
    Key? key,
    required this.poseEsperada,
    required this.onResultado,
  }) : super(key: key);

  @override
  State<LivePoseDetectorSimuladaPage> createState() => _LivePoseDetectorSimuladaPageState();
}

class _LivePoseDetectorSimuladaPageState extends State<LivePoseDetectorSimuladaPage> {
  String? imagemUrl;

  @override
  void initState() {
    super.initState();
    _carregarImagemPose();
  }

  @override
  void didUpdateWidget(covariant LivePoseDetectorSimuladaPage oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.poseEsperada != widget.poseEsperada) {
      setState(() {
        imagemUrl = null;
      });
      _carregarImagemPose();
    }
  }

  Future<void> _carregarImagemPose() async {
    try {
      final res = await http.get(Uri.parse('${AppConfig.baseUrlBackend1}/imagem_pose/${widget.poseEsperada}'));
      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        final pasta = data['pasta'];
        final ficheiro = data['ficheiro'];

        final imagemFinalUrl = '${AppConfig.baseUrlBackend1}/images_test/$pasta/$ficheiro';
        final imagemRes = await http.get(Uri.parse(imagemFinalUrl));
        final imagemBytes = imagemRes.bodyBytes;

        setState(() {
          imagemUrl = imagemFinalUrl;
        });

        await Future.delayed(const Duration(seconds: 2));
        final random = Random();
        final conf = 70 + random.nextDouble() * 30;
        final List<String> correcoes = conf >= 90
            ? <String>[]
            : <String>["Ajusta a postura dos braços", "Inclina ligeiramente o tronco"];

        widget.onResultado(ResultadoPose(
          nomePose: widget.poseEsperada,
          precisao: conf,
          imagem: imagemBytes,
          correcoes: correcoes,
        ));
      }
    } catch (e) {
      print('Erro ao carregar imagem simulada: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: imagemUrl == null
          ? const Center(child: CircularProgressIndicator())
          : Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Image.network(imagemUrl!, height: 240),
          ),
          const Text(
            "A avaliar pose simulada...",
            style: TextStyle(fontSize: 18),
          ),
        ],
      ),
    );
  }
}
