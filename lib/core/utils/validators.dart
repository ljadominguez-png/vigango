class AppValidators {
  static String? validateEmail(String? value) {
    if (value == null || value.trim().isEmpty) {
      return 'Email Address is Required';
    }
    //In ASCII/standard regex engines, \w is shorthand for [a-zA-Z0-9_]
    final validEmail = RegExp(r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,}$');
    if (!validEmail.hasMatch(value.trim())) {
      return 'Please enter a valid email';
    }
    return null;
  }

  static String? validateUsername(String? value) {
    if (value == null || value.trim().isEmpty) {
      return 'Username required';
    }
    final validUsername = RegExp(r'^[\w]{3,16}$');
    if (!validUsername.hasMatch(value.trim())) {
      return 'please enter a valid username';
    }
    return null;
  }

  static String? validateField(String? value, String fieldname) {
    if (value == null || value.trim().isEmpty) {
      return '$fieldname cannot be empty!';
    }
    return null;
  }

  static String? validatePassword(String? value) {
    if (value == null || value.trim().isEmpty) {
      return 'Password is required';
    }
    if (value.length < 8) {
      return 'Password must be atleast 8 characters long';
    }
    return null;
  }

  //double check if passwords are the same,
  static String? confirmPassword(
      String? init_password, String? confirm_password) {
    if (confirm_password == null || confirm_password.trim().isEmpty) {
      return 'Please confirm your password';
    }
    if (init_password != confirm_password) {
      return 'Passwords do not match';
    }
    return null;
  }
}
