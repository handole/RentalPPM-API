from api.models.master_employee import *
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.master_user import master_user


class MasterEmployee(APIView):
    def get(self, request, format=None):
        m_user = master_user.objects.all()        
        on_list_user = [[m.employee_id_id for m in m_user]][0]        
        m_employee = master_employee.objects.exclude(employee_id__in=on_list_user)
        a=[]
        for p in m_employee:
            b = {'employee_id':p.employee_id,'nama':p.name,'address':p.address,'id_type':p.id_type,
                'id_number':p.id_number,'employee_status':p.employee_status,
                'dob':p.dob,'phone_number':p.phone_number
            }
            a.append(b)  
        return Response(a)