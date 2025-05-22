import 'package:flutter/material.dart';
import '../resultado_pose.dart';

class SlideshowFeedbackPage extends StatefulWidget {
  final List<ResultadoPose> resultados;
  final String nivel;
  final double mediaFinal;
  final bool passou;
  final VoidCallback onRepetir;

  const SlideshowFeedbackPage({
    super.key,
    required this.resultados,
    required this.nivel,
    required this.mediaFinal,
    required this.passou,
    required this.onRepetir,
  });

  @override
  State<SlideshowFeedbackPage> createState() => _SlideshowFeedbackPageState();
}

class _SlideshowFeedbackPageState extends State<SlideshowFeedbackPage> {
  late PageController _pageController;
  int _paginaAtual = 0;

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
  }

  void _avancar() {
    if (_paginaAtual + 1 < widget.resultados.length) {
      _pageController.nextPage(duration: const Duration(milliseconds: 300), curve: Curves.easeIn);
    }
  }

  void _voltar() {
    if (_paginaAtual > 0) {
      _pageController.previousPage(duration: const Duration(milliseconds: 300), curve: Curves.easeIn);
    }
  }

  @override
  Widget build(BuildContext context) {
    final total = widget.resultados.length;

    return Scaffold(
      appBar: AppBar(
        title: Text('Feedback Visual - Nível ${widget.nivel}'),
      ),
      body: Column(
        children: [
          Expanded(
            child: PageView.builder(
              controller: _pageController,
              itemCount: total,
              onPageChanged: (index) {
                setState(() {
                  _paginaAtual = index;
                });
              },
              itemBuilder: (context, index) {
                final resultado = widget.resultados[index];
                final sucesso = resultado.precisao >= 70;

                return Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            sucesso ? Icons.check_circle : Icons.cancel,
                            color: sucesso ? Colors.green : Colors.red,
                            size: 28,
                          ),
                          const SizedBox(width: 8),
                          Text(
                            resultado.nomePose.replaceAll('_', ' '),
                            style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                      const SizedBox(height: 16),
                      Image.memory(resultado.imagem, height: 250),
                      const SizedBox(height: 16),
                      Text('Precisão: ${resultado.precisao.toStringAsFixed(1)}%'),
                      const SizedBox(height: 12),
                      if (resultado.correcoes.isNotEmpty) ...[
                        const Text('Sugestões de Correção:', style: TextStyle(fontWeight: FontWeight.bold)),
                        const SizedBox(height: 8),
                        ...resultado.correcoes.map((c) => Text('- $c')),
                      ],
                    ],
                  ),
                );
              },
            ),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              if (_paginaAtual > 0)
                ElevatedButton(
                  onPressed: _voltar,
                  child: const Text('Anterior'),
                ),
              if (_paginaAtual < total - 1)
                ElevatedButton(
                  onPressed: _avancar,
                  child: const Text('Seguinte'),
                ),
            ],
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }
}
