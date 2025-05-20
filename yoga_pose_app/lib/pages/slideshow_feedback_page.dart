
import 'package:flutter/material.dart';
import '../resultado_pose.dart';

class SlideshowFeedbackPage extends StatelessWidget {
  final List<ResultadoPose> resultados;
  final String nivel;
  final double mediaFinal;
  final bool passou;
  final VoidCallback onRepetir;

  const SlideshowFeedbackPage({
    Key? key,
    required this.resultados,
    required this.nivel,
    required this.mediaFinal,
    required this.passou,
    required this.onRepetir,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Feedback Final - Nível $nivel')),
      body: Column(
        children: [
          Expanded(
            child: PageView.builder(
              itemCount: resultados.length,
              itemBuilder: (context, index) {
                final resultado = resultados[index];
                return Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    children: [
                      Text(
                        resultado.nomePose,
                        style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 12),
                      Expanded(
                        child: Image.memory(
                          resultado.imagem,
                          fit: BoxFit.contain,
                        ),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        'Precisão: ${resultado.precisao.toStringAsFixed(1)}%',
                        style: const TextStyle(fontSize: 18),
                      ),
                      const SizedBox(height: 8),
                      const Text('Correções:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      ...resultado.correcoes.map((c) => Text('- $c')).toList(),
                    ],
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 16.0),
            child: Column(
              children: [
                Text('Média final: ${mediaFinal.toStringAsFixed(1)}%', style: const TextStyle(fontSize: 18)),
                Text(passou ? '✅ Passaste o nível!' : '❌ Não passaste o nível', style: const TextStyle(fontSize: 18)),
                const SizedBox(height: 12),
                ElevatedButton(
                  onPressed: onRepetir,
                  child: const Text('Repetir nível'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
