from django.db.models.signals import pre_save, post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from .models import Task

@receiver(pre_save, sender=Task)
def store_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Task.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Task.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Task)
def notify_status_change(sender, instance, created, **kwargs):
    if created:
        return

    old_status = getattr(instance, '_old_status', None)
    if old_status is None or old_status == instance.status:
        return

    if instance.status == instance.last_notified_status:
        return

    if instance.owner and instance.owner.email:
        send_mail(
            subject=f'Task "{instance.title}" status changed',
            message=f'Status changed from {old_status} to {instance.status}',
            from_email='noreply@taskmanager.com',
            recipient_list=[instance.owner.email],
        )
        Task.objects.filter(pk=instance.pk).update(last_notified_status=instance.status)