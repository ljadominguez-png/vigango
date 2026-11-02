import 'package:flutter/material.dart';

class Header extends StatelessWidget {
  const Header({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Image.asset('assets/app_icon/ViganGo_icon.png', height: 80, width: 80,),
        const SizedBox(height: 10),
        Text('ViganGo', style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold),),
        const SizedBox(height: 10),
        Text('Welcome back!', style: TextStyle(fontSize: 18),)
      ],
    );
  }
}