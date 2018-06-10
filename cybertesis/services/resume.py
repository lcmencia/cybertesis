import datetime

from tesis.models import Institution, Faculty, Tesis


class ResumeServices:
    """Servicio para obtener los datos del resumen (los 4 cuadraditos)"""

    def __init__(self):
        self.total_faculty = 0
        self.total_institution = 0
        self.outside_capital_percentage = 0
        self.trending = 'trending_flat'
        self.init_year = 1900
        self.total_tesis_number = 0

    def generate_resume(self):
        total_tesis = Tesis.objects.all()
        # Cuadradito 1
        # Total de tesis en el sitio
        self.total_tesis_number = len(total_tesis)
        # Se obtiene la primera tesis, la ultima de la lista, para sacar el dato desde que año tenemos tesis
        last = total_tesis.reverse()[0]
        self.init_year = last.year
        # Cuadradito 2
        university_list = Institution.objects.all()
        self.total_institution = len(university_list)
        faculty_list = Faculty.objects.all()
        self.total_faculty = len(faculty_list)
        # Cuadradito 3
        outside_central_count = 0
        actual_year = datetime.datetime.now().year
        years_dict = dict()
        for t in total_tesis:
            if t.career.faculty.department_id.department_id not in [18, 11]:
                # No es de Asunción o Central
                outside_central_count += 1
                year_compare = t.year
                if (actual_year - 2) <= year_compare < actual_year:
                    if year_compare in years_dict:
                        years_dict[year_compare] += 1
                    else:
                        years_dict[year_compare] = 1
        self.outside_capital_percentage = (outside_central_count / self.total_tesis_number) * 100
        self.trending = 'trending_flat'
        # En years_dict tenemos un dict de los dos ultimos años por ejemplo {'2017':20, '2016':12}
        # Entonces vemos que se aumento y debemos mostrar la flecha hacia arriba
        last_year = actual_year - 1
        last_last_year = actual_year - 2
        if last_year in years_dict and last_last_year in years_dict:
            if years_dict[last_year] > years_dict[last_last_year]:
                self.trending = 'trending_up'
            elif years_dict[last_year] < years_dict[last_last_year]:
                self.trending = 'trending_down'
