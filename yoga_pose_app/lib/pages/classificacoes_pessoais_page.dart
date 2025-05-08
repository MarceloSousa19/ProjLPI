import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class ClassificacoesPessoaisPage extends StatefulWidget {
  const ClassificacoesPessoaisPage({super.key});

  @override
  State<ClassificacoesPessoaisPage> createState() => _ClassificacoesPessoaisPageState();
}

class _ClassificacoesPessoaisPageState extends State<ClassificacoesPessoaisPage> {
  List<Map<String, dynamic>> _classificacoes = [];

  @override
  void initState() {
    super.initState();
    _carregarClassificacoes();
  }

  Future<void> _carregarClassificacoes() async {
    try {
      final String jsonString = await rootBundle.loadString('shared_data/recordes_pessoais.json');
      final List<dynamic> dados = json.decode(jsonString);

      setState(() {
        _classificacoes = dados.cast<Map<String, dynamic>>();
      });
    } catch (e) {
      debugPrint('Erro ao carregar classificações: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Classificações Pessoais')),
      body: _classificacoes.isEmpty
          ? const Center(child: Text('Nenhuma classificação disponível.'))
          : ListView.builder(
        itemCount: _classificacoes.length,
        itemBuilder: (context, index) {
          final item = _classificacoes[index];
          return ListTile(
            leading: const Icon(Icons.check_circle_outline),
            title: Text(item['nomePose'].replaceAll('_', ' ')),
            trailing: Text('${item['precisao'].toStringAsFixed(1)}%'),
          );
        },
      ),
    );
  }
}
