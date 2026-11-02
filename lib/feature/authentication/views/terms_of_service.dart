import 'package:flutter/material.dart';
import 'package:vigango/feature/authentication/widgets/terms_of_sevice_sheet.dart';

class TermsOfService extends StatefulWidget {
  const TermsOfService({super.key});

  @override
  State<TermsOfService> createState() => _TermsOfServiceState();
}

class _TermsOfServiceState extends State<TermsOfService> {
  bool _isAgreed = false;
  @override
  Widget build(BuildContext context) {
    final Color activeColor = Theme.of(context).colorScheme.inversePrimary;
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Checkbox(
          value: _isAgreed,
          activeColor: activeColor, 
          onChanged: (bool? newValue) {
            setState(() {
              _isAgreed = newValue ?? false; 
            });
          },
        ),
        Flexible(child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text("I agree to the "),
            InkWell(
              onTap: () => showTermsOfServiceSheet(context),
          child: Text("Privacy Policy",
          style: TextStyle(decoration: TextDecoration.underline),),
        ),
          ],
        )),
        
      ],
    );
  }
}