import 'package:flutter/material.dart';
import 'package:vigango/core/utils/validators.dart';

class emailField extends StatelessWidget {
  const emailField({
    super.key,
    required TextEditingController emailController,
  }) : _emailController = emailController;

  final TextEditingController _emailController;

  @override
  Widget build(BuildContext context) {
    return TextFormField(
        controller: _emailController,
        decoration: InputDecoration(
          hintText: "you@example.com",
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(15),
          ),
        ),
        validator: (value) {
          return AppValidators.validateEmail(value);
        });
  }
}
