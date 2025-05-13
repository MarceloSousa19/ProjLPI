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
        setState(() {
          individuais = List<Map<String, dynamic>>.from(data);
          individuais.sort((a, b) => (b['pontuacao'] ?? 0).compareTo(a['pontuacao'] ?? 0));
        });
        print('📁 Individuais carregados: ${individuais.length}');
      }
      if (await fileGrp.exists()) {
        final data = json.decode(await fileGrp.readAsString());
        setState(() {
          grupos = List<Map<String, dynamic>>.from(data);
          grupos.sort((a, b) => (b['pontuacao'] ?? 0).compareTo(a['pontuacao'] ?? 0));
        });
        print('📁 Grupos carregados: ${grupos.length}');
      }
    } catch (e) {
      debugPrint('Erro ao carregar classificações: $e');
    }
  }

  Widget _buildTabela(String titulo, List<Map<String, dynamic>> dados, {bool grupo = false}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(titulo, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        const SizedBox(height: 10),
        ...List.generate(dados.take(10).length, (i) {
          final e = dados[i];
          final nome = e['nome'] ?? 'Desconhecido';
          final pontuacao = e['pontuacao'] ?? 0;
          final temMedalha = e['medalha'] == true;

          return ListTile(
            dense: true,
            leading: Text("${i + 1}.", style: const TextStyle(fontSize: 16)),
            title: Text(nome, style: const TextStyle(fontSize: 16)),
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                if (temMedalha) const Icon(Icons.emoji_events, color: Colors.amber),
                const SizedBox(width: 6),
                Text("$pontuacao poses", style: const TextStyle(fontSize: 14)),
              ],
            ),
          );
        }),
      ],
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
            Expanded(child: _buildTabela("Top Jogadores", individuais)),
            const SizedBox(width: 20),
            Expanded(child: _buildTabela("Top Grupos", grupos, grupo: true)),
          ],
        ),
      ),
    );
  }
}
