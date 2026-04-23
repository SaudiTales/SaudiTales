from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import Landmark, Favorite, Story, ImageRecognitionLog, ActivityLog 
from django.db.models import Q, Count, F
from django.db.models.functions import TruncDate, TruncMonth
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta
import os
import joblib, random
import numpy as np
from PIL import Image
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Create your views here.
def home(request):

    # to count number of likes and comments of landmarks
    popular_landmarks = Landmark.objects.annotate(
        likes_count=Count('favorite_set', distinct=True),
        comments_count=Count('story_set', distinct=True),
        popularity_score=F('likes_count') + 0.5 * F('comments_count')
    ).order_by('-popularity_score')[:3]

    return render(request, 'frontend/home.html', {
        'popular_landmarks': popular_landmarks,
    })
def explore(request):
    return render(request, 'frontend/explore.html',{
    })
def exploreResult(request):
    query = request.GET.get('q', '') #the one we used as name
    region = request.GET.get('region', '')
    search_type = 'text'

    #to prevent empty search
    if not query and not region:
        return render(request, 'frontend/explore.html', {
            'error_message': "Please enter a search term or select a region to continue."
        })
    
    if query and len(query) < 3:
        return render(request, 'frontend/exploreResult.html', {
            'query': query,
            'region': region,
            'error_message': "Please enter at least 3 characters to search."
        })

    landmark = None
    top_landmarks = []
    related_landmarks = [] # it will be by reigon since we have reigon filter
    explore_landmarks = [] #this is for filter by region
    random_landmarks = [] # for when no result 
    
    #1- when using filter:
    if region and not query:
        explore_landmarks = list(
            Landmark.objects.filter(Destination__iexact=region)
        )
        random.shuffle(explore_landmarks)
        return render(request, 'frontend/exploreResult.html', {
            'explore_landmarks': explore_landmarks,
            'query': '',
            'region': region,
            'landmark': None,
            'top_landmarks': [],
            'related_landmarks': [],
            'random_landmarks': [],
            'search_type': 'text',
        })
    
    #2- when normail search:
    if query:
        results = Landmark.objects.filter(
            #we used icontains to "NOT" make the search case sensitive
            Q(Landmark_Name__icontains=query) | Q(Destination__icontains=query)
        )
        
        #2.1 if result exist:
        if results.exists():

            # landmark = results.first() if results.count() == 1 else None
            # top_landmarks = results if results.count() > 1 else []
            
            if results.count() == 1:
                landmark = results.first()

            else:
                top_landmarks = results
                
            first_result = results.first()


            related_landmarks = list(
                Landmark.objects.filter(Destination=first_result.Destination)
                .exclude(id__in=results.values_list('id', flat=True))
            )

            related_landmarks = random.sample(
                related_landmarks,
                min(3, len(related_landmarks))
            )

        #2.2 if no result:
        else:
            random_landmarks = list(Landmark.objects.all())
            random_landmarks = random.sample(
                random_landmarks,
                min(3, len(random_landmarks))
            )

            return render(request, 'frontend/exploreResult.html', {
                'random_landmarks': random_landmarks,
                'query': query,
                'region': region,
                'search_type': 'text',
            })

    # #3- when no result appear (other places section)
    # if not query and not region:
    #     random_landmarks = list(Landmark.objects.all())
    #     random.shuffle(random_landmarks)
    #     random_landmarks = random_landmarks[:3]

    #     return render(request, 'frontend/exploreResult.html', {
    #         'random_landmarks': random_landmarks,
    #         'query': query,
    #         'region': region,
    #     })

    return render(request, 'frontend/exploreResult.html', {
        'landmark': landmark,
        'top_landmarks': top_landmarks,
        'related_landmarks': related_landmarks,
        'random_landmarks': random_landmarks,
        'explore_landmarks': explore_landmarks,
        'query': query,
        'region': region,
        'search_type': 'text',
    })
