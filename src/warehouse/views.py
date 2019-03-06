from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'warehouse/index.html'


class AboutView(TemplateView):
    template_name = 'warehouse/about.html'


class ProductsView(TemplateView):
    template_name = 'warehouse/products.html'


class ContactView(TemplateView):
    template_name = 'warehouse/contact.html'
