import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:yoga_pose_app/config.dart';

class ClassificacoesPessoaisPage extends StatefulWidget {
  const ClassificacoesPessoaisPage({super.key});

  @override
  State<ClassificacoesPessoaisPage> createState() => _ClassificacoesPessoaisPageState();
}

class _ClassificacoesPessoaisPageState extends State<ClassificacoesPessoaisPage> {
  Map<String, dynamic> historico = {};
  Map<String, List<String>> posesPorNivel = {};
  bool carregando = true;

  @override
  void initState() {
    super.initState();
    carregarDados();
  }

  Future<void> carregarDados() async {
    try {
      final resHistorico = await http.get(Uri.parse('${AppConfig.baseUrlBackend1}/classificacao_pessoal'));
      final resPoses = await http.get(Uri.parse('${AppConfig.baseUrlBackend1}/poses_por_nivel'));

      if (resHistorico.statusCode == 200 && resPoses.statusCode == 200) {
        setState(() {
          historico = jsonDecode(resHistorico.body);
          final rawData = jsonDecode(resPoses.body) as Map<String, dynamic>;
          posesPorNivel = rawData.map((nivel, poses) {
            return MapEntry(nivel, List<String>.from(poses));
          });

          carregando = false;
        });
      } else {
        print("Erro ao carregar dados: ${resHistorico.statusCode} / ${resPoses.statusCode}");
        setState(() => carregando = false);
      }
    } catch (e) {
      print("Erro na requisição: $e");
      setState(() => carregando = false);
    }
  }

  double? obterMelhorPrecisao(String nomePose) {
    if (!historico.containsKey(nomePose)) return null;
    final tentativas = historico[nomePose]["tentativas"] as List<dynamic>;
    if (tentativas.isEmpty) return null;
    return tentativas.map((t) => t["precisao"] as num).reduce((a, b) => a > b ? a : b).toDouble();
  }

  double calcularMediaNivel(String nivel) {
    final poses = posesPorNivel[nivel] ?? [];
    final precisoes = poses
        .map(obterMelhorPrecisao)
        .where((p) => p != null)
        .cast<double>()
        .toList();

    if (precisoes.isEmpty) return 0.0;
    return precisoes.reduce((a, b) => a + b) / precisoes.length;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Classificações Pessoais'),
        backgroundColor: Colors.indigo.shade700,
      ),
      body: carregando
          ? const Center(child: CircularProgressIndicator())
          : ListView(
        padding: const EdgeInsets.all(16),
        children: posesPorNivel.entries
            .where((entry) {
          if (entry.key == 'Mestre') {
            try {
              final medias = ['Principiante', 'Intermedio', 'Avancado']
                  .map(calcularMediaNivel)
                  .toList();
              final mediaBase = medias.reduce((a, b) => a + b) / medias.length;
              return mediaBase >= 90.0;
            } catch (e) {
              return false;
            }
          }
          return true;
        })
            .map((entry) {
          final nivel = entry.key;
          final poses = entry.value;

          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Nível: $nivel',
                style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 8),
              ...poses.map((pose) {
                final precisao = obterMelhorPrecisao(pose);
                return Card(
                  elevation: 2,
                  margin: const EdgeInsets.symmetric(vertical: 4),
                  child: ListTile(
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    title: Text(
                      pose.replaceAll('_', ' '),
                      style: const TextStyle(fontSize: 16),
                    ),
                    trailing: Text(
                      precisao != null
                          ? '${precisao.toStringAsFixed(1)}%'
                          : 'Por realizar',
                      style: TextStyle(
                        fontSize: 14,
                        color: precisao != null ? Colors.green : Colors.grey,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                );
              }),
              const Divider(height: 32, thickness: 1.2),
            ],
          );
        })
            .toList(),
      ),
    );
  }
}
