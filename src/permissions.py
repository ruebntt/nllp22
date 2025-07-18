def check_permission(user, action):
    permissions = {
        'admin': ['insert', 'delete', 'search'],
        'user': ['search']
    }
    return action in permissions.get(user.role, [])
