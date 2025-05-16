import 'package:flutter/material.dart';
import 'pages/main_page.dart';
import 'dart:io';
import 'package:yoga_pose_app/pages/avaliacao_page.dart';

void main() {
// Permitir HTTP inseguro no desktop (para ver a foto dentro do flutter)
  HttpOverrides.global = MyHttpOverrides();
  runApp(const YogaPoseApp());
}
class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback = (X509Certificate cert, String host, int port) => true;
  }
}

class YogaPoseApp extends StatelessWidget {
  const YogaPoseApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: MainPage(),

    );
  }
}
