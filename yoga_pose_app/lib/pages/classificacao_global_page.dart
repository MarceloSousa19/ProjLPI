import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';

class ClassificacaoGlobalPage extends StatefulWidget {
  const ClassificacaoGlobalPage({super.key});

  @override
  State<ClassificacaoGlobalPage> createState() => _ClassificacaoGlobalPageState();
}

class _ClassificacaoGlobalPageState extends State<ClassificacaoGlobalPage> {
  List<Map<String, dynamic>> individuais = [];
  List<Map<String, dynamic>> grupos = [];

  @override
  void initState() {
    super.initState();
    carregarClassificacoes();
  }

  void carregarClassificacoes() async {
    try {
      final fileInd = File('shared_data/classificacao_individual.json');
      final fileGrp = File('shared_data/classificacao_grupos.json');

      if (await fileInd.exists()) {
        final data = json.decode(await fileInd.readAsString());
        final lista = List<Map<String, dynamic>>.from(data);
        lista.sort((a, b) => (b['pontuacao'] ?? 0).compareTo(a['pontuacao'] ?? 0));
        setState(() {
          individuais = lista;
        });
      }

      if (await fileGrp.exists()) {
        final data = json.decode(await fileGrp.readAsString());
        final lista = List<Map<String, dynamic>>.from(data);
        lista.sort((a, b) => (b['pontuacao'] ?? 0).compareTo(a['pontuacao'] ?? 0));
        setState(() {
          grupos = lista;
        });
      }
    } catch (e) {
      debugPrint('Erro ao carregar classificações: $e');
    }
  }

  Widget _buildTabela(String titulo, List<Map<String, dynamic>> dados) {
    return Expanded(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(titulo, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          ...List.generate(dados.take(10).length, (i) {
            final e = dados[i];
            final nome = e['nome'];
            final pontuacao = e['pontuacao'];
            final temMedalha = e['medalha'] == true;

            return ListTile(
              leading: Text("${i + 1}.", style: const TextStyle(fontSize: 18)),
              title: Text(nome, style: const TextStyle(fontSize: 18)),
              trailing: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  if (temMedalha) const Icon(Icons.emoji_events, color: Colors.amber),
                  const SizedBox(width: 6),
                  Text("$pontuacao poses", style: const TextStyle(fontSize: 16)),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🏅 Classificação Global')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildTabela("Top Jogadores", individuais),
            const SizedBox(width: 24),
            _buildTabela("Top Grupos", grupos),
          ],
        ),
      ),
    );
  }
}
