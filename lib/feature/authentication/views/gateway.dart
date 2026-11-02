import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:vigango/core/widgets/buttons/buttons.dart';
import 'package:vigango/feature/authentication/views/center_screen.dart';
import 'package:vigango/feature/authentication/views/terms_of_service.dart';

class GateWay extends StatelessWidget {
  const GateWay({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
          child: Padding(
              padding:
                  const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
                  child: Column(
                    children: [
                      const Spacer(flex:1),
                      const Center(child: CenterScreen(),),
                      const Spacer(flex: 1),
                      Column(
                        children: [
                          Buttons(
                            buttonLabel: 'Continue with Google', 
                            enablebackground: true, 
                            enableBorder: true, 
                            enableBold: true, 
                            onTap: () => context.push('/welcomescreen')),
                          
                            const SizedBox(height: 20),
                          
                            Buttons(
                            buttonLabel: 'Continue with Email', 
                            enablebackground: false, 
                            enableBorder: true, 
                            enableBold: false, 
                            onTap: () => context.push('/authorization')),
                          
                            const SizedBox(height: 20),
                            TermsOfService(),
                        ],
                      ),
                    ],
                  ),)),
    );
  }
}
