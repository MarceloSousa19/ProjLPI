
import 'dart:typed_data';

class ResultadoPose {
  final String nomePose;
  final double precisao;
  final List<String> correcoes;
  final Uint8List imagemBytes;

  ResultadoPose({
    required this.nomePose,
    required this.precisao,
    required this.correcoes,
    required this.imagemBytes,
  });
}
