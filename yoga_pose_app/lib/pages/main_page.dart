import 'package:flutter/material.dart';
import 'package:yoga_pose_app/pages/avaliacao_page.dart';
import 'package:yoga_pose_app/pages/perfil_page.dart';
import 'package:yoga_pose_app/pages/historico_page.dart';
import 'package:yoga_pose_app/pages/classificacao_global_page.dart';

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _indiceAtual = 0;
  final List<Widget> _paginas = const [
    PerfilPage(),
    AvaliacaoPage(),
    HistoricoPage(),
    ClassificacaoGlobalPage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _paginas[_indiceAtual],
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: Colors.black,
        selectedItemColor: Colors.white,
        unselectedItemColor: Colors.grey,
        currentIndex: _indiceAtual,
        onTap: (index) => setState(() => _indiceAtual = index),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Perfil'),
          BottomNavigationBarItem(icon: Icon(Icons.fitness_center), label: 'Avaliação'),
          BottomNavigationBarItem(icon: Icon(Icons.history), label: 'Histórico'),
          BottomNavigationBarItem(icon: Icon(Icons.leaderboard), label: 'Ranking'),
        ],
      ),
    );
  }
}
