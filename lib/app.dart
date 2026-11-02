
import 'package:flutter/material.dart';
import 'package:vigango/core/routers/app_router.dart';

class ViganGo extends StatelessWidget{
  const ViganGo({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: "ViganGo",
      debugShowCheckedModeBanner: false,
      //home: AuthWrapper(),
      routerConfig: AppRouter.destinations,
    );
  }
  
}