import datetime

from tesis.models import Tesis, SubCategory


class TesisServices:

    def __init__(self):
        self.LIMIT = 10
        self.total_tesis = 0
        self.trending = 'trending_flat'
        self.tesis_list = []
        self.top_sub_categories = {}
        self.top_categories = {}

    def generate_tesis_resume(self):
        # Se obtiene la cantidad total de tesis
        self.tesis_list = Tesis.objects.all()
        self.total_tesis = len(self.tesis_list)

        # Se obtienen todas la categorías y cada categoría se le da un valor de 0
        sub_category_list = SubCategory.objects.all()
        sub_category_values = {}
        for sc in sub_category_list:
            sub_category_values[sc.sub_category_name] = 0

        # Se buscan las tesis que fueron rankeadas y total de votación
        for tesis in self.tesis_list.all():
            # total de votación para esa tesis
            total_ranking = len(tesis.tesisranking_set.all())
            # cada tesis puede tener más de una sub-categoría
            for s in tesis.sub_category.all():
                # A cada sub-categoría se suma la cantidad de votación que tuvo la tesis
                sub_category_values[s.sub_category_name] += total_ranking

        # Se ordena la lista de sub-categorías según la cantidad de votación, de mayor a menor
        self.top_sub_categories = [{k: sub_category_values[k]} for k in
                                   sorted(sub_category_values, key=sub_category_values.get, reverse=True)][:self.LIMIT]
        categories_list = []
        names_list = []
        # Se buscan las categorías asociadas a cada sub-categoría, y se agregan a la lista de ranking
        for sc in self.top_sub_categories:
            sub_categories = SubCategory.objects.filter(sub_category_name=list(sc.keys())[0])
            for subc in sub_categories.all():
                for c in subc.categories.all():
                    if c.category_name not in names_list:
                        names_list.append(c.category_name)
                        categories_list.append({'category_name': c.category_name, 'id': c.id,
                                                'category_icon': c.category_fa_icon})
        self.top_categories = categories_list

        self.trending = 'trending_flat'
        actual_year = datetime.datetime.now().year
        years_dict = dict()
        for full in self.tesis_list:
            if full.career.faculty.department_id.department_id not in [18, 11]:
                year_compare = full.year
                if (actual_year - 2) <= year_compare < actual_year:
                    if year_compare in years_dict:
                        years_dict[year_compare] += 1
                    else:
                        years_dict[year_compare] = 1
        # En years_dict tenemos un dict de los dos ultimos años por ejemplo {'2017':20, '2016':12}
        # Entonces vemos que se aumento y debemos mostrar la flecha hacia arriba
        last_year = actual_year - 1
        last_last_year = actual_year - 2
        if last_year in years_dict and last_last_year in years_dict:
            if years_dict[last_year] > years_dict[last_last_year]:
                self.trending = 'trending_up'
            elif years_dict[last_year] < years_dict[last_last_year]:
                self.trending = 'trending_down'

    @classmethod
    def get_by_id(cls, tesis_id):
        tesis_data = {}
        try:
            tesis = Tesis.objects.get(id=tesis_id)
            if tesis:
                tesis_data['title'] = tesis.title
                tesis_data['career_name'] = tesis.career.name
                tesis_data['postgraduate'] = tesis.career.postgraduate
                tesis_data['institution'] = tesis.career.faculty.institution.name
                tesis_data['logo'] = tesis.career.faculty.institution.logo
                tesis_data['faculty'] = tesis.career.faculty.name
                tesis_data['place'] = tesis.career.faculty.department_id.department_name
                tesis_data['url'] = tesis.url
                tesis_data['format'] = tesis.format
                tesis_data['year'] = tesis.year
                tesis_data['type'] = tesis.tesis_type
                tesis_data['add_date'] = tesis.added_date
                tesis_data['description'] = tesis.description
                tutors = []
                for tutor in tesis.tutor.all()[:2]:
                    tutors.append(tutor.name)
                tesis_data['tutor1'] = tutors[0] if tutors else ''
                tesis_data['tutor2'] = tutors[1] if len(tutors) >= 2 else ''
                authors = []
                for author in tesis.author.all()[:2]:
                    authors.append(author.name)
                tesis_data['authors'] = ', '.join(authors)
        except Exception as e:
            return None
        return tesis_data
