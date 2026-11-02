class UserModel{
  final int? id;
  final String email;
  final String? username;
  final String? photoUrl;

  UserModel({
     this.id, 
     required this.email, 
    this.username, 
    this.photoUrl});
  
  factory UserModel.fromJson(Map<String, dynamic> json){
    return UserModel(
      id: json['id'] as int?,
      email: json['email'] as String,
      username: json['username'] as String?,
      photoUrl: json['photoUrl'] as String?,);
  }

  Map<String, dynamic> toJson(){
    return {
      if (id != null) 'id' : id,
      'email' : email,
      if(username != null)'username' : username,
      if(photoUrl != null)'photoUrl' : photoUrl, 
    };
  }

}