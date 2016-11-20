from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
import json
from models import Place

# Create your views here.
def index(request):
    example = {
        'solved' : 'false',
        'users_completed' : [
        ],
    }
    return HttpResponse(json.dumps(example), content_type='application/json')

def getCompletedPuzzles(request):
    place_qs = Place.objects.filter(completed=True)

    response_data = {}
    completedPuzzles = []
    for place in place_qs:
        temp_obj = {
            'name' : place.name,
            'id' :  place.id,
        }
        completedPuzzles.append(temp_obj)

    response_data['completedPuzzles'] = completedPuzzles

    return JsonResponse(response_data)

def postPuzzleSolved(request):
    response_data = {}
    if request.method != "POST":
        response_data['status'] = "failed: not POST request"
        response_data['score'] = 0
        return JsonResponse(response_data)
    else:
        try:
            puzzle_id = int(request.POST['puzzle_id'])
            username = request.POST['username']
        except Exception:
            response_data['status'] = "failed: invalid POST request"
            response_data['score'] = 0
            return JsonResponse
            
        get_place = get_object_or_404(Place, pk=puzzle_id)
        get_place.addSolver(username)
        get_place.completed = True
        get_place.save()
        score = get_place.getScore()


        response_data['status'] = "success"
        response_data['score'] = score

        return JsonResponse(response_data)


def getPlacePic(request, place_id):
    get_place = get_object_or_404(Place, pk=place_id)
    context = {
        'picture' : "img/" + get_place.picture
    }
    return render(request, 'umdPuzzle/pic.html', context)


def getPlace(request):
    response_data = {}
    if request.GET.get('lat') and request.GET.get('lon'):
        # convert to float
        fLat = float(request.GET.get('lat'))
        fLon = float(request.GET.get('lon'))

        places_qs = Place.objects.all()
        closest_place = None
        min_distance = None

        for place in places_qs:
            curr_dist = place.getDistance(fLat, fLon)
        
            if min_distance == None or curr_dist < min_distance:
                min_distance = curr_dist
                closest_place = place
        if closest_place is not None :
            response_data['distance'] = min_distance

            # get the solvers of the place
            solvers = closest_place.getSolvers()

            response_data['place'] = {
                'id' : closest_place.id,
                'name' : closest_place.name,
                'latitude' : closest_place.latitude,
                'longitude' : closest_place.longitude,
                'pic' : closest_place.picture,
                'completed' : closest_place.completed,
                'solvers' : solvers,
            }
        else:
            response_data['distance'] = "no objects in database"
            response_data['place'] = {}


    else:
        response_data['distance'] = "lat and lon parameters nonexistant"
        response_data['place'] = {}

    return JsonResponse(response_data)
