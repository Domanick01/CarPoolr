from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Message



User = get_user_model()

@login_required
def inbox(request):
    # Get all users the current user has chatted with
    user = request.user
    conversations = User.objects.filter(
        Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
    ).exclude(id=user.id).distinct()

    return render(request, 'chat/inbox.html', {'conversations': conversations})


@login_required
def conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    user = request.user

    # Mark messages as read
    Message.objects.filter(sender=other_user, recipient=user, is_read=False).update(is_read=True)

    messages = Message.objects.filter(
        Q(sender=user, recipient=other_user) |
        Q(sender=other_user, recipient=user)
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(sender=user, recipient=other_user, content=content)
            return redirect('chat:conversation', user_id=user_id)

    return render(request, 'chat/conversation.html', {
        'other_user': other_user,
        'messages': messages,
    })
