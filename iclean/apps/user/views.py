from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.user.permissions import IsStaff, IsClientUser, IsCompanyUser, IsClient, IsCompany 
from apps.user.models import Role, User, Client, Company
from apps.user.serializers import RoleSerializer, UserSerializer, ClientSerializer, CompanySerializer


"""
root api
"""
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'notification': reverse('notification-list', request=request, format=format),
        'review': reverse('review-list', request=request, format=format),
        'status': reverse('requeststatus-list', request=request, format=format),
        'request': reverse('request-list', request=request, format=format),
        'service': reverse('service-list', request=request, format=format),
        'role': reverse('role-list', request=request, format=format),
        'user': reverse('user-list', request=request, format=format),
        'client': reverse('client-list', request=request, format=format),
        'company': reverse('company-list', request=request, format=format),
    })


"""
Role model
""" 
class RoleList(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request):
        is_staff = getattr(self.request.user, "is_staff", None)
        if is_staff:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"message": "You don't have permission to create role"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class RoleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


    def update(self, request, *args, **kwargs):
        is_staff = getattr(self.request.user, "is_staff", None)
        if is_staff:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        return Response({"message": "You don't have permission to update role"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def destroy(self, request, *args, **kwargs):
        is_staff = getattr(self.request.user, "is_staff", None)
        if is_staff:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Item has been deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "You don't have permission to delete role"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


"""
User model 
"""
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaff | IsClientUser | IsCompanyUser]
    

    def get_queryset(self):
        is_staff = getattr(self.request.user, "is_staff", None)
        if is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

        
    def create(self, request):
        is_staff = getattr(self.request.user, "is_staff", None)
        if is_staff:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"message": "You don't have permission to create user"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaff | IsClientUser | IsCompanyUser]


    def update(self, request, *args, **kwargs):
        is_staff = getattr(self.request.user, "is_staff", None)
        is_client = getattr(self.request.user, "clients", None)
        is_company = getattr(self.request.user, "companys", None)
        if is_staff or is_client or is_company:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            if is_client and not (serializer.validated_data["email"] == self.request.user.email):
                return Response({"message": "You don't have permission to update user's email address"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            if is_company and not (serializer.validated_data["email"] == self.request.user.email):
                return Response({"message": "You don't have permission to update user's email address"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        return Response({"message": "You don't have permission to update user information"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def destroy(self, request, *args, **kwargs):
        is_staff = getattr(self.request.user, "is_staff", None)
        if is_staff:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "User has been deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "You don't have permission to delete user"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


"""
Client model
"""  
class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsStaff | IsClient | IsCompany]
    
    def get_queryset(self):
        is_staff = getattr(self.request.user, "is_staff", None)
        if is_staff:
            return Client.objects.all()
        return Client.objects.select_related('user').filter(user=self.request.user.id)
    

    def create(self, request):
        is_staff = getattr(self.request.user, "is_staff", None)
        if is_staff:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"message": "You don't have permission to create client"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsStaff | IsClient | IsCompany]

    def update(self, request, *args, **kwargs):
        is_staff = getattr(self.request.user, "is_staff", None)
        is_client = getattr(self.request.user, "clients", None)
        if is_staff or is_client:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            if is_client and not (serializer.validated_data["user"] == self.request.user):
                return Response({"message": "You don't have permission to update client's email address"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        return Response({"message": "You don't have permission to update client information"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def destroy(self, request, *args, **kwargs):
        is_staff = getattr(self.request.user, "is_staff", None)
        is_client = getattr(self.request.user, "clients", None)
        if is_staff or is_client:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Client has been deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "You don't have permission to delete client"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


"""
Company model 
"""
class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsStaff | IsClient | IsCompany]
    
    def get_queryset(self):
        is_staff = getattr(self.request.user, "is_staff", None)
        if is_staff:
            return Company.objects.all()
        return Company.objects.select_related('user').filter(user=self.request.user.id)
 

    def create(self, request):
        is_staff = getattr(self.request.user, "is_staff", None)
        if is_staff:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"message": "You don't have permission to create company"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsStaff | IsClient | IsCompany]

    def update(self, request, *args, **kwargs):
        is_staff = getattr(self.request.user, "is_staff", None)
        is_company = getattr(self.request.user, "companys", None)
        if is_staff or is_company:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            if is_company and not (serializer.validated_data["user"] == self.request.user):
                return Response({"message": "You don't have permission to update company's email address"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        return Response({"message": "You don't have permission to update company information"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def destroy(self, request, *args, **kwargs):
        is_staff = getattr(self.request.user, "is_staff", None)
        is_company = getattr(self.request.user, "companys", None)
        if is_staff or is_company:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Company has been deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "You don't have permission to delete company"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
