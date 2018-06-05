from tesis.models import Tesis, SubCategory


class TesisServices:

    def __init__(self):
        self.LIMIT = 10
        self.total_tesis = 0
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

        # Se buscan las teesis que fueron rankeadas y total de votación
        for tesis in self.tesis_list.all():
            # total de votación para esa tesis
            total_ranking = len(tesis.tesisranking_set.all())
            # cada tesis puede tener más de una sub-categoría
            for s in tesis.sub_category.all():
                # A cada sub-categoría se suma la cantidad de votación que tuvo la tesis
                sub_category_values[s.sub_category_name] += total_ranking

        # Se ordena la lista de sub-categorías según la cantidad de votación, de mayor a menor
        self.top_sub_categories = [{k: sub_category_values[k]} for k in sorted(sub_category_values, key=sub_category_values.get, reverse=True)][:self.LIMIT]
        categories_list = []
        names_list = []
        # Se buscan las cateorías asociadas a cada sub-categoría, y se agregan a la lista de ranking
        for sc in self.top_sub_categories:
            sub_categories = SubCategory.objects.filter(sub_category_name=list(sc.keys())[0])
            for subc in sub_categories.all():
                for c in subc.categories.all():
                    if c.category_name not in names_list:
                        names_list.append(c.category_name)
                        categories_list.append({'category_name': c.category_name,
                                                'category_icon': c.category_fa_icon})
        self.top_categories = categories_list
