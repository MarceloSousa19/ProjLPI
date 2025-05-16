import 'package:flutter/material.dart';

class FeedbackFinalPage extends StatelessWidget {
  final String nivel;
  final double mediaFinal;
  final List<String> nomesPoses;
  final List<double> precisoes;
  final bool passou;
  final VoidCallback onRepetir;

  const FeedbackFinalPage({
    Key? key,
    required this.nivel,
    required this.mediaFinal,
    required this.nomesPoses,
    required this.precisoes,
    required this.passou,
    required this.onRepetir,
  }) : super(key: key);

  String _comentario(double precisao) {
    if (precisao >= 90) return "Excelente 👌";
    if (precisao >= 70) return "Bom 💪";
    return "Atenção ❗";
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Resultado - $nivel')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text(
              passou ? '✅ Passou o nível!' : '❌ Falhou o nível',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: passou ? Colors.green : Colors.red),
            ),
            const SizedBox(height: 16),
            Text(
              'Média final: ${mediaFinal.toStringAsFixed(1)}%',
              style: const TextStyle(fontSize: 20),
            ),
            const SizedBox(height: 24),
            Expanded(
              child: ListView.builder(
                itemCount: nomesPoses.length,
                itemBuilder: (context, index) {
                  final nome = nomesPoses[index];
                  final precisao = precisoes[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      title: Text(nome),
                      subtitle: Text('Precisão: ${precisao.toStringAsFixed(1)}%'),
                      trailing: Text(_comentario(precisao)),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              icon: Icon(passou ? Icons.home : Icons.refresh),
              label: Text(passou ? 'Voltar ao menu' : 'Tentar novamente'),
              style: ElevatedButton.styleFrom(
                backgroundColor: passou ? Colors.green : Colors.blue,
                minimumSize: const Size(double.infinity, 50),
              ),
              onPressed: () {
                if (passou) {
                  Navigator.popUntil(context, (route) => route.isFirst);
                } else {
                  onRepetir();
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}
