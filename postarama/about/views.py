from django.views.generic.base import TemplateView

from .models import Image, Technology


class AboutAuthorView(TemplateView):
    # В переменной template_name обязательно указывается имя шаблона,
    # на основе которого будет создана возвращаемая страница
    template_name = "about/author.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["img_1"] = Image.objects.all()[0]
        context["img_2"] = Image.objects.all()[1]
        context["img_3"] = Image.objects.all()[2]
        return context


class AboutTechView(TemplateView):
    # В переменной template_name обязательно указывается имя шаблона,
    # на основе которого будет создана возвращаемая страница
    template_name = "about/tech.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["techs"] = Technology.objects.all()

        return context
