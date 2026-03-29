# dashboard/views.py
from django.shortcuts import render
from django.db.models import Sum
from finanzas.models import IngresoEconomico, EgresoEconomico

def financial_dashboard(request):
    total_ingresos = IngresoEconomico.objects.aggregate(Sum('monto'))['monto__sum'] or 0
    total_egresos = EgresoEconomico.objects.aggregate(Sum('monto'))['monto__sum'] or 0
    balance = total_ingresos - total_egresos

    tipos_ingreso = IngresoEconomico.objects.values('tipo_ingreso').distinct()
    tipos_egreso = EgresoEconomico.objects.values('tipo_egreso').distinct()

    context = {
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'balance': balance,
        'tipos_ingreso': tipos_ingreso,
        'tipos_egreso': tipos_egreso,
    }
    return render(request, 'dashboard/financial_dashboard.html', context)
