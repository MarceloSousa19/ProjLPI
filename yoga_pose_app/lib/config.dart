import 'dart:io';
import 'package:flutter/foundation.dart';

class AppConfig {
  static const int portaBackend1 = 5001;
  static const int portaBackend2 = 5002;

  static String get baseIp {
    if (kIsWeb) return '172.20.10.2';

    if (Platform.isAndroid) {
      // emulador Android
      bool isProbablyEmulator = !Platform.environment.containsKey('ANDROID_STORAGE');
      return isProbablyEmulator ? '10.0.2.2' : '172.20.10.2';
    }

    if (Platform.isLinux || Platform.isWindows || Platform.isMacOS) {
      // Flutter desktop (como no teu caso)
      return '172.20.10.2';
    }

    // fallback seguro
    return '172.20.10.2';
  }

  static String get baseUrlBackend1 => 'http://$baseIp:$portaBackend1';
  static String get baseUrlBackend2 => 'http://$baseIp:$portaBackend2';
}
