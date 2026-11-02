import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:markdown_widget/markdown_widget.dart';

void showTermsOfServiceSheet(BuildContext context) {
  showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
          initialChildSize: 0.8,
          minChildSize: 0.5,
          maxChildSize: 0.95,
          expand: false,
          builder: (context, scrollController) {
            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Center(
                    child: const Text(
                      'Privacy Policy',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                  ),
                  const Divider(),
                  Expanded(
                    child: FutureBuilder<String>(
                      future: rootBundle.loadString('assets/legal/terms.md'), 
                      builder: (context, snapshot){
                        if (snapshot.connectionState == ConnectionState.waiting){
                          return const Center(child: CircularProgressIndicator());
                        }
                        if(snapshot.hasError){
                          return Center(
                            child: Text(
                              'Error loading terms: ${snapshot.error}',
                              style: const TextStyle( color: Colors.red),
                            )
                          );
                        }
                        return MarkdownWidget(
                          data:snapshot.data ?? '');
                      }) ),
                      Row(
                        children: [
                          ElevatedButton(onPressed: Navigator.of(context).pop, 
                          child: Text('I disagree')),
                          const Spacer(),
                          ElevatedButton(onPressed: Navigator.of(context).pop, 
                          child: Text('I agree')),
                        ],
                      )
                ],
              ),
            );
          }));
}
