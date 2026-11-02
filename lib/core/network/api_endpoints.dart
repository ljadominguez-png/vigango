import 'package:flutter/foundation.dart';

class ApiEndpoints {
  static String get baseUrl {
    if (kIsWeb) return 'http://127.0.0.1:8000';
    // ANDROID ONLY
    return 'http://10.0.2.2:8000';
  }
  static String get register => '$baseUrl/api/v1/auth/register';
  static String get login => '$baseUrl/auth/login';
}