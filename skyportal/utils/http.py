def serialize_requests_request(request):
    return {
        'headers': dict(request.headers),
        'body': request.body.decode(),
        'url': request.url,
        'method': request.method,
    }


def serialize_requests_response(response):
    return {
        'headers': dict(response.headers),
        'content': response.text,
        'cookies': response.cookies.get_dict(),
        'elapsed': response.elapsed.total_seconds(),
        'status_code': response.status_code,
        'ok': response.ok,
    }


def serialize_tornado_request(handler):
    return {
        'headers': dict(handler.request.headers),
        'body': handler.request.body.decode(),
        'url': handler.request.uri,
        'method': handler.request.method,
    }
