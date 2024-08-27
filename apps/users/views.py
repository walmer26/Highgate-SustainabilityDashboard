from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import ProfileForm
from .models import Profile, User
from .serializers import UserSerializer


@login_required()
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')

    return render(request, 'users/profile.html', {'form': form, 'user': user})


@api_view()
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    serializer = UserSerializer(user)
    return Response(serializer.data)