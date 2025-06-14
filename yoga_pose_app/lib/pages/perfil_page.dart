import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
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

  Future<File> _obterFicheiroPerfil() async {
    if (Platform.isAndroid || Platform.isIOS) {
      final dir = await getApplicationDocumentsDirectory();
      return File('${dir.path}/foto_perfil.png');
    } else {
      return File('../shared_data/foto_perfil.png');
    }
  }

  void carregarImagemPerfil() async {
    final file = await _obterFicheiroPerfil();
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
      final destino = await _obterFicheiroPerfil();
      await destino.writeAsBytes(await File(picked.path).readAsBytes());
      setState(() {
        imagemPerfil = destino;
      });
    }
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
      appBar: AppBar(
        title: const Text('Perfil do Utilizador'),
        backgroundColor: Colors.indigo.shade700,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            GestureDetector(
              onTap: escolherFoto,
              child: CircleAvatar(
                radius: 50,
                backgroundImage: imagemPerfil != null ? FileImage(imagemPerfil!) : null,
                child: imagemPerfil == null ? const Icon(Icons.person, size: 50) : null,
                backgroundColor: Colors.indigo,
              ),
            ),
            const SizedBox(height: 16),
            const Text(
              'Nome: João Sousa',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 8),
            Text(
              'Nível Atual: $nivelAtual',
              style: const TextStyle(fontSize: 16, fontStyle: FontStyle.italic),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                icon: const Icon(Icons.bar_chart),
                label: const Text('Classificações Pessoais'),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const ClassificacoesPessoaisPage()),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.indigo.shade100,
                  foregroundColor: Colors.indigo.shade900,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(24),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 30),
            const Align(
              alignment: Alignment.centerLeft,
              child: Text(
                'Níveis Concluídos:',
                style: TextStyle(fontSize: 16),
              ),
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              children: concluidos.map((nivel) => Chip(label: Text(nivel))).toList(),
            ),
          ],
        ),
      ),
    );
  }
}
