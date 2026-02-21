from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Driver, Vehicle, Route, StudentTransport, TransportAttendance, MaintenanceLog, FuelLog
from core.models import User, Announcement
from students.models import Student

@login_required
def transport_dashboard(request):
    if request.user.role not in [User.Role.TRANSPORT_MANAGER, User.Role.ADMIN]:
        # Ideally, Drivers might also access this or a subset
        return render(request, 'core/access_denied.html')

    total_vehicles = Vehicle.objects.count()
    total_drivers = Driver.objects.count()
    total_routes = Route.objects.count()
    total_transport_students = StudentTransport.objects.count()

    maintenance_alerts = MaintenanceLog.objects.order_by('-date')[:5]
    fuel_logs = FuelLog.objects.order_by('-date')[:5]
    announcements = Announcement.objects.filter(target_role=User.Role.TRANSPORT_MANAGER).order_by('-date_posted')[:5]

    context = {
        'total_vehicles': total_vehicles,
        'total_drivers': total_drivers,
        'total_routes': total_routes,
        'total_transport_students': total_transport_students,
        'maintenance_alerts': maintenance_alerts,
        'fuel_logs': fuel_logs,
        'announcements': announcements,
    }
    return render(request, 'transport/dashboard.html', context)

@login_required
def driver_dashboard(request):
    try:
        driver = request.user.driver_profile
    except Driver.DoesNotExist:
        # Fallback if accessed by non-driver or misconfigured user
        return render(request, 'core/access_denied.html')

    # Get assigned vehicle
    try:
        vehicle = driver.assigned_vehicle
    except Vehicle.DoesNotExist:
        vehicle = None
    
    # Get routes for vehicle
    routes = []
    if vehicle:
        routes = vehicle.routes.all()
    
    context = {
        'driver': driver,
        'vehicle': vehicle,
        'routes': routes
    }
    return render(request, 'transport/driver_dashboard.html', context)

@login_required
def manage_attendance(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    allocations = StudentTransport.objects.filter(route=route)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        for alloc in allocations:
            pickup = request.POST.get(f'pickup_{alloc.student.id}') == 'on'
            drop = request.POST.get(f'drop_{alloc.student.id}') == 'on'
            
            TransportAttendance.objects.update_or_create(
                student=alloc.student,
                route=route,
                date=date,
                defaults={'is_present_pickup': pickup, 'is_present_drop': drop}
            )
        messages.success(request, f"Attendance updated for route {route.name}")
        return redirect('transport:dashboard')

    return render(request, 'transport/manage_attendance.html', {'route': route, 'allocations': allocations})

@login_required
def log_fuel(request):
    is_driver = hasattr(request.user, 'driver_profile')
    driver_vehicle = None
    if is_driver:
        try:
            driver_vehicle = request.user.driver_profile.assigned_vehicle
        except (AttributeError, Vehicle.DoesNotExist):
            driver_vehicle = None

    if request.method == 'POST':
        # If driver, force their vehicle, else get from form
        if is_driver and driver_vehicle:
            vehicle_id = driver_vehicle.id
        else:
            vehicle_id = request.POST.get('vehicle')
            
        date = request.POST.get('date')
        liters = request.POST.get('liters')
        cost = request.POST.get('cost')
        odometer = request.POST.get('odometer')
        
        if vehicle_id:
            FuelLog.objects.create(
                vehicle_id=vehicle_id,
                date=date,
                liters=liters,
                cost=cost,
                odometer_reading=odometer
            )
            messages.success(request, "Fuel log added successfully.")
        else:
            messages.error(request, "No vehicle selected or assigned.")

        if is_driver:
            return redirect('transport:driver_dashboard')
        return redirect('transport:dashboard')
    
    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles,
        'is_driver': is_driver,
        'driver_vehicle': driver_vehicle
    }
    return render(request, 'transport/log_fuel.html', context)

@login_required
def log_maintenance(request):
    is_driver = hasattr(request.user, 'driver_profile')
    driver_vehicle = None
    if is_driver:
        try:
            driver_vehicle = request.user.driver_profile.assigned_vehicle
        except (AttributeError, Vehicle.DoesNotExist):
            driver_vehicle = None

    if request.method == 'POST':
        if is_driver and driver_vehicle:
            vehicle_id = driver_vehicle.id
        else:
            vehicle_id = request.POST.get('vehicle')
            
        date = request.POST.get('date')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        serviced_by = request.POST.get('serviced_by')
        
        if vehicle_id:
            MaintenanceLog.objects.create(
                vehicle_id=vehicle_id,
                date=date,
                description=description,
                cost=cost,
                serviced_by=serviced_by
            )
            messages.success(request, "Maintenance log added successfully.")
        else:
             messages.error(request, "No vehicle selected or assigned.")

        if is_driver:
             return redirect('transport:driver_dashboard')
        return redirect('transport:dashboard')

    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles,
        'is_driver': is_driver,
        'driver_vehicle': driver_vehicle
    }
    return render(request, 'transport/log_maintenance.html', context)


@login_required
def driver_profile(request):
    try:
        driver = request.user.driver_profile
    except Driver.DoesNotExist:
        return render(request, 'core/access_denied.html')

    # Get assigned vehicle
    try:
        vehicle = driver.assigned_vehicle
    except Vehicle.DoesNotExist:
        vehicle = None

    # Get routes for vehicle
    routes = []
    if vehicle:
        routes = vehicle.routes.all()

    # Get recent fuel & maintenance logs
    fuel_logs = []
    maintenance_logs = []
    if vehicle:
        fuel_logs = FuelLog.objects.filter(vehicle=vehicle).order_by('-date')[:5]
        maintenance_logs = MaintenanceLog.objects.filter(vehicle=vehicle).order_by('-date')[:5]

    context = {
        'driver': driver,
        'vehicle': vehicle,
        'routes': routes,
        'fuel_logs': fuel_logs,
        'maintenance_logs': maintenance_logs,
    }
    return render(request, 'transport/driver_profile.html', context)
