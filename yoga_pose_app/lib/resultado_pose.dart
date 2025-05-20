
import 'dart:typed_data';

class ResultadoPose {
  final String nomePose;
  final double precisao;
  final Uint8List imagem;
  final List<String> correcoes;

  ResultadoPose({
    required this.nomePose,
    required this.precisao,
    required this.imagem,
    required this.correcoes,
  });
}
