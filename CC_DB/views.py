from django.shortcuts import render
import os
import csv
from CC_DB.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Polygon
from django.contrib.gis.geos import LineString
from django.contrib.gis.geos import Point


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


### need to delete database, reinstall spatial extensions, remake tables with migrate, and repopulate

def fill_units():
    with open(os.path.join(BASE_DIR, 'units.csv'), 'rb') as f:
        reader = csv.reader(f)
        l = 0
        for row in reader:
            l += 1
            if l > 1:
                xyz = row[2].split(",")
                p = [None] * int(row[1])
                for n in range(1,int(row[1])+1):
                    p[n-1] = Point(float(xyz[(n-1)*3]),float(xyz[(n-1)*3+1]),float(xyz[((n-1)*3+2)]))
                if int(row[1]) == 1:
                    g = p[0]
                if int(row[1]) == 2:
                    g = LineString((p[0],p[1]))
                if int(row[1]) > 2:
                    if p[0]==p[int(row[1])-1]:
                        g = Polygon(p)
                    else:
                        g = LineString(p)
                s, created  = Excavation_unit.objects.get_or_create(unit=row[0],defaults={'extent': g})
                s.save()


def fill_xyz():
    with open(os.path.join(BASE_DIR, 'xyz.csv'), 'rb') as f:
        reader = csv.reader(f)
        l = 0
        for row in reader:
            l += 1
            if l > 1:
                s = Context.objects.get(pk = row[0])
                xyz = row[2].split(",")
                p = [None] * int(row[1])
                for n in range(1,int(row[1])+1):
                    p[n-1] = Point(float(xyz[(n-1)*3]),float(xyz[(n-1)*3+1]),float(xyz[((n-1)*3+2)]))
                if int(row[1]) == 1:
                    g = p[0]
                if int(row[1]) == 2:
                    g = LineString((p[0],p[1]))
                if int(row[1]) > 2:
                    p.append(p[0])
                    g = Polygon(p)
                s.points = g
                s.save()


def fill_context():
    with open(os.path.join(BASE_DIR, 'context.csv'), 'rb') as f:
        reader = csv.reader(f)
        n = 0
        for row in reader:
            n += 1
            if n > 1:
                s = Context(pk=row[0], cat_no=row[1], unit=row[2], id_no=row[3], level=row[4], code=row[5])
                s.save()


def fill_photos():
    with open(os.path.join(BASE_DIR, 'photos.csv'), 'rb') as f:
        reader = csv.reader(f)
        n = 0
        for row in reader:
            n += 1
            if n > 1:
                s = Photo(pk = row[0], image01 = row[1])
                s.save()
    # Now reload the context data to repair the empty records created by adding small_finds (it is a django bug)
    fill_context()


def fill_small_finds():
    with open(os.path.join(BASE_DIR, 'small_finds.csv'), 'rb') as f:
        reader = csv.reader(f)
        n = 0
        for row in reader:
            n += 1
            if n > 1:
                for n in range(1,len(row)):
                    if int(row[n]) == -1:
                        row[n] = None
                s = Small_Find(pk = row[0], coarse_stone_weight = row[1], coarse_fauna_weight = row[2], fine_stone_weight = row[3], fine_fauna_weight = row[4])
                s.save()
    # Now reload the context data to repair the empty records created by adding small_finds (it is a django bug)
    fill_context()


def fill_lithics():
    with open(os.path.join(BASE_DIR, 'lithics.csv'), 'rb') as f:
        reader = csv.reader(f)
        n = 0
        for row in reader:
            n += 1
            if n > 1:
                for n in range(1,len(row)):
                    if row[n] == 'NA':
                        row[n] = None
                    if row[n] == 'N/A':
                        row[n] = None
                    if row[n] == "":
                        row[n] = None
                s = Lithic(pk = row[0], dataclass = row[1], technique = row[2], alteration = row[3], edge_damage = row[4], platform_surface = row[5], platform_exterior = row[6], form = row[7], scar_morphology = row[8], fb_type = row[9], fb_type_2 = row[10], fb_type_3 = row[11], retouched_edges = row[12], retouch_intensity = row[13], reprise = row[14], raw_material = row[15], exterior_surface = row[16], exterior_type = row[17], platform_technique = row[18], platform_angle = row[19], core_shape = row[20], core_blank = row[21], core_surface_percentage = row[22], proximal_removals = row[23], prepared_platforms = row[24], flake_direction = row[25], scar_length = row[26], scar_width = row[27], multiple = row[28], length = row[29], width = row[30], maximum_width = row[31], thickness = row[32], platform_width = row[33], platform_thickness = row[34], weight = row[35])
                s.save()
    # Now reload the context data to repair the empty records created by adding small_finds (it is a django bug)
    fill_context()

def debugger(request):
    debug_message = os.path.join(BASE_DIR, 'context.csv')
    return render(request, 'CC/debugger.html',{'debug_message': debug_message})

def populate_context(request):
    fill_context()
    return HttpResponseRedirect('../admin/')


