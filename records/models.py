from django.db import models


class ProductionUnit(models.Model):
    """
    Класс производственных единиц от Предприятия до Детали Оборудования
    """
    plant = models.ForeignKey('self', blank=True, null=True,
                              related_name='parts', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        if self.plant is None:
            plant_name = '\\'
        else:
            plant_name = self.plant
        return '{0} - {1}'.format(plant_name, self.name)

    class Meta:
        ordering = ['plant_id', 'name']
        verbose_name = 'оборудование'
        verbose_name_plural = 'оборудование'

    def unit_tree(self):
        """
        Метод строит дерево подчиненных объектов
        """
        def get_knot_dict(input_set):
            res = {}
            for unit in input_set:
                if unit.plant_id in res:
                    res[unit.plant_id].append(unit)
                else:
                    res[unit.plant_id] = [unit]
            return res

        def get_tree(knot_dict, tree, ident=0, node=None):
            if node:
                tree.append((node, ident))
            ident += 1
            for branch_object in knot_dict[node.id if node else None]:
                if branch_object.id in knot_dict:
                    get_tree(knot_dict, tree, ident, branch_object)
                else:
                    tree.append((branch_object, ident))

        units = ProductionUnit.objects.all()
        tree = []
        knot_dict = get_knot_dict(units)
        get_tree(knot_dict, tree, 0, self)
        return tree
