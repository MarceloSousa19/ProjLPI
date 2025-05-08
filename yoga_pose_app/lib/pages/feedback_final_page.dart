import 'package:flutter/material.dart';

class FeedbackFinalPage extends StatelessWidget {
  final String nivel;
  final List<double> precisoes;
  final List<String> nomesPoses;
  final double mediaFinal;
  final bool passou;

  const FeedbackFinalPage({
    super.key,
    required this.nivel,
    required this.precisoes,
    required this.nomesPoses,
    required this.mediaFinal,
    required this.passou,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Feedback Final')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Nível: $nivel', style: const TextStyle(fontSize: 22)),
            Text('Resultado: ${passou ? "✅ Passou" : "❌ Falhou"}', style: const TextStyle(fontSize: 20)),
            Text('Média Final: ${mediaFinal.toStringAsFixed(2)}%', style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 20),
            const Text('Desempenho nas poses:', style: TextStyle(fontSize: 18)),
            const SizedBox(height: 10),
            Expanded(
              child: ListView.builder(
                itemCount: nomesPoses.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    leading: const Icon(Icons.fitness_center),
                    title: Text(nomesPoses[index].replaceAll('_', ' ')),
                    trailing: Text('${precisoes[index].toStringAsFixed(1)}%'),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
