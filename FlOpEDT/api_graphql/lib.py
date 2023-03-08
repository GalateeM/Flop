from graphql_relay import from_global_id

def assign_value_to_foreign_key (params, fk, type_fk, mutation_name):
    """ Pour affecter des valeurs à des arguments de type ForeignKey dans les mutations
    """
    if params.get(fk, None):
        id_fk = from_global_id(params[fk])[1]
        try:
            params[fk] = type_fk.objects.get(id=id_fk)
        except type_fk.DoesNotExist:
            if mutation_name == "create":
                params[fk] = None
    else:
        if mutation_name == "create":
            params[fk] = None

def get_manyToManyField_values (params, field, type_field):
    """ Retourne les objets correspondant aux arguments de type ManyToManyField dans les mutations
    """
    field_set = None
    if params.get(field, None):
        field_ids = [ from_global_id(id)[1] for id in params[field] ]
        field_set = type_field.objects.filter(id__in = field_ids)
        del params[field]
    return field_set

def assign_values_to_manyToManyField (model, field, value_to_add):
    """ Pour affecter des valeurs à des arguments de type ManyToMany dans les mutations
    """
    if value_to_add != None and len(value_to_add) > 0:
        getattr(model, field).clear()
        getattr(model, field).add(*value_to_add)
        model.save()