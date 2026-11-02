import 'package:go_router/go_router.dart';
import 'package:vigango/feature/authentication/views/authorization.dart';
import 'package:vigango/feature/authentication/views/forgot_password.dart';
import 'package:vigango/feature/authentication/views/gateway.dart';
import 'package:vigango/feature/authentication/views/log_in.dart';
import 'package:vigango/feature/authentication/views/sign_up.dart';
import 'package:vigango/feature/authentication/views/welcome_greeter.dart';

class AppRouter {
  // declaire the path here so that it wont cause any global typos
  static const String gateWay = '/';
  static const String authorization = '/authorization';
  static const String login = '/login';
  static const String signUp = '/signup';
  static const String forgot_password = '/forgotpassword';
  static const String welcome = '/welcomescreen';
  static const String home = '/home';

  static final GoRouter destinations = GoRouter(
    initialLocation: gateWay,
    //Auth
    /*redirect: (context, state){
      final bool isAuthenticated = false;
      final bool isLoggingIn = state.matchedLocation == login;
      if(!isAuthenticated){
        return gateWay;
      }
    },*/

    routes:[
      //root
      GoRoute(
        path: gateWay,
        builder:(context, state) => const GateWay(),
      ),
      GoRoute(
        path: authorization,
        builder: (context, state) => const Authorization(),
      ),
      // log in
      GoRoute(
        path: login,
        builder:(context, state) => const LogIn()
        ,),
      // sign up
      GoRoute(
        path: signUp,
        builder:(context, state) => const SignUp(),
        ),
      // forgot password
      GoRoute(
        path: forgot_password,
        builder: (context, state) => const ForgotPassword(),
        ),
      // Welcome Screen  
      GoRoute(
        path: welcome,
        builder:(context, state) => const WelcomeScreen(),
        ),
    ]
  );
}