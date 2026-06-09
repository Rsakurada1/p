from django.http import JsonResponse


def health_check(request):
    return JsonResponse({
        "status": "ok",
        "message": "Django API is running",
    })


def task_list(request):
    return JsonResponse({
        "tasks": [
            {
                "id": 1,
                "title": "Learn Django",
                "completed": False,
            },
            {
                "id": 2,
                "title": "Create simple API",
                "completed": False,
            },
        ],
    })
