import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:lucide_icons_flutter/lucide_icons.dart';
import 'package:vigango/core/utils/validators.dart';
import 'package:vigango/core/widgets/buttons/noicon.dart';

class LogIn extends StatefulWidget {
  const LogIn({super.key});

  @override
  State<LogIn> createState() => _LogInState();
}

class _LogInState extends State<LogIn> {
      final TextEditingController _passwordController = TextEditingController();
      bool _obscureText = true;
      bool _hasAttempted = false;
      final _formKey = GlobalKey<FormState>();


  @override
  void dispose() {
    // TODO: implement dispose
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Form(
        key: _formKey,
        //current issue, it auto validates as soon as the user clicks which is annoying
        autovalidateMode: _hasAttempted ? AutovalidateMode.onUserInteraction : AutovalidateMode.disabled,
        child: Column(
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text("Email"),
                const SizedBox(height: 8),
                TextFormField(
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
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text("Password"),
                const SizedBox(height: 8),
                TextFormField(
                  decoration: InputDecoration(
                    hintText: "Min 6 Characters",
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(15),
                    ),
                    suffixIcon: Padding(
                      padding: const EdgeInsets.only(right: 8.0),
                      child: IconButton(
                        onPressed: () {
                          setState(() {
                            _obscureText = !_obscureText;
                          });
                        },
                        icon: Icon(
                          _obscureText ? LucideIcons.eyeOff : LucideIcons.eye,
                        ),
                      ),
                    ),
                  ),
                  obscureText: _obscureText,
                  validator: (value){
                    return AppValidators.validatePassword(value);
                  }
                ),
              ],
            ),
            const SizedBox(height: 5),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                InkWell(
                  onTap: () => context.push('/forgotpassword'),
                  child: Text(
                    "Forgot Password",
                    style: TextStyle(decoration: TextDecoration.underline),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 36),

            NoIcon(
              buttonLabel: 'Log in',
              enablebackground: true,
              enableBorder: false,
              enableBold: true,
              onTap: () {
                setState(() {
                  _hasAttempted = true;
                });

                if (_formKey.currentState!.validate()) {
                  // If it returns true, EVERY field passed its rules perfectly!
                  // This is where you safely dispatch your event to your AuthBloc
                  context.push('/home');// not focusvoidscreen()
                } else {
                  // If it returns false, Flutter automatically halts execution
                  // and lights up the red error states on the screen.
                 
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}