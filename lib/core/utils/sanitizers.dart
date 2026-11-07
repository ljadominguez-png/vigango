class AppSanitizer {
  AppSanitizer._();

  static final _whitespacePattern = RegExp(r'\s+');
  static final _usernameInvalidCharsPattern = RegExp(r'[\w]');

  static String email(String? input) {
    if (input == null) return '';
    return input.trim().toLowerCase();
  }

  static String username(String? input) {
    if (input == null) return '';
    return input
        .trim()
        .toLowerCase()
        .replaceAll(_whitespacePattern, '_')
        .replaceAll(_usernameInvalidCharsPattern, '');
  }
}
