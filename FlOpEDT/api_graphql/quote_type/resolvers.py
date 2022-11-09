from quote.models import QuoteType

def all_quote_types(root, info):
    return QuoteType.objects.all()
