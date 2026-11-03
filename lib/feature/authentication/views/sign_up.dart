
import 'package:flutter/material.dart';
import 'package:lucide_icons_flutter/lucide_icons.dart';
import 'package:vigango/core/utils/validators.dart';
import 'package:vigango/core/widgets/buttons/noicon.dart';

class SignUp extends StatefulWidget {
  const SignUp({super.key});

  @override
  State<SignUp> createState() => _SignUpState();
}

class _SignUpState extends State<SignUp> {
  bool _obscureText = true;
  bool _obscureText2 = true;
  bool _hasAttempted = false;
  final _formKey = GlobalKey<FormState>();

  late final TextEditingController _emailController;
  late final TextEditingController _passwordController;
  late final TextEditingController _confirmPassword;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _emailController = TextEditingController();
    _passwordController = TextEditingController();
    _confirmPassword = TextEditingController();
  }

  @override
  void dispose() {
    // TODO: implement dispose
    super.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPassword.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => FocusScope.of(context).unfocus(),
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(
          parent: BouncingScrollPhysics(),
        ),
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Form(
            key: _formKey,
            autovalidateMode: _hasAttempted ? AutovalidateMode.onUserInteraction : AutovalidateMode.disabled, 
            child: Column(
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("Email"),
                    const SizedBox(height: 8),
                    TextFormField(
                      controller: _emailController,
                      decoration: InputDecoration(
                        hintText: "you@example.com",
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(15),
                        ),
                      ),
                      validator: (value) {
                        return AppValidators.validateEmail(value);
                      },
                    ),
                  ],
                ),
                const SizedBox(height: 18),
                const SizedBox(height: 18),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("Confirm Password"),
                    const SizedBox(height: 8),
                    TextFormField(
                      controller: _confirmPassword,
                      decoration: InputDecoration(
                        hintText: "Min 8 Characters",
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(15),
                        ),
                        suffixIcon: Padding(
                          padding: const EdgeInsets.only(right: 8.0),
                          child: IconButton(
                            onPressed: () {
                              setState(() {
                                _obscureText2 = !_obscureText2;
                              });
                            },
                            icon: Icon(
                              _obscureText2
                                  ? LucideIcons.eyeOff
                                  : LucideIcons.eye,
                            ),
                          ),
                        ),
                      ),
                      obscureText: _obscureText2,
                      validator: (value) { 
                        return AppValidators.validatePassword(value);
                      },
                    ),
                  ],
                ),

                const SizedBox(height: 36),

                NoIcon(
                  buttonLabel: 'Create Account',
                  enablebackground: true,
                  enableBorder: false,
                  enableBold: true,
                  onTap: () {
                    setState(() {
                      _hasAttempted = true;
                    });
                    if (_formKey.currentState!.validate()) {

                       print("Form is perfectly clean. Routing data...");
                    } else {
                      // If it returns false, Flutter automatically halts execution
                      // and lights up the red error states on the screen.
                      print("Validation failed. Halting network submission.");
                    }
                  },
                ),
                const SizedBox(height: 200),
              ],
            ),
          ),
        ),
      ),
    );
  }

  
}
