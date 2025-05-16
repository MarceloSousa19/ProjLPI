import 'package:flutter/material.dart';
import 'avaliacao_nivel_page.dart';
/* import 'avaliacao_principiante.dart';
import 'avaliacao_intermedio.dart';
import 'avaliacao_avancado.dart';
import 'avaliacao_mestre.dart';
*/
class AvaliacaoPage extends StatefulWidget {
  const AvaliacaoPage({super.key});

  @override
  State<AvaliacaoPage> createState() => _AvaliacaoPageState();
}

class _AvaliacaoPageState extends State<AvaliacaoPage> {
  String nivelAtual = 'Principiante';
  bool desbloqueadoIntermedio = false;
  bool desbloqueadoAvancado = false;
  bool desbloqueadoMestre = false;

  /* void _navegarParaNivel(String nivel) {
    Widget page;
    switch (nivel) {
      case 'Principiante':
        page = const AvaliacaoPrincipiantePage();
        break;
      case 'Intermédio':
        page = const AvaliacaoIntermedioPage();
        break;
      case 'Avançado':
        page = const AvaliacaoAvancadoPage();
        break;
      case 'Mestre':
        page = const AvaliacaoMestrePage();
        break;
      default:
        return;
    }

    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => page),
    );
  }
*/

  void _navegarParaNivel(String nivel) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => AvaliacaoNivelPage(nivel: nivel),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Avaliação de Nível')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Escolha o seu nível de avaliação:',
              style: TextStyle(fontSize: 20),
            ),
            const SizedBox(height: 24),
            _buildBotaoNivel('Principiante', true),
            const SizedBox(height: 12),
            _buildBotaoNivel('Intermédio', desbloqueadoIntermedio),
            const SizedBox(height: 12),
            _buildBotaoNivel('Avançado', desbloqueadoAvancado),
            const SizedBox(height: 12),
            if (desbloqueadoMestre) _buildBotaoNivel('Mestre', true),
          ],
        ),
      ),
    );
  }

  Widget _buildBotaoNivel(String nome, bool ativo) {
    return ElevatedButton.icon(
      icon: ativo
          ? const Icon(Icons.fitness_center)
          : const Icon(Icons.lock_outline),
      onPressed: ativo ? () {
        setState(() {
          nivelAtual = nome;
        });
        _navegarParaNivel(nome);
      } : null,
      style: ElevatedButton.styleFrom(
        backgroundColor: ativo ? Colors.blue : Colors.grey,
        foregroundColor: Colors.white,
        minimumSize: const Size(double.infinity, 50),
      ),
      label: Text(nome),
    );
  }
}
