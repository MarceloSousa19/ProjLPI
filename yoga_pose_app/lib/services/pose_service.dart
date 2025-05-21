import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config.dart';
import 'package:yoga_pose_app/resultado_pose.dart';

class PoseService {
  Future<List<String>> getPosesPorNivel(String nivel) async {
    final url = Uri.parse('${AppConfig.baseUrlBackend1}/poses_por_nivel');

    final response = await http.get(url);
    if (response.statusCode == 200) {
      final data = json.decode(response.body);

      // Corrigir para usar a chave com a primeira letra maiúscula
      final chaveNivel = nivel[0].toUpperCase() + nivel.substring(1).toLowerCase();

      if (data is Map<String, dynamic> && data.containsKey(chaveNivel)) {
        final lista = data[chaveNivel];
        if (lista is List) {
          return List<String>.from(lista);
        }
      }

      throw Exception('Nível "$chaveNivel" não encontrado na resposta.');
    } else {
      throw Exception('Erro ao carregar poses do backend');
    }
  }
  Future<Map<String, dynamic>> obterImagemDaPose(String nomePose) async {
    final res = await http.get(Uri.parse('${AppConfig.baseUrlBackend1}/imagem_pose/$nomePose'));


    if (res.statusCode == 200) {
      return jsonDecode(res.body);
    } else {
      throw Exception('Falha ao obter imagem da pose');
    }
  }

  Future<void> guardarHistoricoIndividual(List<ResultadoPose> resultados) async {
    for (var resultado in resultados) {
      await http.post(
        Uri.parse('${AppConfig.baseUrlBackend1}/guardar_historico_individual'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'nome_pose': resultado.nomePose,
          'precisao': resultado.precisao,
        }),
      );
    }
  }

  Future<void> guardarHistoricoParticipacao(
      String nivel,
      List<double> precisoes,
      List<String> nomes,
      bool passou,
      double media,
      ) async {
    await http.post(
      Uri.parse('${AppConfig.baseUrlBackend1}/guardar_historico_participacao'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'nivel': nivel,
        'precisoes_poses': precisoes,
        'nomes_poses': nomes,
        'passou': passou,
        'media_final': media,
      }),
    );
  }


}
