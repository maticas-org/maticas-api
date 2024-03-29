from rest_framework import permissions 
from structure.models import *


#======================================================================#
#                   Custom Permissions Classes
#======================================================================#

class CustomListPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """
            This method is first executed, and if there is a need to get an object 
            from the database and do something with it, it passes over to 
            'has_object_permission' method
        """
        
        if request.user.is_authenticated:
            print(f"user {request.user} authenticated, checking ...")
            return self.has_permission_for_action(request, view)

        elif request.user.is_anonymous or not request.user.is_active:
            print(f"user {request.user} is anonymous or inactive")
            return False

        return False


    def has_object_permission(self, request, view, obj):
        return False;

    def has_permission_for_action(self, request, view):

        # get the pertinent permissions the user has for executing actions
        # on this model
        permissions = self.get_permission_set_for_actions(request.user, view)

        # If there are permissions, check if the requested method is possible
        if permissions.exists():
            return self.is_allowed(request.method, permissions)
        else:
            return False

    def get_permission_set_for_actions(self, user, view):
            
        crop_id = view.kwargs.get('crop_id')
        return Permission.objects.filter(user = user, crop = crop_id, crop__isnull = False, granted = True)

    def is_allowed(self, method, permission_set) -> bool:

        if not permission_set:
            print("not allowed, there are no permissions")
            return False

        allowed_methods = {
            'GET': 'view',
        }

        required_permission_type = allowed_methods.get(method)
        print(f"required permission type: {required_permission_type}")
        print(f"permission set: {permission_set.filter(permission_type=required_permission_type)}")

        if required_permission_type:
            return permission_set.filter(permission_type=required_permission_type).exists()
        else:
            print("not allowed, unsupported action")
            return False

    


class CustomPermissionBaseClass(permissions.BasePermission):


    def has_permission(self, request, view):
        """
            This method is first executed, and if there is a need to get an object 
            from the database and do something with it, it passes over to 
            'has_object_permission' method
        """
        
        if request.user.is_authenticated:
            print(f"user {request.user} authenticated, checking ...")
            return self.has_permission_for_action(request, view)

        elif request.user.is_anonymous or not request.user.is_active:
            print(f"user {request.user} is anonymous or inactive")
            return False


        return False


    def has_object_permission(self, request, view, obj):
        """
            This is called when dealing with GET, UPDATE, PATCH, or DELETE methods
            never with POST requests because the object does not exist.
        """
        return self.has_permission_for_action(request, view)

    def get_org_id(self, view):
        return view.kwargs.get('pk')

    def get_permission_set_for_actions(self, user, view):

        org_id = self.get_org_id(view)
        return Permission.objects.filter(user = user, crop__isnull = True, org = org_id, granted = True)

    def has_permission_for_action(self, request, view):

        # get the pertinent permissions the user has for executing actions
        # on this model
        permissions = self.get_permission_set_for_actions(request.user)

        # If there are permissions, check if the requested method is possible
        if permissions.exists():
            return self.is_allowed(request.method, permissions)
        else:
            return False


    def is_allowed(self, method, permission_set) -> bool:
        """ Checks if the given permission_set allows the execution of the requested action """

        if not permission_set:
            print("not allowed, there are no permissions")
            return False

        allowed_methods = {
            'GET': 'view',
            'POST': 'add',
            'DELETE': 'delete',
            'PUT': 'edit',
            'PATCH': 'edit',
        }

        required_permission_type = allowed_methods.get(method)
        print(f"required permission type: {required_permission_type}")
        print(f"permission set: {permission_set.filter(permission_type=required_permission_type)}")

        if required_permission_type:
            return permission_set.filter(permission_type=required_permission_type).exists()
        else:
            print("not allowed, unsupported action")
            return False


#======================================================================#
#                           Org permissions
#======================================================================#


class OrgPermission(CustomPermissionBaseClass):

    def can_post(self, user):

        #if the user already has some permissions over some organization
        #then the user won't be allowed to create a new org, because 
        #one user can only have one org.
        permissions = Permission.objects.filter(user = user, crop__isnull = True)
        print(f"checking if {user} can post... permissions: {permissions}, can post: {permissions.count() == 0}")

        return permissions.count() == 0


    def has_permission_for_action(self, request, view):

        if request.method == 'POST':
            return self.can_post(request.user)

        else:

            org_permissions = self.get_permission_set_for_actions(request.user, view)

            #if there are permissions then check if the requested action 
            #is possible 
            if org_permissions.exists():
                return self.is_allowed(request.method, org_permissions)
            else:
                return False







