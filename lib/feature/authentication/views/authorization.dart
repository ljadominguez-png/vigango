//this serves as the 1. continue with google, and 2. continue with email

import 'package:flutter/material.dart';
import 'package:vigango/feature/authentication/views/log_in.dart';
import 'package:vigango/feature/authentication/views/sign_up.dart';
import 'package:vigango/feature/authentication/widgets/header.dart';

class Authorization extends StatefulWidget {
  const Authorization({super.key});

  @override
  State<Authorization> createState() => _AuthorizationState();
}

class _AuthorizationState extends State<Authorization> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  final List<Widget> _AuthorizationOptions = [LogIn(), SignUp()];

  @override
  void initState(){
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose(){
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final Color labelColor = Theme.of(context).colorScheme.inverseSurface;
    final Color unselected = Theme.of(context).colorScheme.outline;
    return Scaffold(
      resizeToAvoidBottomInset: false,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              Row(
                children: [
                  BackButton(),
                  Text('Back', style: TextStyle(fontSize: 18)),
                ],
              ),
              Header(),
              const SizedBox(height: 10),
              TabBar(
                controller: _tabController,
                onTap: (index) {
                  // When a native tab header is tapped, animate the PageView to match
                  _tabController.animateTo(
                    index,
                    duration: const Duration(milliseconds: 300),
                    curve: Curves.easeInOut,
                  );
                },
                // Styling parameters to try and strip down the Material bloat
                isScrollable: true,
                tabAlignment: TabAlignment.start,
                labelColor: labelColor, 
                unselectedLabelColor: unselected, 
                labelStyle: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
                indicatorColor: labelColor, 
                indicatorWeight: 2.0, 
                indicatorSize: TabBarIndicatorSize
                    .label, 
                dividerColor: Colors
                    .transparent, 
                tabs: const [
                  Tab(text: "Log In"),
                  Tab(text: "Sign Up"),
                ],
              ),
              const SizedBox(height: 20),
              Expanded(
                child: TabBarView(
                  controller: _tabController,
                  children: _AuthorizationOptions,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}