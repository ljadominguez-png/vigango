// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'package:flutter/material.dart';

class UsernameScreen extends StatefulWidget {
  final String email;
  final String password;
  const UsernameScreen({
    Key? key,
    required this.email,
    required this.password,
  }) : super(key: key);

  @override
  State<UsernameScreen> createState() => _UsernameScreenState();
}

class _UsernameScreenState extends State<UsernameScreen> {
  late final TextEditingController _usernameController;

  @override
  void initState() {
    // TODO: implement initState
    _usernameController = TextEditingController();
    super.initState();
  }

  @override
  void dispose() {
    // TODO: implement dispose
    _usernameController.dispose();
    super.dispose();
  }


  @override
  Widget build(BuildContext context) {
    return const Placeholder();
  }
}