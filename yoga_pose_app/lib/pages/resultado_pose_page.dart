import 'package:flutter/material.dart';
import '../resultado_pose.dart';

class ResultadoPosePage extends StatelessWidget {
  final ResultadoPose resultado;
  final VoidCallback onNext;

  const ResultadoPosePage({
    Key? key,
    required this.resultado,
    required this.onNext,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final bool sucesso = resultado.precisao >= 90.0;
    final bool deveMostrarCorrecao = resultado.precisao < 90.0 && resultado.correcoes.isNotEmpty;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Resultado da Pose'),
        backgroundColor: Colors.indigo.shade700,
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.memory(resultado.imagem, height: 220),
              ),
              const SizedBox(height: 20),
              Text(
                sucesso ? 'Pose correta!' : 'Melhorias sugeridas:',
                style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w600),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 10),
              Text(
                'Avaliação: ${resultado.precisao.toStringAsFixed(1)}%',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: sucesso ? Colors.green : Colors.orange,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              if (deveMostrarCorrecao) ...[
                const Text(
                  'Correções recomendadas:',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                ...resultado.correcoes.map(
                      (c) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 2.0),
                    child: Text(
                      '- $c',
                      style: const TextStyle(fontSize: 14),
                    ),
                  ),
                ),
              ],
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: onNext,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.indigo.shade700,
                  padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                child: const Text(
                  'Próxima Pose',
                  style: TextStyle(fontSize: 16),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
