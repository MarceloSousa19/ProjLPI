import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';

class HistoricoPage extends StatefulWidget {
  const HistoricoPage({Key? key}) : super(key: key);

  @override
  State<HistoricoPage> createState() => _HistoricoPageState();
}

class _HistoricoPageState extends State<HistoricoPage> {
  late Future<List<Map<String, dynamic>>> _historico;

  @override
  void initState() {
    super.initState();
    _historico = _carregarHistorico();
  }

  Future<List<Map<String, dynamic>>> _carregarHistorico() async {
    final file = File('../shared_data/historico_participacoes.json');

    if (await file.exists()) {
      final content = await file.readAsString();
      final List<dynamic> jsonList = json.decode(content);
      return jsonList.cast<Map<String, dynamic>>();
    } else {
      return [];
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Histórico de Participações')),
      body: FutureBuilder<List<Map<String, dynamic>>> (
        future: _historico,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return const Center(child: Text('Erro ao carregar histórico.'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('Nenhum histórico encontrado.'));
          }

          final historico = snapshot.data!;
          return ListView.builder(
            itemCount: historico.length,
            itemBuilder: (context, index) {
              final item = historico[index];
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: ListTile(
                  title: Text("Nível: ${item['nivel']}"),
                  subtitle: Text("Data: ${item['data']} • Resultado: ${item['resultado_nivel']}"),
                  trailing: Text("Média: ${item['media_final']}%"),
                  onTap: () {
                    _mostrarDetalhes(context, item);
                  },
                ),
              );
            },
          );
        },
      ),
    );
  }

  void _mostrarDetalhes(BuildContext context, Map<String, dynamic> item) {
    final poses = List<Map<String, dynamic>>.from(item['poses']);

    showModalBottomSheet(
      context: context,
      builder: (context) => Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              "Detalhes da participação (${item['data']})",
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            ...poses.map((p) => ListTile(
              leading: Icon(
                p['sucesso'] == true ? Icons.check_circle : Icons.cancel,
                color: p['sucesso'] == true ? Colors.green : Colors.red,
              ),
              title: Text(p['nome']),
              trailing: Text("${p['precisao']}%"),
            ))
          ],
        ),
      ),
    );
  }
}
