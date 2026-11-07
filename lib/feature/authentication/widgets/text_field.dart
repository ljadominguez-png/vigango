import 'package:flutter/material.dart';

class text_field extends StatelessWidget {
  final TextEditingController textController;
  final String hint;
  final String? Function(String?) validator;
  const text_field({
    super.key,
    required this.textController,
    required this.hint,
    required this.validator,
  });

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: textController,
      keyboardType: TextInputType.emailAddress,
      textInputAction: TextInputAction.done,
      decoration: InputDecoration(
        hintText: hint,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
        ),
      ),
      validator: validator,
    );
  }
}
