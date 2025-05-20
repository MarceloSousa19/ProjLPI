
import 'package:flutter/material.dart';
import '../resultado_pose.dart';
import 'slideshow_feedback_page.dart';

class FeedbackFinalPage extends StatelessWidget {
  final List<ResultadoPose> resultados;
  final String nivel;
  final double mediaFinal;
  final List<String> nomesPoses;
  final List<double> precisoes;
  final bool passou;
  final VoidCallback onRepetir;

  const FeedbackFinalPage({
    Key? key,
    required this.resultados,
    required this.nivel,
    required this.mediaFinal,
    required this.nomesPoses,
    required this.precisoes,
    required this.passou,
    required this.onRepetir,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Resultado Final - Nível $nivel'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Text(
              passou ? '✅ Parabéns! Passaste o nível!' : '❌ Não passaste o nível',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            Text(
              'Média final: ${mediaFinal.toStringAsFixed(1)}%',
              style: const TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 24),
            Expanded(
              child: ListView.builder(
                itemCount: nomesPoses.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(nomesPoses[index]),
                    trailing: Text('${precisoes[index].toStringAsFixed(1)}%'),
                  );
                },
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => SlideshowFeedbackPage(
                      resultados: resultados,
                      nivel: nivel,
                      mediaFinal: mediaFinal,
                      passou: passou,
                      onRepetir: onRepetir,
                    ),
                  ),
                );
              },
              child: const Text('Ver Feedback Visual'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: onRepetir,
              child: const Text('Repetir Nível'),
            ),
          ],
        ),
      ),
    );
  }
}
