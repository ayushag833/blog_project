def password_validate(password):
    if not password:
        return False, "Password is required"

    if len(password) < 6:
        return False, "Password length must be minimum 6 characters long"

    if not any(char.isdigit() for char in password):
        return False, "Password should have at least one numeral"
        
    if not any(char.isupper() for char in password):
        return False, "Password should have at least one uppercase letter"
        
    if not any(char.islower() for char in password):
        return False, "Password should have at least one lowercase letter"
        
    if not any(char in ['$', '@', '#', '%'] for char in password):
        return False, "Password should have at least one of the symbols $@#%"

    return True, "Password Validation Success"


def create_update_record(request_data, model_class, serailizer_class):
    id = request_data.get('id')
    instance = model_class.objects.filter(id=id, is_active=True).first()
    if not instance: #POST
        serializer = serailizer_class(data=request_data)
    else: #PUT
        serializer = serailizer_class(instance, data=request_data, partial=True)        
    if serializer.is_valid():
        new_instance = serializer.save()
        return serailizer_class(new_instance).data
    return serializer.errors