#======================================================================#
#                           Crop permissions
#======================================================================#


class CropPermission(CustomPermissionBaseClass):

    def can_post(self, user):

        #if the user already has add permissions over the org they belong to
        #then the user would be allowed to create a new crop
        permissions = Permission.objects.filter(user = user, crop__isnull = True, permission_type = 'add', granted = True)
        print(f"checking if {user} can post... permissions: {permissions}")

        return permissions.count() == 1


    def get_org_id(self, view):
        crop_id = view.kwargs.get('pk')
        
        if crop_id:
            try:
                crop = Crop.objects.get(id = crop_id)
                return crop.org

            except Crop.DoesNotExist:
                return None
        return None

    def has_permission_for_action(self, request, view):

        if request.method == 'POST':
            return self.can_post(request.user)

        else:
            org_permissions = self.get_permission_set_for_actions(request.user, view)

            #if there are permissions then check if the requested action 
            #is possible 
            if org_permissions.exists():
                return self.is_allowed(request.method, org_permissions)
            else:
                return False



#======================================================================#
#                           Actuator permissions
#======================================================================#


class ActuatorPermission(CustomPermissionBaseClass):

    def can_post(self, user, view):

        #get the crop id from the request
        crop_id = view.request.data.get('crop')

        if crop_id:

            #if the user has 'add' permissions over the crop they want to add
            #an actuator to, then they can post
            permissions = Permission.objects.filter(user = user, crop = crop_id, permission_type = 'add', granted = True)
            print(f"checking if {user} can post... permissions: {permissions} over crop {crop_id}")

            return permissions.count() == 1

        return False


    def get_org_id(self, view):

        actuator_id = view.kwargs.get('pk')
        
        if actuator_id:
            try:
                crop = Actuator.objects.get(id = actuator_id).crop
                return crop.org

            except Crop.DoesNotExist:
                return None
        return None


    def get_permission_set_for_actions(self, user, view):

        actuator_id = view.kwargs.get('pk')
        org_id = self.get_org_id(view)

        if actuator_id:
            try:
                crop = Actuator.objects.get(id = actuator_id).crop
                return Permission.objects.filter(user = user, crop = crop, org = org_id, granted = True)

            except Crop.DoesNotExist:
                return None

        return None

    def has_permission_for_action(self, request, view):

        if request.method == 'POST':
            return self.can_post(request.user, view)

        else:

            #get the permissions the user has over the crop 
            #they want to add/mod/del an actuator to
            permissions = self.get_permission_set_for_actions(request.user, view)

            #if there are permissions then check if the requested action 
            #is possible 
            if permissions.exists():
                return self.is_allowed(request.method, permissions)
            else:
                return False


#======================================================================#
#                           Conditions permissions
#======================================================================#


class ConditionPermission(CustomPermissionBaseClass):

    def can_post(self, user, view):
        
        #get the crop id from the request
        crop_id = view.request.data.get('crop')

        if crop_id:
                
                #if the user has 'add' permissions over the crop they want to add
                #a condition to, then they can post
                permissions = Permission.objects.filter(user = user, crop = crop_id, permission_type = 'add', granted = True)
                print(f"checking if {user} can post... permissions: {permissions} over crop {crop_id}")
    
                return permissions.count() == 1
        
        return False

        
    def get_org_id(self, view):
        
        #get the condition id from the request
        condition_id = view.kwargs.get('pk')

        if condition_id:

            try:
                condition = Condition.objects.get(id = condition_id)
                return condition.crop.org

            except Condition.DoesNotExist:
                return None 

        return None 

    def get_permission_set_for_actions(self, user, view):
        
        #get the condition id from the request
        condition_id = view.kwargs.get('pk')

        if condition_id:
            try:
                condition = Condition.objects.get(id = condition_id)
                return Permission.objects.filter(user = user, crop = condition.crop, granted = True)

            except Condition.DoesNotExist:
                return None
        
        return None

    def has_permission_for_action(self, request, view):

        if request.method == 'POST':
            return self.can_post(request.user, view)

        else:

            #get the permissions the user has over the crop 
            #they want to add/mod/del condition to
            permissions = self.get_permission_set_for_actions(request.user, view)

            #get the org id from the request
            org_id = self.get_org_id(view)  
            
            #Ensure the user is trying to add a crop to the org they belong to
            if org_id and permissions:
                permissions = permissions.filter(org = org_id)
            else:
                return False

            #if there are permissions then check if the requested action 
            #is possible 
            if permissions.exists():
                return self.is_allowed(request.method, permissions)
            else:
                return False



