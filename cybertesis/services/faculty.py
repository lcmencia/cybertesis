from tesis.models import Full, Tesis


class FacultyService:
    """
    Objeto para manejar datos relacionados a las facutades
    """

    def __init__(self):
        self.total_tesis = 0
        self.outside_capital_percentage = 0

    def get_all_faculty_info(self):
        total_tesis = Tesis.objects.all()
        self.total_tesis = len(total_tesis)
        outside_central_count = 0
        for t in total_tesis:
            if t.career.faculty.department_id.department_id not in [18, 11]:
                # No es de Asunción o Central
                outside_central_count += 1
        self.outside_capital_percentage = (outside_central_count / self.total_tesis) * 100
