// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:vigango/core/routers/app_router.dart';
import 'package:vigango/core/utils/sanitizers.dart';
import 'package:vigango/core/utils/validators.dart';
import 'package:vigango/core/widgets/buttons/noicon.dart';
import 'package:vigango/feature/authentication/models/registerrequest.dart';
import 'package:vigango/feature/authentication/widgets/text_field.dart';

class UsernameScreen extends StatefulWidget {
  final Registerrequest registerData;
  const UsernameScreen({
    Key? key,
    required this.registerData,
  }) : super(key: key);

  @override
  State<UsernameScreen> createState() => _UsernameScreenState();
}

class _UsernameScreenState extends State<UsernameScreen> {
  final _formkey = GlobalKey<FormState>();
  late final TextEditingController _usernameController;
  bool _isloading = false;
  bool _accCreated = false;

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

  void _submit() async {
    String sanitizedUsername = AppSanitizer.username(_usernameController.text);

    //stop immediately
    if (!_formkey.currentState!.validate()) return;

    //if none then submit the user's new acc

    //wait till userprof is uploaded
    setState(() => _isloading = true);

    //if done proceed to greeter
    context.go(AppRouter.welcome);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: SafeArea(
          child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
        child: _usernameView(),
      )),
    );
  }

  Widget _usernameView() {
    return Form(
        key: _formkey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            //username field
            Text('Enter your Username'),
            const SizedBox(height: 8),
            text_field(
                textController: _usernameController,
                hint: 'User67',
                validator: (value) => AppValidators.validateUsername(value)),
            const SizedBox(height: 33),
            //button for submission
            NoIcon(
                buttonLabel: 'Create Account',
                enablebackground: true,
                enableBorder: true,
                enableBold: true,
                onTap: _submit)
          ],
        ));
  }
}
