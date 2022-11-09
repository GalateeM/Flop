from quote.models import Quote

def all_quote(root,info):
    return Quote.objects.all()