def populate_lithics(request):
    fill_lithics()
    return HttpResponseRedirect('../admin/')


def populate_small_finds(request):
    fill_small_finds()
    return HttpResponseRedirect('../admin/')


def populate_photos(request):
    fill_photos()
    return HttpResponseRedirect('../admin/')

def populate_xyz(request):
    fill_xyz()
    return HttpResponseRedirect('../admin/')


def populate_units(request):
    fill_units()
    return HttpResponseRedirect('../admin/')


def populate_database(request):
    fill_context()
    fill_small_finds()
    fill_lithics()
    fill_photos()
    fill_xyz()
    fill_units()
    return HttpResponseRedirect('../admin/')

def home(request):
    return HttpResponseRedirect('../admin/')

# Untested
def create_context_csv(self, request, queryset):
    response = HttpResponse(content_type='text/csv')  # declare the response type
    response['Content-Disposition'] = 'attachment; filename="cc_context.csv"'  # declare the file name
    writer = unicodecsv.writer(response)  # open a .csv writer
    c = Context()       # create an empty instance of a context object

    context_field_list = c.__dict__.keys()  # fetch the fields names from the instance dictionary
    try:  # try removing the geom field from the list
        context_field_list.remove('geom')
    except ValueError:  # raised if geom field is not in the dictionary list
        pass
    # Replace the geom field with two new fields
    context_field_list.append("point_x")  # add new fields for coordinates of the geom object
    context_field_list.append("point_y")

    writer.writerow(context_field_list)  # write column headers

    for an_object in queryset:  # iterate through the occurrence instances selected in the admin
        # The next line uses string comprehension to build a list of values for each field
        context_dict = an_object.__dict__
        context_dict['point_x'] = an_object.geom.get_x()  # translate the occurrence geom object
        context_dict['point_y'] = an_object.geom.get_y()

        # Next we use the field list to fetch the values from the dictionary.
        # Dictionaries do not have a reliable ordering. This code insures we get the values
        # in the same order as the field list.
        try:  # Try writing values for all keys listed in both the occurrence and biology tables
            writer.writerow([an_object.__dict__.get(k) for k in context_field_list])
        except ObjectDoesNotExist:  # Django specific exception
            writer.writerow([an_object.__dict__.get(k) for k in context_field_list])
        except AttributeError:  # Django specific exception
            writer.writerow([an_object.__dict__.get(k) for k in context_field_list])

    return response

# Untested
def create_lithics_csv(self, request, queryset):
    response = HttpResponse(content_type='text/csv')  # declare the response type
    response['Content-Disposition'] = 'attachment; filename="cc_lithics.csv"'  # declare the file name
    writer = unicodecsv.writer(response)    # open a .csv writer
    l = Lithic()                           # create an empty instance of a context object

    lithic_field_list = l.__dict__.keys()  # fetch the fields names from the instance dictionary

    writer.writerow(lithic_field_list)  # write column headers

    for an_object in queryset:  # iterate through the occurrence instances selected in the admin
        # The next line uses string comprehension to build a list of values for each field
        lithic_dict = an_object.__dict__

        # Next we use the field list to fetch the values from the dictionary.
        # Dictionaries do not have a reliable ordering. This code insures we get the values
        # in the same order as the field list.
        try:  # Try writing values for all keys listed in both the occurrence and biology tables
            writer.writerow([an_object.__dict__.get(k) for k in lithic_field_list])
        except ObjectDoesNotExist:  # Django specific exception
            writer.writerow([an_object.__dict__.get(k) for k in lithic_field_list])
        except AttributeError:  # Django specific exception
            writer.writerow([an_object.__dict__.get(k) for k in lithic_field_list])

    return response

# Untested
def create_small_finds_csv(self, request, queryset):
    response = HttpResponse(content_type='text/csv')  # declare the response type
    response['Content-Disposition'] = 'attachment; filename="cc_small_finds.csv"'  # declare the file name
    writer = unicodecsv.writer(response)    # open a .csv writer
    s = Small_Find()                           # create an empty instance of a context object

    small_find_field_list = s.__dict__.keys()  # fetch the fields names from the instance dictionary

    writer.writerow(small_find_field_list)  # write column headers

    for an_object in queryset:  # iterate through the occurrence instances selected in the admin
        # The next line uses string comprehension to build a list of values for each field
        small_find_dict = an_object.__dict__

        # Next we use the field list to fetch the values from the dictionary.
        # Dictionaries do not have a reliable ordering. This code insures we get the values
        # in the same order as the field list.
        try:  # Try writing values for all keys listed in both the occurrence and biology tables
            writer.writerow([an_object.__dict__.get(k) for k in small_find_field_list])
        except ObjectDoesNotExist:  # Django specific exception
            writer.writerow([an_object.__dict__.get(k) for k in small_find_field_list])
        except AttributeError:  # Django specific exception
            writer.writerow([an_object.__dict__.get(k) for k in small_find_field_list])

    return response
