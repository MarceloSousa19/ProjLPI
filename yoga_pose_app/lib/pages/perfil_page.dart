import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:yoga_pose_app/config.dart';
import 'classificacoes_pessoais_page.dart';

class PerfilPage extends StatefulWidget {
  const PerfilPage({super.key});

  @override
  State<PerfilPage> createState() => _PerfilPageState();
}

class _PerfilPageState extends State<PerfilPage> {
  File? imagemPerfil;
  String nivelAtual = 'Principiante';
  List<String> concluidos = [];

  @override
  void initState() {
    super.initState();
    carregarImagemPerfil();
    carregarProgresso();
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
      final destino = File('../shared_data/foto_perfil.png');
      await destino.writeAsBytes(await file.readAsBytes());
      setState(() {
        imagemPerfil = destino;
      });
    }
  }

  void carregarProgresso() async {
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
          concluidos = List<String>.from(data['concluidos'] ?? []);
        });
      }
    } catch (e) {
      debugPrint('Erro ao carregar progresso: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
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
              const SizedBox(height: 12),
              const Text('Níveis Concluídos:', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              Wrap(
                spacing: 8,
                children: concluidos
                    .map((nivel) => Chip(label: Text(nivel)))
                    .toList(),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
