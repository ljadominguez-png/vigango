import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:vigango/feature/authentication/presenters/auth_state.dart';
import 'package:vigango/feature/authentication/repositories/auth_repository.dart';

class AuthCubit extends Cubit<AuthState>{
  final AuthRepository _repository;

  AuthCubit({AuthRepository? repository})
  : _repository = repository ?? AuthRepository(), super(const AuthInitial());

  Future<void> register({
    required String username,
    required String email,
    required String password,
  })async{
    emit(const AuthLoading());

    try {
      final user = await _repository.register
      (username: username, email: email, password: password);
      emit(AuthSuccess(user));
    } catch (e) {
      emit(AuthFailure(e.toString().replaceAll('Exception: ', '')));
    }
  }

  Future<void> signInWithGoogle({
    required String idToken,
  })async{
    emit(const AuthLoading());
    try{
      final user = await _repository.authenticateWithGoogle(id_token: idToken);
      emit(AuthSuccess(user));
    }catch (e) {
      emit(AuthFailure(e.toString().replaceAll('Exception: ', '')));
    }
  }

  void reset() => emit(const AuthInitial());
}