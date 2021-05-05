from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.groups.filter(name__in=['general', 'serjant', 'president']) or request.user.is_superuser


class FilterObjPermission(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        else:
            user_group = request.user.groups.filter(name__in=['general', 'president', 'serjant'])
            doc = obj.document_root in ['public', 'private', 'secret', 'top-secret']
            if user_group and doc:
                return True
