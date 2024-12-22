from sanic import response

def role_required(allowed_roles):
    def decorator(func):
        async def wrapper(request, *args, **kwargs):
            user_role = request.headers.get("Role")
            if not user_role:
                return response.json({"error": "Role header is missing"}, status=403)
            if user_role not in allowed_roles:
                return response.json({"error": f"Access denied for role: {user_role}"}, status=403)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
