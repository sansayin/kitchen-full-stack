from django.urls import path, include
import asyncio
import json
from datetime import datetime
from typing import AsyncGenerator

from django.http import (
    HttpRequest,
    HttpResponseBase,
    StreamingHttpResponse,
    HttpResponseNotAllowed,
)
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import path
from django.utils.timezone import now

from kitchen_service.notifications import get_async_client, send_notification
from .views import (
    load_image,
    cook_meal,
    cook_status,
    ticket_status,
    board_view,
    refresh_board_view,
)


async def streamed_events(
    event_name: str, request: HttpRequest
) -> AsyncGenerator[str, None]:
    """Listen for events and generate an SSE message for each event"""

    try:
        async with get_async_client().pubsub() as pubsub:
            await pubsub.subscribe(event_name)
            while True:
                msg = await pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=None
                )
                if msg is None:
                    continue
                data = json.loads(msg["data"])
                ctx = data["context"]
                template = data.get("template", "")
                if template == "STOP":
                    break
                elif not template:
                    continue
                ctx["message_time"] = datetime.fromtimestamp(ctx["message_time"])
                # Strip out the newlines, to avoid issues. Clunky, I know, fix this properly later.
                text = render_to_string(template, ctx, request).replace("\n", "")
                yield f"data: {text}\n\n"
    except asyncio.CancelledError:
        # Do any cleanup when the client disconnects
        # Note: this will only be called starting from Django 5.0; until then, there is no cleanup,
        # and you get some spammy 'took too long to shut down and was killed' log messages from Daphne etc.
        raise


def events(request: HttpRequest, event_name: str) -> HttpResponseBase:
    if request.method != "GET":
        return HttpResponseNotAllowed(
            [
                "GET",
            ]
        )
    return StreamingHttpResponse(
        streaming_content=streamed_events(event_name, request),
        content_type="text/event-stream",
    )


def sse(request: HttpRequest) -> HttpResponseBase:
    async def stream(request: HttpRequest) -> AsyncGenerator[str, None]:
        counter = 0
        while True:
            counter += 1
            await asyncio.sleep(5.0)
            yield f"data: <div>{counter}</div>\n\n"

    return StreamingHttpResponse(
        streaming_content=stream(request),
        content_type="text/event-stream",
    )


urlpatterns = [
    path("", board_view, name="board-view"),
    path("cook_meal/<int:ticket>/<str:meal_name>/", cook_meal, name="cook-meal"),
    path("cook_status/<int:ticket>/<str:meal_name>/", cook_status, name="cook-status"),
    path("ticket_status/<int:ticket>", ticket_status, name="ticket-status"),
    path("refresh/", refresh_board_view, name="refresh-board-view"),
    path("load_image/<str:name>", load_image, name="load-image"),
    path("events/<str:event_name>/", events, name="events"),
    path("sse/", sse, name="basic-sse"),
]
