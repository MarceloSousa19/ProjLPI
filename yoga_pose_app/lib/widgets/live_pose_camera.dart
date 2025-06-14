import 'dart:convert';
import 'dart:typed_data';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image/image.dart' as img;
import 'package:yoga_pose_app/config.dart';
import '../resultado_pose.dart';
import 'package:http_parser/http_parser.dart';
import 'dart:io';
import '../pages/resultado_pose_page.dart';

class LivePoseDetectorCameraPage extends StatefulWidget {
  final String poseEsperada;
  final void Function(ResultadoPose resultado) onResultado;

  const LivePoseDetectorCameraPage({
    Key? key,
    required this.poseEsperada,
    required this.onResultado,
  }) : super(key: key);

  @override
  State<LivePoseDetectorCameraPage> createState() => _LivePoseDetectorCameraPageState();
}

class _LivePoseDetectorCameraPageState extends State<LivePoseDetectorCameraPage> {
  CameraController? _controller;
  bool _enviando = false;
  DateTime? _ultimaCaptura;
  double _melhorConf = 0.0;
  String? imagemUrl;

  @override
  void initState() {
    super.initState();
    _carregarImagemPose();
    _iniciarCamera();
  }

  Future<void> _carregarImagemPose() async {
    try {
      final res = await http.get(Uri.parse('${AppConfig.baseUrlBackend1}/imagem_pose/${widget.poseEsperada}'));
      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        final pasta = data['pasta'];
        final ficheiro = data['ficheiro'];
        setState(() {
          imagemUrl = '${AppConfig.baseUrlBackend1}/images_test/$pasta/$ficheiro';
        });
      }
    } catch (e) {
      print('Erro a carregar imagem da pose: $e');
    }
  }

  Future<void> _iniciarCamera() async {
    final cameras = await availableCameras();
    final back = cameras.firstWhere((cam) => cam.lensDirection == CameraLensDirection.back);

    _controller = CameraController(back, ResolutionPreset.low, enableAudio: false);
    await _controller!.initialize();

    if (!mounted) return;
    setState(() {});

    await Future.delayed(Duration(seconds: 5));

    _controller!.startImageStream((CameraImage image) async {
      final agora = DateTime.now();

      if (_enviando || (_ultimaCaptura != null && agora.difference(_ultimaCaptura!) < Duration(seconds: 2))) return;

      _enviando = true;
      _ultimaCaptura = agora;

      final jpeg = await _converterYUVparaJPEG(image);
      if (jpeg != null) {
        final media = jpeg.reduce((a, b) => a + b) ~/ jpeg.length;
        if (media > 15) {
          await _enviarParaAPI(jpeg);
        } else {
          print("Ignorado: imagem escura ou vazia");
        }
      }

      _enviando = false;
    });
  }

  Future<List<int>?> _converterYUVparaJPEG(CameraImage image) async {
    try {
      final width = image.width;
      final height = image.height;

      final img.Image imgRGB = img.Image(width: width, height: height);
      final uvRowStride = image.planes[1].bytesPerRow;
      final uvPixelStride = image.planes[1].bytesPerPixel ?? 1;

      for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
          final int uvIndex = uvPixelStride * (x ~/ 2) + uvRowStride * (y ~/ 2);
          final int yValue = image.planes[0].bytes[y * image.planes[0].bytesPerRow + x];
          final int uValue = image.planes[1].bytes[uvIndex];
          final int vValue = image.planes[2].bytes[uvIndex];

          int r = (yValue + 1.370705 * (vValue - 128)).round();
          int g = (yValue - 0.337633 * (uValue - 128) - 0.698001 * (vValue - 128)).round();
          int b = (yValue + 1.732446 * (uValue - 128)).round();

          r = r.clamp(0, 255);
          g = g.clamp(0, 255);
          b = b.clamp(0, 255);

          imgRGB.setPixelRgb(x, y, r, g, b);
        }
      }

      final rotated = img.copyRotate(imgRGB, angle: 90);
      return img.encodeJpg(rotated);
    } catch (e) {
      print('Erro ao converter YUV para RGB: $e');
      return null;
    }
  }

  Future<void> _enviarParaAPI(List<int> jpeg) async {
    try {
      final file = File('/storage/emulated/0/Download/frame_debug.jpg');
      await file.writeAsBytes(jpeg);
      print('🧪 Frame salvo localmente: ${file.path}');

      final uri = Uri.parse('${AppConfig.baseUrlBackend2}/classificar_pose');
      final req = http.MultipartRequest('POST', uri)
        ..files.add(http.MultipartFile.fromBytes(
          'imagem',
          jpeg,
          filename: 'frame.jpg',
          contentType: MediaType('image', 'jpeg'),
        ));

      final res = await req.send();
      final resBody = await res.stream.bytesToString();

      if (res.statusCode == 200) {
        final data = jsonDecode(resBody);

        if (data.containsKey('erro')) {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(data['erro']),
                duration: Duration(seconds: 2),
                backgroundColor: Colors.red,
              ),
            );
          }
          return;
        }

        final poseDetectada = data['pose'];
        final conf = data['precisao'].toDouble();
        final List<String> correcoes = List<String>.from(data['correcoes']);

        final imagemCapturada = Uint8List.fromList(jpeg);
        final resultado = ResultadoPose(
          nomePose: widget.poseEsperada,
          precisao: conf,
          imagem: imagemCapturada,
          correcoes: correcoes,
        );

        _controller?.dispose();

        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ResultadoPosePage(
              resultado: resultado,
              onNext: () {
                Navigator.pop(context);
                widget.onResultado(resultado);
              },
            ),
          ),
        );
      }
    } catch (e) {
      print('Erro API: $e');
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_controller == null || !_controller!.value.isInitialized) {
      return const Center(child: CircularProgressIndicator());
    }

    return Scaffold(
      backgroundColor: Colors.white,
      body: Column(
        children: [
          Expanded(
            child: Center(
              child: AspectRatio(
                aspectRatio: _controller!.value.aspectRatio,
                child: CameraPreview(_controller!),
              ),
            ),
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }
}
