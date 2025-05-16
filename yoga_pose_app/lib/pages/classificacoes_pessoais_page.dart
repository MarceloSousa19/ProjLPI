import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:yoga_pose_app/config.dart';

class ClassificacoesPessoaisPage extends StatefulWidget {
  const ClassificacoesPessoaisPage({super.key});

  @override
  State<ClassificacoesPessoaisPage> createState() => _ClassificacoesPessoaisPageState();
}

class _ClassificacoesPessoaisPageState extends State<ClassificacoesPessoaisPage> {
  Map<String, dynamic> classificacoes = {};
  bool carregando = true;

  @override
  void initState() {
    super.initState();
    carregarClassificacoes();
  }

  Future<void> carregarClassificacoes() async {
    try {
      final res = await http.get(Uri.parse('${AppConfig.baseUrlBackend2}/classificacao_pessoal'));
      if (res.statusCode == 200) {
        setState(() {
          classificacoes = jsonDecode(res.body);
          carregando = false;
        });
      }
    } catch (e) {
      print("Erro ao buscar classificações: $e");
      setState(() => carregando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Classificações Pessoais')),
      body: carregando
          ? const Center(child: CircularProgressIndicator())
          : classificacoes.isEmpty
          ? const Center(child: Text("Nenhuma classificação encontrada"))
          : ListView(
        padding: const EdgeInsets.all(16),
        children: classificacoes.entries.map((entry) {
          final nivel = entry.key;
          final poses = entry.value as List<dynamic>;

          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '🧘 Nível: $nivel',
                style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              ...poses.map((p) => ListTile(
                title: Text(p['pose'].replaceAll('_', ' ')),
                trailing: Text(p['precisao'] != null
                    ? '${(p['precisao'] as double).toStringAsFixed(1)}%'
                    : '—'),
              )),
              const Divider(),
            ],
          );
        }).toList(),
      ),
    );
  }
}
