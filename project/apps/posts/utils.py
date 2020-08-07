from django.shortcuts import get_object_or_404
from project.apps.categories.models import Category, Subcategory

def category_and_subcategory_finder(data):
    """
    A funcion that recieves the request data and 
    decides category and subcategory for further usage
    """
    if data.get('category'):
        category = get_object_or_404(Category, pk=data.get('category'))
    else:
        category = None

    if self.request.data.get('subcategory'):
        if Subcategory.objects.filter(pk=data.get('subcategory')).exists():
            subcategory = Subcategory.objects.get(pk=data.get('subcategory'))
        else:
            subcategory = None
    else:
        subcategory = None
    
    return category, subcategory

def serializer_decider(serializer, category, subcategory):
    """
    A funcion that recieves the post serializer, category and subcategory,
    and executes save operation accordingly
    """
    if category:
        if subcategory:                
            serializer.save(category=category, subcategory=subcategory)
        else:
            serializer.save(category=category)
    elif subcategory:
        serializer.save(subcategory=subcategory)
    else:
        serializer.save()
    return serializer.data