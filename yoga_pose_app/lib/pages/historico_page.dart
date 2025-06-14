import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:yoga_pose_app/config.dart';
import 'package:path_provider/path_provider.dart';

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

  Future<File> _getHistoricoFile() async {
    final dir = await getApplicationDocumentsDirectory();
    return File('${dir.path}/historico_participacoes.json');
  }

  Future<List<Map<String, dynamic>>> _carregarHistorico() async {
    final url = Uri.parse('${AppConfig.baseUrlBackend1}/historico_participacoes');

    final res = await http.get(url);

    if (res.statusCode == 200) {
      final List<dynamic> jsonList = json.decode(res.body);
      return jsonList.cast<Map<String, dynamic>>();
    } else {
      throw Exception('Erro ao carregar histórico');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Histórico de Participações'),
        backgroundColor: Colors.indigo.shade700,
      ),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: _historico,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return const Center(child: Text('Erro ao carregar histórico.'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('Nenhum histórico encontrado.'));
          }

          final historico = snapshot.data!.reversed.toList();

          return ListView.builder(
            itemCount: historico.length,
            padding: const EdgeInsets.all(16),
            itemBuilder: (context, index) {
              final item = historico[index];
              final nivel = _normalizarNivel(item['nivel']);
              return Card(
                elevation: 4,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                margin: const EdgeInsets.symmetric(vertical: 10),
                child: ListTile(
                  contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                  title: Text(
                    "Nível: $nivel",
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                  ),
                  subtitle: Text(
                    "Data: ${item['data']} • Resultado: ${item['resultado_nivel']}",
                    style: const TextStyle(fontSize: 14),
                  ),
                  trailing: Text(
                    "Média: ${item['media_final']}%",
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  onTap: () => _mostrarDetalhes(context, item),
                ),
              );
            },
          );
        },
      ),
    );
  }

  String _normalizarNivel(String nivel) {
    const mapa = {
      "Principiante": "Principiante",
      "Intermedio": "Intermédio",
      "Avancado": "Avançado",
      "Mestre": "Mestre"
    };
    return mapa[nivel] ?? nivel;
  }

  void _mostrarDetalhes(BuildContext context, Map<String, dynamic> item) {
    final poses = List<Map<String, dynamic>>.from(item['poses']);

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
        expand: false,
        builder: (context, scrollController) => Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              Text(
                "Detalhes da participação (${item['data']})",
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              Expanded(
                child: ListView.builder(
                  controller: scrollController,
                  itemCount: poses.length,
                  itemBuilder: (context, index) {
                    final p = poses[index];
                    return ListTile(
                      leading: Icon(
                        p['sucesso'] == true ? Icons.check_circle : Icons.cancel,
                        color: p['sucesso'] == true ? Colors.green : Colors.red,
                      ),
                      title: Text(
                        p['nome'],
                        style: const TextStyle(fontSize: 15),
                      ),
                      trailing: Text(
                        "${p['precisao']}%",
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
