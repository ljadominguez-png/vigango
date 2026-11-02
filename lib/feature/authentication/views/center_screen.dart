import 'package:flutter/material.dart';

class CenterScreen extends StatelessWidget {
  const CenterScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final Color fontColor = Theme.of(context).colorScheme.onSurface;
    return Column(
      children: [
        Image.asset('assets/app_icon/ViganGo_icon.png', height: 100, width: 100),
        const SizedBox(height: 8),
        Text(
          'ViganGo',
          style: TextStyle(
            fontWeight: FontWeight.bold, fontSize: 25,
            color: fontColor),
        ),
        const SizedBox(height: 8),
        Text(
          'Local Activities and Tourism Discovery Platform for Vigan and Metro Vigan',
          textAlign: TextAlign.center,
          style: TextStyle(fontSize:18,
          color: fontColor),
        ),
      ],
    );
  }
}