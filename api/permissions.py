from rest_framework import permissions 

from structure.models import *



class IsUserAllowed(permissions.BasePermission):


    def has_permission(self, request, view):

        if (request.user.is_anonymous) or (not request.user.is_active):
            return False

        elif request.user.is_authenticated:
            return True

        return False


    def has_object_permission(self, request, view, obj):


        #this is a longer condition which basically tries to see if
        is_related = self.has_permission_over_obj(request, obj)

        if is_related:
            return True

        return False

        

    def has_permission_over_obj(self, request, obj) -> bool:

        """
            This function verifies if the user requesting the operation over the object 
            can do it or not. 

            This takes into account if the user is authenticated and if the user has permissions
            over the object, for that it looks into the Permission table.
        """
        
        if request.user.is_authenticated:

            #get all the permissions a user has with granted status
            p = Permission.objects.filter(user = request.user).filter(granted = True)
            #print("user with permissions: ", p)


            #if the user is doing something over himself it's okey
            if isinstance(obj, User):
                return obj == request.user 

            elif isinstance(obj, Org):
                org_permissions = p.filter(org = obj).filter(crop__isnull = True)
                print(org_permissions)
                return self.is_allowed(request.method, org_permissions)

            elif isinstance(obj, Crop):
                #get the permissions the user has over the crop
                crop_permissions = p.filter(crop = obj)
                return self.is_allowed(request.method, crop_permissions)

            elif isinstance(obj, (Condition, Measurement, Actuator)):
                #get the permissions the user has over the crop 
                crop_permissions = p.filter(crop = obj.crop)
                return self.is_allowed(request.method, crop_permissions)
                
            else:
                return False

        else:
            return False


    def is_allowed(self, method, permission_set) -> bool:

        """ Checks if the given permission_set allows the execution of the requested method """

        if (permission_set == []) or (permission_set == None):
            return False

        permission_assign       = (permission_set.filter(permission_type__in = ['assign',]).count() >= 1)
        permission_view         = (permission_set.filter(permission_type__in = ['view',]).count() >= 1)
        permission_add          = (permission_set.filter(permission_type__in = ['add',]).count() >= 1)
        permission_delete       = (permission_set.filter(permission_type__in = ['delete',]).count() >= 1)
        permission_edit_control = (permission_set.filter(permission_type__in = ['edit', 'control']).count() >= 1)

        print(permission_set.filter(permission_type__in = ['edit', 'control']).count()>=1)
        print(method)

        # if he has the assign permission_set then he is boss
        if permission_assign:
            return True

        elif permission_view and (method in permissions.SAFE_METHODS):
            return True

        elif permission_add and (method in permissions.SAFE_METHODS + ('POST',)):
            return True

        elif permission_delete and (method in permissions.SAFE_METHODS + ('DELETE',)):
            return True

        elif permission_edit_control and (method in permissions.SAFE_METHODS + ('PATCH', 'PUT',)):
            print("HAS PERMISSION")
            return True

        else:
            return False


    def is_first_time(self, method, permission_set) -> bool:

        """ Figures out if this is the first time of the user creating an Organization, Crop, Actuator, or Measurement """

        pass




