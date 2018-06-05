from tesis.models import Faculty


class FacultyService:
    """
    Objeto para manejar datos relacionados a las facutades
    """

    def __init__(self):
        self.total_faculty = 0
        self.outside_capital_percentage = 0

    def get_all_faculty_info(self):
        faculty_list = Faculty.objects.all()
        # Se obtiene la cantidad de facultades que son fuera de Asunción y Central
        outside_central_count = 0
        for f in faculty_list:
            if f.department_code.department_code not in [0, 11]:
                # No es de Asunción o Central
                outside_central_count += 1
        self.total_faculty = len(faculty_list)
        self.outside_capital_percentage = 100 - ((self.total_faculty - outside_central_count) / self.total_faculty * 100)