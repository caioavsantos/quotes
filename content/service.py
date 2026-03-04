import random
from .models import Quote, DailyQuote
from django.utils import timezone

def get_day_quote():

    if not Quote.objects.exists():
        return None
    
    today = timezone.localdate()

    daily = DailyQuote.objects.filter(date=today).first()
    if daily:
        return daily.quote
    
    used_quotes = DailyQuote.objects.values_list("quote_id", flat=True)
    unused_quotes = Quote.objects.exclude(id__in=used_quotes)

    if not unused_quotes.exists():
        DailyQuote.objects.all().delete()
        unused_quotes = Quote.objects.all()
    
    quote = random.choice(list(unused_quotes))

    DailyQuote.objects.create(date=today, quote=quote)

    return quote