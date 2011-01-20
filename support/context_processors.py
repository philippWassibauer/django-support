from models import SupportQuestion

def ticket_count(request):
    return { 'OPEN_TICKETS': SupportQuestion.objects.filter(closed=False).count(),
        'UNACCEPTED_TICKETS': SupportQuestion.objects.filter(accepted_by__isnull=True).count()}