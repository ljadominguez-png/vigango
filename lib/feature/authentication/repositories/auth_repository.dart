import 'dart:convert';

import 'package:vigango/core/network/api_endpoints.dart';
import 'package:vigango/feature/authentication/models/user.dart';
import 'package:http/http.dart' as http;

class AuthRepository {

  // for user sign up
  Future<UserModel> register({
    required String username,
    required String email,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse(ApiEndpoints.register),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: jsonEncode({
        'username' : username.trim(),
        'email': email.trim(),
        'password': password,
      }),
    );
    if (response.statusCode == 200 || response.statusCode == 201) {
      final Map<String, dynamic> data = jsonDecode(response.body);
      return UserModel.fromJson(data);
    } else {
      final errorData = jsonDecode(response.body);
      final message = errorData is Map && errorData.containsKey('detail')
          ? errorData['detail']
          : 'Registration failed (${response.statusCode})';
      throw Exception(message);
    }
  }

  //for user log in
  Future<UserModel> LogIn({
    required String email,
    required String password,
  })async{
    final response = await http.post(
      Uri.parse(ApiEndpoints.login),
      headers: {'Content-Type' : 'application/json'},
      body: jsonEncode({
        'email' : email.trim(),
        'password' : password
      }),
    );

    if(response.statusCode == 200){
      return UserModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Invalid Credentials');
    }
  }
  //for user google sign in
  Future<UserModel> authenticateWithGoogle({
    required String id_token,
  })async{
    final response = await http.post(
      Uri.parse(ApiEndpoints.googleAuth),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'id_token' : id_token}),
    );
    if (response.statusCode == 200){
      return UserModel.fromJson(jsonDecode(response.body));
    }else {
      throw Exception('Unsupported format');
    }
  }
 }
