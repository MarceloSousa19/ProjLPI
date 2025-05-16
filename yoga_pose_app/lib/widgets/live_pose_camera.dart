import 'dart:convert';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image/image.dart' as img;
import 'package:yoga_pose_app/config.dart';

class LivePoseDetectorCameraPage extends StatefulWidget {
  final String poseEsperada;
  final void Function(String nomePose, double precisao) onResultado;

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
          imagemUrl = '${AppConfig.baseUrlBackend1}/images/$pasta/$ficheiro';
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

    _controller!.startImageStream((CameraImage image) async {
      if (_enviando) return;

      _enviando = true;
      final jpeg = await _converterYUVparaJPEG(image);
      if (jpeg == null) {
        _enviando = false;
        return;
      }

      await _enviarParaAPI(jpeg);
      _enviando = false;
    });
  }

  Future<List<int>?> _converterYUVparaJPEG(CameraImage image) async {
    try {
      final width = image.width;
      final height = image.height;
      final imgRGB = img.Image(width: width, height: height);
      final plane = image.planes[0];

      for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
          final pixelIndex = y * plane.bytesPerRow + x;
          final value = plane.bytes[pixelIndex];
          imgRGB.setPixelRgb(x, y, value, value, value);
        }
      }

      return img.encodeJpg(imgRGB);
    } catch (_) {
      return null;
    }
  }

  Future<void> _enviarParaAPI(List<int> jpeg) async {
    try {
      final uri = Uri.parse('${AppConfig.baseUrlBackend2}/classificar_pose');
      final req = http.MultipartRequest('POST', uri)
        ..files.add(http.MultipartFile.fromBytes('imagem', jpeg, filename: 'frame.jpg'));

      final res = await req.send();
      final resBody = await res.stream.bytesToString();

      if (res.statusCode == 200) {
        final data = jsonDecode(resBody);
        final poseDetectada = data['pose'];
        final conf = data['precisao'].toDouble();

        await _guardarTentativa(widget.poseEsperada, conf);

        if (poseDetectada == widget.poseEsperada) {
          setState(() {
            if (conf > _melhorConf) _melhorConf = conf;
          });

          if (conf >= 0.70) {
            await Future.delayed(const Duration(milliseconds: 500));
            _controller?.dispose();
            widget.onResultado(widget.poseEsperada, conf * 100);
          }
        }
      }
    } catch (e) {
      print('Erro API: $e');
    }
  }

  Future<void> _guardarTentativa(String pose, double conf) async {
    try {
      final uri = Uri.parse('${AppConfig.baseUrlBackend2}/guardar_tentativa');
      await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'pose': pose, 'precisao': conf}),
      );
    } catch (e) {
      print('Erro a guardar tentativa: $e');
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
          if (imagemUrl != null)
            Container(
              padding: const EdgeInsets.all(8),
              child: Image.network(
                imagemUrl!,
                height: 200,
                fit: BoxFit.contain,
              ),
            ),
          Expanded(
            child: CameraPreview(_controller!),
          ),
          const SizedBox(height: 8),
          Text(
            'Confiança para "${widget.poseEsperada.replaceAll('_', ' ')}": ${(_melhorConf * 100).toStringAsFixed(2)}%',
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }
}

