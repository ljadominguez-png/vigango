import 'package:flutter/material.dart';

class Buttons extends StatelessWidget {
  final String buttonLabel;
  final bool enableBold;
  final bool enablebackground;
  final bool enableBorder;
  final String? picturePath;
  final IconData? icon;
  final VoidCallback? onTap;

  const Buttons({super.key,
  required this.buttonLabel, 
  required this.enablebackground,
  required this.enableBorder,
  required this.enableBold,
  this.picturePath,
  this.icon,
  this.onTap});

  @override
  Widget build(BuildContext context) {
    final Color coverBgColor = Theme.of(context).colorScheme.surface;
    final Color backgroundColor = Theme.of(context).colorScheme.primary;
    final Color foregroundColor = Theme.of(context).colorScheme.inversePrimary;
    return ElevatedButton.icon(
  onPressed: onTap ,

  icon: picturePath != null  ? Image.asset(picturePath!, height: 30, width: 30) : Icon(icon),
  label:  Text(buttonLabel, style: TextStyle(fontWeight: enableBold ? FontWeight.bold : null, fontSize: 16),), 
  style: ElevatedButton.styleFrom(
    backgroundColor: enablebackground ? backgroundColor : coverBgColor,
    foregroundColor: foregroundColor, 
    minimumSize: const Size.fromHeight(60), 
    side: enableBorder ? BorderSide(
      color: foregroundColor,
      width: 1.5
    ) : null,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(16),
     
    ),
    elevation: 0, 
  ),
);
  }
}