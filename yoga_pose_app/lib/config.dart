import 'dart:io';
import 'package:flutter/foundation.dart';

class AppConfig {
  static const int portaBackend1 = 5001;
  static const int portaBackend2 = 5002;

  static String get baseIp {
    if (kIsWeb) return '192.168.1.77';

    if (Platform.isAndroid) {
      // emulador Android
      bool isProbablyEmulator = !Platform.environment.containsKey('ANDROID_STORAGE');
      return isProbablyEmulator ? '10.0.2.2' : '192.168.1.77';
    }

    if (Platform.isLinux || Platform.isWindows || Platform.isMacOS) {
      // Flutter desktop (como no teu caso)
      return '192.168.1.77';
    }

    // fallback seguro
    return '192.168.1.77';
  }

  static String get baseUrlBackend1 => 'http://$baseIp:$portaBackend1';
  static String get baseUrlBackend2 => 'http://$baseIp:$portaBackend2';
}
