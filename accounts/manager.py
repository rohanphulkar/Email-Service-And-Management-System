from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,username,name,password=None):
        if not username:
            raise ValueError("Username is required")
        if not name:
            raise ValueError("Name is required")
        if not password:
            raise ValueError("Password is required")
        
        # create a new user instance
        user = self.model(
            username=username,
            name=name,
        )

        #set the password
        user.set_password(password)

        #save the user instance
        user.save()
        return user
    
    def create_superuser(self,username,name,password=None):
        if not password:
            raise ValueError("Password is required")
        
        # create a new user instance with create_user method
        user = self.create_user(username=username,name=name,password=password)

        # set the ser's admin, staff and superuser flags
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        # save the user instance
        user.save()
        return user