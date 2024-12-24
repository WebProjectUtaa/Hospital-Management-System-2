from sanic import response

def role_required(allowed_roles):
    """
    Kullanıcının belirli rollere sahip olup olmadığını kontrol eden decorator.
    """
    def decorator(func):
        async def wrapper(request, *args, **kwargs):
            user = request.ctx.user
            if not user or "role" not in user:
                return response.json({"error": "Unauthorized access. Role missing."}, status=403)
            if user["role"] not in allowed_roles:
                return response.json({"error": f"Access denied for role: {user['role']}"}, status=403)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
