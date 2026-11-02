import 'package:flutter/material.dart';

class NoIcon extends StatelessWidget {
  final String buttonLabel;
  final bool enableBold;
  final bool enablebackground;
  final bool enableBorder;
  final VoidCallback? onTap;

  const NoIcon({
    super.key,
    required this.buttonLabel, 
    required this.enablebackground,
    required this.enableBorder,
    required this.enableBold,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final Color coverBgColor = Theme.of(context).colorScheme.surface;
    final Color backgroundColor = Theme.of(context).colorScheme.primary;
    final Color foregroundColor = Theme.of(context).colorScheme.inversePrimary;


    return ElevatedButton(
      onPressed: onTap,
      style: ElevatedButton.styleFrom(
        backgroundColor: enablebackground ? backgroundColor : coverBgColor,
        foregroundColor: foregroundColor, 
        minimumSize: const Size.fromHeight(60), 
        side: enableBorder ? BorderSide(
          color: foregroundColor,
          width: 1.5,
        ) : null,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
        elevation: 0, 
      ),

      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        mainAxisSize: MainAxisSize.min, // Hug content tightly inside the centered space
        children: [
          Text(
            buttonLabel, 
            style: TextStyle(
              fontWeight: enableBold ? FontWeight.bold : null, 
              fontSize: 16,
            ),
          ), 
        ],
      ),
    );
  }
}