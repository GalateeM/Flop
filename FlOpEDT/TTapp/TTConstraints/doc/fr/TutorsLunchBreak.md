A AJOUTER AUTOMATIQUEMENT:

### Paramètres:
- tutors :
- start_time: 
- end_time:
- lunch_length : 

### Description
Cette contrainte garantit que les profs {tutors} aient une pause pour déjeuner (ou autre chose) de {lunch_length} minutes
au moins entre {start_time} et {end_time} les {week_days}.

### Exemple : 
- tutors = [MPH]
- start_time = 12h30
- end_time = 14h
- lunch_length = 60 minutes

Ok:![Situation autorisée](../images/ok_tutors_lunch_break.png), Pas ok : ![Situation interdite](../images/forbidden_tutors_lunch_break.png)