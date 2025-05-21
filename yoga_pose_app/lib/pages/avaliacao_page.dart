import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:yoga_pose_app/config.dart';
import 'avaliacao_nivel_page.dart';

class AvaliacaoPage extends StatefulWidget {
  const AvaliacaoPage({super.key});

  @override
  State<AvaliacaoPage> createState() => _AvaliacaoPageState();
}

class _AvaliacaoPageState extends State<AvaliacaoPage> {
  String nivelAtual = 'Principiante';
  List<String> desbloqueados = ['Principiante'];

  @override
  void initState() {
    super.initState();
    carregarProgresso();
  }

  Future<void> carregarProgresso() async {
    try {
      final res = await http.get(Uri.parse('${AppConfig.baseUrlBackend1}/progresso'));
      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        final raw = data['nivel_maximo_desbloqueado'] ?? 'Principiante';
        final mapaNomes = {
          'Principiante': 'Principiante',
          'Intermedio': 'Intermédio',
          'Avancado': 'Avançado',
          'Mestre': 'Mestre',
        };
        final convertido = mapaNomes[raw] ?? raw;
        setState(() {
          nivelAtual = convertido;
          desbloqueados = _calcularDesbloqueados(convertido);
        });
      }
    } catch (e) {
      print('Erro ao carregar progresso: $e');
    }
  }

  List<String> _calcularDesbloqueados(String nivelAtual) {
    const ordem = ['Principiante', 'Intermédio', 'Avançado', 'Mestre'];
    final index = ordem.indexOf(nivelAtual);
    return ordem.sublist(0, index + 1);
  }

  void _navegarParaNivel(String nivel) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => AvaliacaoNivelPage(nivel: nivel),
      ),
    );
  }

  Widget _buildBotaoNivel(String nome, bool ativo) {
    return ElevatedButton.icon(
      icon: ativo ? const Icon(Icons.fitness_center) : const Icon(Icons.lock_outline),
      onPressed: ativo ? () {
        setState(() {
          nivelAtual = nome;
        });
        _navegarParaNivel(nome);
      } : null,
      style: ElevatedButton.styleFrom(
        backgroundColor: ativo ? Colors.blue : Colors.grey,
        foregroundColor: Colors.white,
        minimumSize: const Size(double.infinity, 50),
      ),
      label: Text(nome),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Avaliação de Nível')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Escolha o seu nível de avaliação:',
              style: TextStyle(fontSize: 20),
            ),
            const SizedBox(height: 24),
            _buildBotaoNivel('Principiante', desbloqueados.contains('Principiante')),
            const SizedBox(height: 12),
            _buildBotaoNivel('Intermédio', desbloqueados.contains('Intermédio')),
            const SizedBox(height: 12),
            _buildBotaoNivel('Avançado', desbloqueados.contains('Avançado')),
            const SizedBox(height: 12),
            if (desbloqueados.contains('Mestre'))
              _buildBotaoNivel('Mestre', true),
          ],
        ),
      ),
    );
  }
}
