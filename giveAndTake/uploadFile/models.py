from django.db import models

class File(models.Model):
    name = models.CharField(max_length=255)
    file_url = models.URLField()  # url of the file in cloudinary
    cloudinary_id = models.CharField(max_length=255)  # for deleting the file later
    owner = models.EmailField(max_length=255, null=False, blank=False)  # email of the user who has access to the file
    original_owner = models.EmailField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (owned by {self.original_owner})"

class TransferHistory(models.Model):
    file_name = models.CharField(max_length=255)
    from_user = models.EmailField(max_length=255)  # email of the user who transferred the file
    to_user = models.EmailField(max_length=255)  # email of the user who received the file
    action = models.CharField(max_length=10, choices=[('TRANSFER', 'TRANSFER'), ('REVOKE', 'REVOKE')])
    transferred_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.file_name} - {self.transferred_at} - {self.from_user} to {self.to_user}"
    
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f'format(self.username, self.email)'
    

# so one thing i have just pointing out right now is that
# when ever any document uploaded by a user
# the owner is the user who uploaded it
# and the original owner is the user who created the document
# that means both owner and original owner are same
