import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config.dart';

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

}
