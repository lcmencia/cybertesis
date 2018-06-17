from tesis.models import Tesis, SubCategory, TesisRanking, Full

from tesis.constants import ORDER_BY_MOST_RECENT, ORDER_BY_MOST_VALUED


class TesisServices:

    def __init__(self):
        self.LIMIT = 10
        self.top_categories = {}
        self.top_tutors = []

    @classmethod
    def calculate_tesis_rating(cls, rating_list):
        # Se calcula rating la lista de tesis
        rating_total = 0
        for rating in rating_list:
            rating_total += rating.value
        total_vote = len(rating_list)
        return {'stars': 0 if total_vote == 0 else int(round(rating_total / total_vote)),
                'total_vote': total_vote}

    @classmethod
    def generate_tutor_json_list(cls, tutors_name_list, tutors_obj, subcategy_obj):
        tutors_full = []
        for tesis_tutor in tutors_obj:
            tesis_of_tutor = Tesis.objects.filter(tutor__id=tesis_tutor.id).order_by('-year')[:1].all()
            year = tesis_of_tutor[0].year if tesis_of_tutor else ''
            name = tesis_tutor.name
            category = subcategy_obj.categories.all()[0].category_name
            if name not in tutors_name_list:
                tutors_name_list.append(name)
                tutors_full.append({
                    "name": name,
                    "category": category,
                    "year": year
                })
        return tutors_name_list, tutors_full

    def generate_tesis_resume(self):
        # Se obtiene la cantidad total de tesis
        tesis_list = Tesis.objects.all()

        # Se obtienen todas la categorías y cada categoría se le da un valor de 0
        sub_category_list = SubCategory.objects.all()
        sub_category_values = {}
        for sc in sub_category_list:
            sub_category_values[sc.sub_category_name] = 0

        # Se buscan las tesis que fueron rankeadas y total de votación
        for tesis in tesis_list.all():
            # total de votación para esa tesis
            all_ranking = tesis.tesisranking_set.all()
            total_ranking = len(all_ranking) if all_ranking else 0
            # cada tesis puede tener más de una sub-categoría
            for s in tesis.sub_category.all():
                # A cada sub-categoría se suma la cantidad de votación que tuvo la tesis
                sub_category_values[s.sub_category_name] += total_ranking

        # Se ordena la lista de sub-categorías según la cantidad de votación, de mayor a menor
        top_sub_categories = [{k: sub_category_values[k]} for k in
                              sorted(sub_category_values, key=sub_category_values.get, reverse=True)][:self.LIMIT]
        categories_list = []
        names_list = []
        tutors_list = []
        # Se buscan las categorías asociadas a cada sub-categoría, y se agregan a la lista de ranking
        for sc in top_sub_categories:
            sub_categories = SubCategory.objects.filter(sub_category_name=list(sc.keys())[0])
            for subc in sub_categories.all():
                for tesis in subc.tesis_set.all():
                    names_list, tutors = TesisServices.generate_tutor_json_list(tutors_name_list=names_list,
                                                                                tutors_obj=tesis.tutor.all(),
                                                                                subcategy_obj=subc)
                    tutors_list += tutors
                for c in subc.categories.all():
                    if c.category_name not in names_list:
                        names_list.append(c.category_name)
                        categories_list.append({'category_name': c.category_name, 'id': c.id,
                                                'category_icon': c.category_fa_icon})
        self.top_categories = categories_list
        self.top_tutors = tutors_list

    @classmethod
    def get_tesis_rating(cls, tesis_id):
        tesis_rating_list = TesisRanking.objects.filter(tesis_id=tesis_id)
        return cls.calculate_tesis_rating(tesis_rating_list.all())

    @classmethod
    def get_by_id(cls, tesis_id):
        tesis_data = {}
        try:
            tesis = Tesis.objects.get(id=tesis_id)
            if tesis:
                tesis_data['id'] = tesis_id
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
                # Calcular la cantidad de estrellas
                rating_calculated = cls.calculate_tesis_rating(tesis.tesisranking_set.all())
                tesis_data['stars'] = rating_calculated.get('stars', 0)
                tesis_data['total_vote'] = rating_calculated.get('total_vote', 0)
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

    @classmethod
    def get_by_category(cls, category_id, order):
        tesis_all = Tesis.objects.all()
        tesis_id_list = set()
        all_full = None
        if category_id > 0:
            for t in tesis_all:
                # Por cada tesis vemos a que subcategorias esta linkeada
                sub_categories = t.sub_category.all()
                for sc in sub_categories:
                    # Por cada subcategoria vemos a que categoria esta linkeada
                    categories = sc.categories.all()
                    for cat in categories:
                        # Por cada categoria, si la categoria es la filtrada esa tesis se agrega a la lista de ID de tesis
                        if cat.id == category_id:
                            tesis_id_list.add(t.id)
                            break
        if len(tesis_id_list) > 0 and category_id > 0:
            # Si la lista de ID de tesis no esta vacia, mostrar solo esas tesis
            if order == ORDER_BY_MOST_RECENT:
                all_full = Full.objects.filter(pk__in=list(tesis_id_list)).order_by('-year', '-added_date')
            elif order == ORDER_BY_MOST_VALUED:
                all_full = Full.objects.filter(pk__in=list(tesis_id_list)).order_by('-rating', '-year', '-added_date')
        else:
            if order == ORDER_BY_MOST_RECENT:
                all_full = Full.objects.all().order_by('-year', '-added_date')
            elif order == ORDER_BY_MOST_VALUED:
                all_full = Full.objects.all().order_by('-rating', '-year', '-added_date')
        return all_full

    @classmethod
    def search_in_tesis(cls, search_text, all_full):
        total_full = list()
        tutors_full = list()
        for full in all_full:
            # Por cada tesis se iteran sus columnas para ver si la palabra existe
            # Esto puede ser demasiado costoso, por eso la vista de donde se obtienen las tesis
            # no tiene todas las columnas, solo las que podrian ser de interes ej: nombre, facultad, año y otros
            for i in range(0, len(full._meta.fields)):
                key = full._meta.fields[i].attname
                value = str(full.__getattribute__(key)).lower()
                # Si la palabra existe se agrega en los resultados
                if search_text in value:
                    total_full.append(full)
                    full_tesis = Tesis.objects.get(pk=full.id)
                    tutors_name_list = []
                    for ft_sc in full_tesis.sub_category.all():
                        # Teniendo las sub-categorías se puede llegar a los tutores de cada tesis
                        for sc_tesis in ft_sc.tesis_set.all():
                            tutors_name_list, tutors = TesisServices.generate_tutor_json_list(
                                tutors_name_list=tutors_name_list,
                                tutors_obj=sc_tesis.tutor.all(),
                                subcategy_obj=ft_sc)
                            tutors_full += tutors
                    break
        return total_full, tutors_full
