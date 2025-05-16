import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'dart:io' show Platform;
import 'live_pose_camera.dart';
import 'live_pose_simulada.dart';

class LivePoseDetectorPage extends StatelessWidget {
  final String poseEsperada;
  final void Function(String nomePose, double precisao) onResultado;

  const LivePoseDetectorPage({
    Key? key,
    required this.poseEsperada,
    required this.onResultado,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (kIsWeb || !(Platform.isAndroid || Platform.isIOS)) {
      return LivePoseDetectorSimuladaPage(
        poseEsperada: poseEsperada,
        onResultado: onResultado,
      );
    } else {
      return LivePoseDetectorCameraPage(
        poseEsperada: poseEsperada,
        onResultado: onResultado,
      );
    }
  }
}
