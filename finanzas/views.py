from django.shortcuts import render, redirect
from django.views import View
from .models import PagoInscripcion, IngresoEconomico, EgresoEconomico  # Cambiar a PagoInscripcion
from .forms import PagoInscripcionForm, IngresoEconomicoForm, EgresoEconomicoForm  # Cambiar a PagoInscripcionForm

class RegistrarPagoInscripcionView(View):
    def get(self, request):
        form = PagoInscripcionForm()
        return render(request, 'finanzas/registrar_pago_inscripcion.html', {'form': form})

    def post(self, request):
        form = PagoInscripcionForm(request.POST)
        if form.is_valid():
            pago = form.save()
            # Registrar el ingreso automáticamente
            IngresoEconomico.objects.create(
                fecha_ingreso=pago.fecha_pago,
                monto=pago.monto,
                tipo_ingreso='concurso',
            )
            IngresoEconomico.save()
            return redirect('lista_inscripciones')
        return render(request, 'finanzas/registrar_pago_inscripcion.html', {'form': form})

class RegistrarIngresoEconomicoView(View):
    def get(self, request):
        form = IngresoEconomicoForm()
        return render(request, 'finanzas/registrar_ingreso_economico.html', {'form': form})

    def post(self, request):
        form = IngresoEconomicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ingresos')
        return render(request, 'finanzas/registrar_ingreso_economico.html', {'form': form})

class RegistrarEgresoEconomicoView(View):
    def get(self, request):
        form = EgresoEconomicoForm()
        return render(request, 'finanzas/registrar_egreso_economico.html', {'form': form})

    def post(self, request):
        form = EgresoEconomicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_egresos')
        return render(request, 'finanzas/registrar_egreso_economico.html', {'form': form})
