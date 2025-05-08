import 'package:flutter/material.dart';
import 'pages/main_page.dart';

void main() {
  runApp(const YogaPoseApp());
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
