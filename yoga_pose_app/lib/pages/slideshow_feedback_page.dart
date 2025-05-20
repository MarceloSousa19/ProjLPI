
import 'package:flutter/material.dart';
import '../resultado_pose.dart';

class SlideshowFeedbackPage extends StatelessWidget {
  final List<ResultadoPose> resultados;

  const SlideshowFeedbackPage({Key? key, required this.resultados}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return PageView.builder(
      itemCount: resultados.length,
      itemBuilder: (context, index) {
        final r = resultados[index];
        return Scaffold(
          appBar: AppBar(title: Text(r.nomePose.replaceAll('_', ' '))),
          body: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                Image.memory(r.imagemBytes, height: 250),
                const SizedBox(height: 20),
                Text(
                  "Precisão: ${r.precisao.toStringAsFixed(1)}%",
                  style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 16),
                const Text(
                  "Correções sugeridas:",
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 8),
                ...r.correcoes.map((c) => Text("• $c")).toList(),
              ],
            ),
          ),
        );
      },
    );
  }
}
