
import 'package:flutter/foundation.dart';
import 'package:vigango/feature/authentication/models/user.dart';

@immutable
sealed class AuthState {
  const AuthState();
}

class AuthInitial extends AuthState{
  const AuthInitial();
}

class AuthLoading extends AuthState{
  const AuthLoading();
}

class AuthSuccess extends AuthState{
  final UserModel user;
  const AuthSuccess(this.user);
}