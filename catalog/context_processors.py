from .models import AppLink


def fbo_leads_url(request):
    """URL pubblico di FBOLeads, letto dalla card (AppLink) del catalogo.

    Usato nella topbar del Portale per il link "Leads". Vuoto se la card
    non esiste o è disattivata.
    """
    app = AppLink.objects.filter(slug='fboleads', is_active=True).first()
    return {'fbo_leads_url': app.url if app else ''}
