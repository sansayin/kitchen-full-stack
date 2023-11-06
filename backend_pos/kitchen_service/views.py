from django.http import HttpResponse
from django.core.cache import caches
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from order_service.models import Menu

from .tasks import task_cook_meal, on_cook_meal_task_success, on_cook_meal_task_failure


def display_ticket(request):
    redis_cache = caches["default"]
    redis_client = redis_cache.client.get_client()
    key_pattern = f"{settings.KAFKA_ORDER_TOPIC}.*"
    matching_keys = redis_client.keys(key_pattern)
    result = {}

    for key in matching_keys:
        full_ticket = key.decode("utf-8")
        ticket = full_ticket.split(f"{settings.KAFKA_ORDER_TOPIC}.")

        fields_and_values = redis_client.hgetall(key)
        if int(fields_and_values[b"total_qty"]) == int(fields_and_values[b"produced"]):
            continue

        decoded_fields_and_values = {
            field.decode("utf-8"): value.decode("utf-8")
            for field, value in fields_and_values.items()
            if field not in [b"total_qty", b"produced", b"meal_id"]
        }

        if decoded_fields_and_values:
            result[int(ticket[1])] = decoded_fields_and_values

    # Sort the result dictionary by its ticket
    sorted_result = dict(sorted(result.items()))

    return render(request, "board/ticket-board.html", {"ticket": sorted_result})


def load_image(request, name):
    obj = get_object_or_404(Menu, item_name=name)
    # Simulate loading an image URL from a database or other source
    image_url = obj.image_url
    # Return the image URL as a response
    response = f'<img style="max-width: 50px; max-height: 50px;"  src="{image_url}" alt="Loaded Image">'
    return HttpResponse(response)


def cook_status(request, ticket, meal_name):
    response = f"<p>Done</p>"
    return HttpResponse(response)


def cook_meal(_, ticket, meal_name):
    task_cook_meal.delay(ticket, meal_name)
    # r = task_cook_meal.apply_async(
    #     args=(ticket, meal_name),
    #     kwargs={"context": {ticket, meal_name}},
    #     link=on_cook_meal_task_success.s(),
    #     link_error=on_cook_meal_task_failure.s(),
    # )
    # print(r)

    response = f"<p>Task Start</p>"
    return HttpResponse(response)


def meal_status(request, tickey, meal_name):
    pass


def ticket_status(request, ticket):
    redis_cache = caches["default"]
    redis_client = redis_cache.client.get_client()
    print(redis_client.hget("ticket.ready", ticket))
    try:
        if int(redis_client.hget("ticket.ready", ticket)) == 1:
            print(f"Ticket:{ticket} is ready")
            response = f"<stong>{ticket} is Ready</strong>"
            return HttpResponse(response)
    except Exception as e:
        pass
    return HttpResponse(status=204)


def get_sorted_tickets():
    redis_cache = caches["default"]
    redis_client = redis_cache.client.get_client()
    key_pattern = f"{settings.KAFKA_ORDER_TOPIC}.*"
    matching_keys = redis_client.keys(key_pattern)
    result = {}

    for key in matching_keys:
        full_ticket = key.decode("utf-8")
        ticket = full_ticket.split(f"{settings.KAFKA_ORDER_TOPIC}.")

        fields_and_values = redis_client.hgetall(key)
        if int(fields_and_values[b"total_qty"]) == int(fields_and_values[b"produced"]):
            continue

        decoded_fields_and_values = {
            field.decode("utf-8"): value.decode("utf-8")
            for field, value in fields_and_values.items()
            if field not in [b"total_qty", b"produced", b"meal_id"]
        }

        if decoded_fields_and_values:
            result[int(ticket[1])] = decoded_fields_and_values
    return dict(sorted(result.items()))


def board_view(request):
    ticket_detail = get_sorted_tickets()
    return render(request, "board/board.html", {"ticket": ticket_detail})


def refresh_board_view(request):
    ticket_detail = get_sorted_tickets()
    new_detail = render(
        request, "board/refresh_board.html", {"ticket": ticket_detail}
    ).content.decode("utf-8")

    return HttpResponse(new_detail)
