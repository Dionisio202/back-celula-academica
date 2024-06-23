from django.shortcuts import render, redirect
from django.views import View
from .models import Concurso, Charla, Ponente
from .forms import ConcursoForm, CharlaForm, PonenteForm, InscripcionConcursoForm

class CrearConcursoView(View):
    def get(self, request):
        form = ConcursoForm()
        return render(request, 'admin/eventos/crear_concurso.html', {'form': form})

    def post(self, request):
        form = ConcursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:eventos_concurso_changelist')
        return render(request, 'admin/eventos/crear_concurso.html', {'form': form})

class CrearCharlaView(View):
    def get(self, request):
        form = CharlaForm()
        return render(request, 'admin/eventos/crear_charla.html', {'form': form})

    def post(self, request):
        form = CharlaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:eventos_charla_changelist')
        return render(request, 'admin/eventos/crear_charla.html', {'form': form})

class CrearPonenteView(View):
    def get(self, request):
        form = PonenteForm()
        return render(request, 'admin/eventos/crear_ponente.html', {'form': form})

    def post(self, request):
        form = PonenteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin:eventos_ponente_changelist')
        return render(request, 'admin/eventos/crear_ponente.html', {'form': form})


class InscribirseConcursoView(View):
    def get(self, request, concurso_id):
        concurso = Concurso.objects.get(id=concurso_id)
        form = InscripcionConcursoForm(initial={'concurso': concurso})
        return render(request, 'eventos/inscribirse_concurso.html', {'form': form, 'concurso': concurso})

    def post(self, request, concurso_id):
        concurso = Concurso.objects.get(id=concurso_id)
        form = InscripcionConcursoForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.concurso = concurso
            inscripcion.save()
            return redirect('concurso_detalle', concurso_id=concurso.id)
        return render(request, 'eventos/inscribirse_concurso.html', {'form': form, 'concurso': concurso})
