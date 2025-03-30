from django.db import models
from django.dispatch import receiver
import os

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    gender = models.CharField(max_length=10, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='images/', blank=True, null=True)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, default="user1234")
    active_now = models.BooleanField(default=False)
    last_time_online = models.DateTimeField()

    # Semnal pentru a șterge poza de profil când un user este șters
    @receiver(models.signals.post_delete, sender='userApp.User')
    def auto_delete_file_on_delete(sender, instance, **kwargs):
        if instance.profile_photo and os.path.isfile(instance.profile_photo.path):
            os.remove(instance.profile_photo.path)

    def get_profile_photo_url(self):
        if self.profile_photo:
            return self.profile_photo.url
        
        # Alege poza default în funcție de gen
        if not self.gender:
            return '/static/userApp/images/default_image_neutral.png'
        elif self.gender.lower() == "male":
            return '/static/userApp/images/default_image_man.png'
        else:
            return '/static/userApp/images/default_image_woman.png'
        
    def __str__(self):
        if len(f"{self.last_name} - {self.first_name}") > 50:
            return f"{self.last_name} - {self.first_name}"[:50] + "..."
        return f"{self.last_name} - {self.first_name}"


class Message(models.Model):
    from_sender = models.UUIDField()
    body = models.CharField(max_length=500)
    sent_date = models.DateTimeField()
    conversation_id = models.ForeignKey('Conversation', on_delete=models.CASCADE)

    def __str__(self):
        if len(self.body) > 50:
            return self.body[:50] + "..."
        return self.body


class Conversation(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        if len(self.conversation_name) > 50:
            return self.conversation_name[:50] + "..."
        return self.conversation_name


class GroupMember(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_created=True)
    left_date = models.DateField(null=True)

    class Meta:
        unique_together = (('user_id', 'conversation_id'),)

    def __str__(self):
        user = User.objects.get(id=self.user_id)
        conversation = Conversation.objects.get(id=self.conversation_id)
        if len(f"{conversation.title} - {user.first_name}") > 50:
            return f"{conversation.title} - {user.first_name}"[:50] + "..."
        return f"{conversation.title} - {user.first_name}"