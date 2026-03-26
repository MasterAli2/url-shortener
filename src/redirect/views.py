from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from .models import ShortLink
from .forms import ShortLinkForm

from django.contrib.auth.decorators import login_required

def redirect_view(request, code): 
    shortlink = ShortLink.get_shortlink(code)
    if shortlink is None:
        return render(request, '404.html', {'message': 'That short link does not exist.'}, status=404)
    
    return redirect(shortlink.url, permanent=False, preserve_request=True)

def inspect_view(request, code):
    shortlink = ShortLink.get_shortlink(code)
    if shortlink is None:
        return render(request, '404.html', {'message': 'That short link does not exist.'}, status=404)
    
    return HttpResponse(f"The requested shortlink links to: {shortlink.url}")


@login_required
def dashboard_view(request: HttpRequest):
    form_type = request.POST.get('form_type')
    
    
    create_form = ShortLinkForm(request.POST or None)
    if request.method == 'POST':
        if form_type == 'create' and create_form.is_valid():
            link = create_form.save(commit=False)
            link.owner = request.user
            link.save()
            return redirect(request.path)
        if form_type == 'delete':
            code = request.POST.get('code')
            if code:
                ShortLink.objects.filter(code=code, owner=request.user).delete()
            return redirect(request.path)
            
            
    shortlinks = ShortLink.get_shortlinks_of(request.user)
    return render(request, 'redirect.html',{'links':shortlinks,
                                            'create_form':create_form})