def infoPlace(request, landmark_id):
    # to fetch the landmark details using the provided landmark_id
    place = get_object_or_404(Landmark, id=landmark_id)
    
    # count views of this landmark
    ActivityLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action_type='view_landmark',
        landmark=place
    )
    
    #to check if this landmark is favorited by the user
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            landmark=place
        ).exists()
    
     #to handle comment submission
    if request.user.is_authenticated and request.method == "POST":
        comment_content = request.POST.get("comment")  # match the input's name in template
        if comment_content:
            from .models import Story  # make sure Story model exists
            Story.objects.create(user=request.user, landmark=place, content=comment_content)
            ActivityLog.objects.create(
                user=request.user,
                action_type='comment'
            )
        return redirect('infoPlace', landmark_id=landmark_id)  # refresh page to show new comment
    
    #to get all comments for this landmark to be displayed
    stories = place.story_set.order_by('-created_at')  # newest first


    return render(request, 'frontend/InfoPlace.html', {
        'place': place,
        'is_favorite': is_favorite,
        'stories': stories,        
    })

@login_required
def profile(request):
    user = request.user
    # Get all landmarks this user has favorited + the comments they shared
    favorites = Favorite.objects.filter(user=user).select_related('landmark')
    user_stories = Story.objects.filter(user=user).order_by('-created_at')
    
    # to have only one card even if user have multiple comments in the same landmark
    unique_stories = {}
    for story in user_stories:
        if story.landmark.id not in unique_stories:
            unique_stories[story.landmark.id] = story
    user_stories_unique = list(unique_stories.values())

    # this is for editing the user display name/first name
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        username = request.POST.get("username")
        email = request.POST.get("email")


        # to check if username exists
        if username and User.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('profile')

        # to check if email exist
        if email and User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('profile')

        #if they are not repeated, update them
        if first_name:
            user.first_name = first_name
        if username:
            user.username = username
        if email:
            user.email = email
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    
    context = {
        'favorites': [f.landmark for f in favorites],
        'user_stories': user_stories_unique,
    }
    return render(request, 'frontend/profile.html', context)

