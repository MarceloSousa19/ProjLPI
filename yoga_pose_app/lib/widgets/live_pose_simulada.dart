import 'dart:math';
import 'package:flutter/material.dart';
import 'package:yoga_pose_app/config.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class LivePoseDetectorSimuladaPage extends StatefulWidget {
  final String poseEsperada;
  final void Function(String nomePose, double precisao) onResultado;

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
      print('→ A carregar imagem da pose: ${widget.poseEsperada}');
      final res = await http.get(Uri.parse('${AppConfig.baseUrlBackend1}/imagem_pose/${widget.poseEsperada}'));

      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        final pasta = data['pasta'];
        final ficheiro = data['ficheiro'];
        final url = '${AppConfig.baseUrlBackend1}/images_test/$pasta/$ficheiro';

        print('→ URL da imagem (simulada): $url');
        setState(() {
          imagemUrl = url;
        });
      } else {
        print('→ Erro HTTP ao obter imagem: ${res.statusCode}');
      }
    } catch (e) {
      print('→ Erro ao carregar imagem da pose simulada: $e');
    }
  }

  void _simularAvaliacao() {
    final double precisaoSimulada = 60 + Random().nextDouble() * 40; // 60% a 100%
    widget.onResultado(widget.poseEsperada, precisaoSimulada);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Avaliação (Simulada)')),
      body: Column(
        children: [
          // Nome da pose no topo
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Text(
              widget.poseEsperada.replaceAll('_', ' '),
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
          ),

          // Imagem ou erro
          if (imagemUrl != null)
            Padding(
              padding: const EdgeInsets.all(16),
              child: Image.network(
                imagemUrl!,
                height: 250,
                fit: BoxFit.contain,
                errorBuilder: (context, error, stackTrace) {
                  print('❌ Erro ao carregar imagem: $error');
                  return const Text('Erro ao carregar imagem ❌');
                },
              ),
            )
          else
            const Padding(
              padding: EdgeInsets.all(16),
              child: CircularProgressIndicator(),
            ),

          const Spacer(),

          // Botão simulado
          ElevatedButton.icon(
            icon: const Icon(Icons.play_arrow),
            label: const Text("Iniciar Avaliação"),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size(double.infinity, 60),
              textStyle: const TextStyle(fontSize: 18),
            ),
            onPressed: _simularAvaliacao,
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }
}
