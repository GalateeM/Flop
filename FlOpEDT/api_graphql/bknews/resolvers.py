from displayweb.models import BreakingNews

def all_bknews(root, info): # week, year, dept
    return BreakingNews.objects.all()