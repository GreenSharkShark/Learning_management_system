from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user == view.get_object().owner)


class IsOwnerOrReadOnly(BasePermission):
    """
    Пользователь может редактировать свой собственный объект, но только просматривать объекты,
    созданные другими пользователями.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешение чтения разрешено всем
        if request.method in SAFE_METHODS:
            return True

        # Разрешение записи разрешено только владельцу объекта
        return bool(obj.owner == request.user)
