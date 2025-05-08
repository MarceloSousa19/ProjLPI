import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'classificacoes_pessoais_page.dart';

class PerfilPage extends StatefulWidget {
  const PerfilPage({super.key});

  @override
  State<PerfilPage> createState() => _PerfilPageState();
}

class _PerfilPageState extends State<PerfilPage> {
  List<Map<String, dynamic>> recordes = [];
  bool desbloqueadoIntermedio = false;
  bool desbloqueadoAvancado = false;
  bool desbloqueadoMestre = false;
  File? imagemPerfil;

  @override
  void initState() {
    super.initState();
    carregarRecordes();
    carregarImagemPerfil();
  }

  void carregarImagemPerfil() async {
    final file = File('shared_data/foto_perfil.png');
    if (await file.exists()) {
      setState(() {
        imagemPerfil = file;
      });
    }
  }

  void escolherFoto() async {
    final picker = ImagePicker();
    final picked = await picker.pickImage(source: ImageSource.gallery);
    if (picked != null) {
      final file = File(picked.path);
      final destino = File('shared_data/foto_perfil.png');
      await destino.writeAsBytes(await file.readAsBytes());
      setState(() {
        imagemPerfil = destino;
      });
    }
  }

  void carregarRecordes() async {
    try {
      final file = File('shared_data/recordes_pessoais.json');
      if (await file.exists()) {
        final content = await file.readAsString();
        final data = json.decode(content);
        final lista = List<Map<String, dynamic>>.from(data);

        bool passouIntermedio = verificarPassouNivel(lista, _posesIntermedio);
        bool passouAvancado = verificarPassouNivel(lista, _posesAvancado);
        bool passouMestre = verificarPassouTodos90(lista);

        setState(() {
          recordes = lista;
          desbloqueadoIntermedio = passouIntermedio;
          desbloqueadoAvancado = passouIntermedio && passouAvancado;
          desbloqueadoMestre = passouMestre;
        });
      }
    } catch (e) {
      debugPrint('Erro ao carregar recordes: $e');
    }
  }

  bool verificarPassouNivel(List<Map<String, dynamic>> lista, List<String> posesNivel) {
    for (final pose in posesNivel) {
      final entry = lista.firstWhere((e) => e['nome_pose'] == pose, orElse: () => {});
      if (entry.isEmpty || (entry['precisao'] ?? 0) < 70) {
        return false;
      }
    }
    final media = posesNivel.map((p) {
      final entry = lista.firstWhere((e) => e['nome_pose'] == p, orElse: () => {});
      return (entry['precisao'] ?? 0).toDouble();
    }).reduce((a, b) => a + b) / posesNivel.length;
    return media >= 80;
  }

  bool verificarPassouTodos90(List<Map<String, dynamic>> lista) {
    final todasPoses = [..._posesPrincipiante, ..._posesIntermedio, ..._posesAvancado];
    for (final pose in todasPoses) {
      final entry = lista.firstWhere((e) => e['nome_pose'] == pose, orElse: () => {});
      if (entry.isEmpty || (entry['precisao'] ?? 0) < 90) {
        return false;
      }
    }
    return true;
  }

  static const List<String> _posesPrincipiante = [
    'Adho_Mukha_Svanasana', 'Balasana', 'Bitilasana', 'Marjaryasana', 'Padmasana',
    'Phalakasana', 'Setu_Bandha_Sarvangasana', 'Sivasana', 'Utkatasana', 'Vrksasana'
  ];

  static const List<String> _posesIntermedio = [
    'Camatkarasana', 'Dhanurasana', 'Eka_Pada_Rajakapotasana', 'Garudasana', 'Hanumanasana',
    'Navasana', 'Pincha_Mayurasana', 'Trikonasana', 'Ustrasana', 'Virabhadrasana_Three'
  ];

  static const List<String> _posesAvancado = [
    'Astavakrasana', 'Bakasana', 'Eka_Pada_Koundinyasana', 'Mayurasana', 'Padma_Mayurasana',
    'Parivrtta_Surya_Yantrasana', 'Tittibhasana', 'Urdhva_Dhanurasana', 'Visvamitrasana', 'Vrschikasana'
  ];

  String determinarNivelAtual() {
    if (desbloqueadoMestre) return 'Mestre';
    if (desbloqueadoAvancado) return 'Avançado';
    if (desbloqueadoIntermedio) return 'Intermédio';
    return 'Principiante';
  }

  @override
  Widget build(BuildContext context) {
    final nivelAtual = determinarNivelAtual();

    return Scaffold(
      appBar: AppBar(title: const Text('Perfil do Utilizador')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              GestureDetector(
                onTap: escolherFoto,
                child: CircleAvatar(
                  radius: 60,
                  backgroundImage: imagemPerfil != null ? FileImage(imagemPerfil!) : null,
                  child: imagemPerfil == null ? const Icon(Icons.person, size: 60) : null,
                ),
              ),
              const SizedBox(height: 16),
              const Text('👤 Nome: João Sousa', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              Text('📈 Nível Atual: $nivelAtual', style: const TextStyle(fontSize: 18)),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                icon: const Icon(Icons.bar_chart),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const ClassificacoesPessoaisPage()),
                  );
                },
                label: const Text('Classificações Pessoais'),
                style: ElevatedButton.styleFrom(minimumSize: const Size(double.infinity, 48)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
