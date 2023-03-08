from graphql_relay import from_global_id

def assign_value_to_foreign_key (params, fk, type_fk, mutation_name):
    """ Pour les arguments de type ForeignKey dans les mutations
    """
    if params.get(fk, None):
        id_fk = from_global_id(params[fk])[1]
        params[fk] = type_fk.objects.get(id=id_fk)
    else:
        if mutation_name == "create":
            params[fk] = None