#======================================================================#
#                           Measurement permissions
#======================================================================#


class MeasurementPermission(CustomPermissionBaseClass):

    def can_post(self, user, view):
        print("-"*10) 
        print(view.request.user, view.request.auth)

        #get the crop id from the request
        if isinstance(view.request.data, list):
            crop_ids = [individual_request.get('crop') for individual_request in view.request.data]
            all_permissions = [] 

            print("checking if user can post multiple measurements...")

            for crop_id in crop_ids:
                permissions = Permission.objects.filter(user = user, crop = crop_id, permission_type = 'add', granted = True)
                all_permissions.append(permissions.count() == 1)

            print(f"all permissions: {all_permissions}, can post: {all(all_permissions)}")
            return all(all_permissions)
        else:
            crop_id = view.request.data.get('crop')

            if crop_id:
                #if the user has 'add' permissions over the crop they want to add
                #a condition to, then they can post
                permissions = Permission.objects.filter(user = user, crop = crop_id, permission_type = 'add', granted = True)
                print(f"checking if {user} can post... permissions: {permissions} over crop {crop_id}")
    
                return permissions.count() == 1

    @staticmethod
    def can_post_from_data(user, data):
        print("-"*10) 
        print(user, data)

        #get the crop id from the request
        if isinstance(data, list):
            crop_ids = [individual_request.get('crop') for individual_request in data]
            all_permissions = [] 

            print("checking if user can post multiple measurements...")

            for crop_id in crop_ids:
                permissions = Permission.objects.filter(user = user, crop = crop_id, permission_type = 'add', granted = True)
                all_permissions.append(permissions.count() == 1)

            print(f"all permissions: {all_permissions}, can post: {all(all_permissions)}")
            return all(all_permissions)
        else:
            crop_id = data.get('crop')

            if crop_id:
                #if the user has 'add' permissions over the crop they want to add
                #a condition to, then they can post
                permissions = Permission.objects.filter(user = user, crop = crop_id, permission_type = 'add', granted = True)
                print(f"checking if {user} can post... permissions: {permissions} over crop {crop_id}")
    
                return permissions.count() == 1

        
    def get_org_id(self, view):
        
        #get the measurement id from the request
        measurement_id = view.kwargs.get('pk')

        if measurement_id:

            try:
                measurement = Measurement.objects.get(id = measurement_id)
                return measurement.crop.org

            except measurement.DoesNotExist:
                return None 

        return None 

    def get_permission_set_for_actions(self, user, view):
        
        #get the condition id from the request
        measurement_id = view.kwargs.get('pk')

        if measurement_id:
            try:
                measurement = Measurement.objects.get(id = measurement_id)
                return Permission.objects.filter(user = user, crop = measurement.crop, granted = True)

            except Condition.DoesNotExist:
                return None
        
        return None

    def has_permission_for_action(self, request, view):

        if request.method == 'POST':
            return self.can_post(request.user, view)

        else:

            #get the permissions the user has over the crop 
            #they want to add/mod/del condition to
            permissions = self.get_permission_set_for_actions(request.user, view)

            #get the org id from the request
            org_id = self.get_org_id(view)  
            
            #Ensure the user is trying to add a crop to the org they belong to
            if org_id and permissions:
                permissions = permissions.filter(org = org_id)
            else:
                return False

            #if there are permissions then check if the requested action 
            #is possible 
            if permissions.exists():
                return self.is_allowed(request.method, permissions)
            else:
                return False




class MeasurementListPermission(CustomListPermission):

    def get_permission_set_for_actions(self, user, view):
            
        crop_id = view.kwargs.get('crop_id')
        return Permission.objects.filter(user = user, crop = crop_id, crop__isnull = False, granted = True)