def register(request):

    if request.method == "POST":

        first_name  = request.POST.get("first_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "account/register.html")

        # to do Email check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "account/register.html")
        
        # password rules
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e:
                messages.error(request, error)
            return render(request, "account/register.html")
        
        # create user
        user = User.objects.create_user(
            first_name=first_name,
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect("/login/")

    return render(request, "account/register.html")

def login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            if user.is_staff or user.is_superuser:
                return redirect("dashboard")
            else:
                return redirect("home")

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "account/login.html")

def logout_view(request):
    auth_logout(request)
    return redirect("home")

@login_required
def toggle_favorite(request, landmark_id):
    landmark = get_object_or_404(Landmark, id=landmark_id)
    favorite_obj = Favorite.objects.filter(user=request.user, landmark=landmark).first()

    if favorite_obj:
        # Already favorited -> remove it
        favorite_obj.delete()
    else:
        # Not favorited -> add it
        Favorite.objects.create(user=request.user, landmark=landmark)

    ActivityLog.objects.create(
        user=request.user,
        action_type='like'
    )
    
    return redirect('infoPlace', landmark_id=landmark.id)

def admin_required(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)
def user_only(user):
    return user.is_authenticated and not (user.is_staff or user.is_superuser)

#admin dashboard:
@login_required
@user_passes_test(admin_required, login_url='/')
def dashboard(request):
    users_count = User.objects.count()
    landmarks_count = Landmark.objects.count()
    comments_count = Story.objects.count()
    image_ops_count = ImageRecognitionLog.objects.count()
    failed_ops_count = ImageRecognitionLog.objects.filter(success=False).count()
    three_months_ago = timezone.now() - timedelta(days=90)
    last_30_days = timezone.now() - timedelta(days=30)

    #landmark % based on reigon
    landmarks_by_dest = Landmark.objects.values('Destination').annotate(count=Count('id')).order_by('-count')
    destinations = [item['Destination'] for item in landmarks_by_dest]
    dest_counts = [item['count'] for item in landmarks_by_dest]

    # for img recognition success/fail last 3 months count
    end_date = timezone.now()
    start_date = end_date - relativedelta(months=2)  # includes current + 2 previous

    image_monthly = (
        ImageRecognitionLog.objects
        .filter(created_at__gte=start_date)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            success_count=Count('id', filter=Q(success=True)),
            failed_count=Count('id', filter=Q(success=False))
        )
        .order_by('month')
    )
    #to show 3 month timeline
    months = []
    success_map = {}
    failed_map = {}
    current = start_date.replace(day=1)
    for i in range(3):
        month_key = current.strftime("%b %Y")
        months.append(month_key)
        success_map[month_key] = 0
        failed_map[month_key] = 0
        current += relativedelta(months=1)
    
    for item in image_monthly:
        key = item['month'].strftime("%b %Y")
        success_map[key] = item['success_count']
        failed_map[key] = item['failed_count']

    image_labels = months
    success_counts = [success_map[m] for m in months]
    failed_counts = [failed_map[m] for m in months]

    # for avtivities(comment/like/search/img recog) log
    activity_monthly = (
        ActivityLog.objects
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    activity_labels = [a['day'].strftime("%m-%d") for a in activity_monthly]
    activity_counts = [a['count'] for a in activity_monthly]


    #for users growth count
    user_growth = (
        User.objects
        .filter(date_joined__gte=last_30_days)
        .annotate(day=TruncDate('date_joined'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    user_labels = [u['day'].strftime("%d %b") for u in user_growth]
    user_counts = [u['count'] for u in user_growth]


    # to show top 5 viewd landmarks
    top_viewed = (
        ActivityLog.objects
        .filter(action_type='view_landmark', landmark__isnull=False)
        .values('landmark__Landmark_Name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    top_viewed_labels = [i['landmark__Landmark_Name'] for i in top_viewed]
    top_viewed_counts = [i['count'] for i in top_viewed]

    context = {
        'users_count': User.objects.count(),
        'landmarks_count': Landmark.objects.count(),
        'comments_count': Story.objects.count(),
        'image_ops_count': image_ops_count,
        'failed_ops_count': failed_ops_count,
        'destinations': destinations,
        'dest_counts': dest_counts,
        'image_labels': image_labels,
        'success_counts': success_counts,
        'failed_counts': failed_counts,
        'activity_labels': activity_labels,
        'activity_counts': activity_counts,
        'user_labels': user_labels,
        'user_counts': user_counts,
        'top_viewed_labels': top_viewed_labels,
        'top_viewed_counts': top_viewed_counts,
    }
    return render(request, 'adminDashboard/dashboard.html', context)

@login_required
@user_passes_test(admin_required, login_url='/')
def landmarks(request):
    landmarks = Landmark.objects.all()
    return render(request, 'adminDashboard/landmarks.html', {'landmarks': landmarks})
@login_required
@user_passes_test(admin_required, login_url='/')
def delete_landmark(request, landmark_id):
    if request.method == "POST":
        landmark = get_object_or_404(Landmark, id=landmark_id)
        landmark.delete()
    return redirect('landmarks')
@login_required
@user_passes_test(admin_required, login_url='/')
def add_landmark(request):
    if request.method == "POST":
        destination = request.POST.get("Destination")
        name = request.POST.get("Landmark_Name")
        description = request.POST.get("Description")
        image_url = request.POST.get("Image_Url")

        Landmark.objects.create(
            Destination=destination,
            Landmark_Name=name,
            Description=description,
            Image_Url=image_url
        )
        return redirect('landmarks')
    return redirect('landmarks')
@login_required
@user_passes_test(admin_required, login_url='/')
def update_landmark(request, landmark_id):
    landmark = get_object_or_404(Landmark, id=landmark_id)

    if request.method == "POST":
        #landmark = Landmark.objects.get(id=landmark_id)

        landmark.Destination = request.POST.get("Destination")
        landmark.Landmark_Name = request.POST.get("Landmark_Name")
        landmark.Description = request.POST.get("Description")
        landmark.Image_Url = request.POST.get("Image_Url")

        landmark.save()

        return redirect("landmarks")
    return render(request, 'update_landmark.html', {'landmark': landmark})
@login_required
@user_passes_test(admin_required, login_url='/')
def accountMange(request):
    users = User.objects.all()
    return render(request, 'adminDashboard/AccountMang.html', {'users': users})
@login_required
@user_passes_test(admin_required, login_url='/')
def delete_user(request, id):
    if request.method == "POST":
        user = get_object_or_404(User, id=id)

        if request.user == user:
            messages.error(request, "You cannot delete your own account!")
            return redirect('AccountManagement')

        user.delete()
    return redirect('AccountManagement')
@login_required
@user_passes_test(admin_required, login_url='/')
def disable_user(request, id):
    if request.method == "POST":
        user = get_object_or_404(User, id=id)

        if request.user == user:
            messages.error(request, "You cannot disable your own account!")
            return redirect('AccountManagement')

        user.is_active = False
        user.save()
    return redirect('AccountManagement')
@login_required
@user_passes_test(admin_required, login_url='/')
def enable_user(request, id):
    if request.method == "POST":
        user = get_object_or_404(User, id=id)
        user.is_active = True
        user.save()
    return redirect('AccountManagement')
@login_required
@user_passes_test(admin_required, login_url='/')
def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('AccountManagement')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('AccountManagement')

        User.objects.create_user(
            username=username,
            email=email,
            password="12345678", #temp password, will be changed later
            first_name="Admin",
            is_superuser=True,
            is_staff=True 
        )

        messages.success(request, "User added successfully!")

    return redirect('AccountManagement')
# for download the MobileNet module once when running the server
base_model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
# Download the features from landmark_features.pkl file 
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml_model', 'landmark_features.pkl')
landmark_features = joblib.load(MODEL_PATH)

# AI Landmark Recognition Model
def predict_landmark(request):
    landmark = None
    top_landmarks = []
    error_msg = None
    success = False

    BASE_THRESHOLD = 0.60
    MARGIN_THRESHOLD = 0.02

    search_type = 'image'

    if request.method == 'POST':

        if not request.FILES.get('image'):
            return render(request, 'frontend/explore.html', {
                'error_message': "Please upload an image before searching."
            })

    if request.method == 'POST' and request.FILES.get('image'):
        try:
            # 1 prepare image
            uploaded_img = request.FILES['image']
            img = Image.open(uploaded_img).convert('RGB')
            img = img.resize((224, 224))
            img_array = np.array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            # 2️ Feature extraction
            query_feature = base_model.predict(img_array, verbose=0).flatten()
            query_feature = normalize([query_feature])[0]

            # 3️ Calculate the highest similarity for each landmark
            similarities = []
            for landmark_id, feature_list in landmark_features.items():
                max_score = -1
                for stored_feature in feature_list:
                    score = cosine_similarity([query_feature], [stored_feature])[0][0]
                    if score > max_score:
                        max_score = score
                similarities.append((landmark_id, max_score))

            # Sort results from highest to lower similarity
            similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

            best_id, best_score = similarities[0]
            second_score = similarities[1][1]
            margin = best_score - second_score

            # 4️ Decision Logic
            if best_score >= BASE_THRESHOLD and margin > MARGIN_THRESHOLD:
                landmark = Landmark.objects.get(id=int(best_id))
                success = True
            else:
                top_3_ids = [int(i) for i, s in similarities[:3]]
                top_landmarks = [Landmark.objects.get(id=lid) for lid in top_3_ids]
                success = False

        except Exception as e:
            error_msg = f"An error occurred during processing: {str(e)}"
            success = False
    
        ImageRecognitionLog.objects.create(success=success)

        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action_type='image_recognition'
        )

    return render(request, 'frontend/exploreResult.html', {
        'landmark': landmark,
        'top_landmarks': top_landmarks,
        'error': error_msg,
        'search_type': 'image',
    })