from django.db import models
from django.contrib.auth.models import User

# جدول المعالم السياحية
class Landmark(models.Model):  
    Destination = models.CharField(max_length=200)      # اسم المدينة
    Landmark_Name = models.CharField(max_length=200)      # اسم المعلم
    Description = models.TextField()              # وصف المعلم
    Image_Url = models.URLField(max_length=500, blank=True)  # رابط الصورة 
    def __str__(self):
        return self.Landmark_Name

# جدول المفضلة
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # ربط المفضلة بالمستخدم
    landmark = models.ForeignKey("Landmark", on_delete=models.CASCADE, related_name='favorite_set') # ربط المفضلة بالمعلم السياحي
    created_at = models.DateTimeField(auto_now_add=True) # تاريخ إضافة المعلم إلى المفضلة

    class Meta:
        unique_together = ('user', 'landmark') # التأكد من أن المستخدم لا يمكنه إضافة نفس المعلم إلى المفضلة أكثر من مرة

    def __str__(self):
        return f"{self.user.username} - {self.landmark.Landmark_Name}"
    
# جدول القصص والتعليقات 
class Story(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) # الشخص اللي كتب القصة 
    landmark = models.ForeignKey("Landmark", on_delete=models.CASCADE, related_name='story_set') # المعلم المرتبط بالقصة 
    content = models.TextField() # نص القصة أو التعليق 
    created_at = models.DateTimeField(auto_now_add=True) # تاريخ الإضافة 
    
    def __str__(self): 
        return f"{self.user.username} - {self.landmark.Landmark_Name}"

# for storing logs to display activities in Dashboard    
class ImageRecognitionLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
class ActivityLog(models.Model):
    ACTION_TYPES = [
        ('search', 'Search'),
        ('image_recognition', 'Image Recognition'),
        ('like', 'Like'),
        ('comment', 'Comment'),
    ]

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=30, choices=ACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    landmark = models.ForeignKey(Landmark, null=True, blank=True, on_delete=models.SET_NULL)