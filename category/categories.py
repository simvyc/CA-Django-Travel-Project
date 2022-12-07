from category.models import Category

def menu_links(request):
    links = Category.objects.all()
    # returns categories list and stores in this variable links
    return dict(links=links)