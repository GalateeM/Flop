flop-edt/FlOpEDT/base/templates/edt-base.html

---Requetes faites : 
l.43 : var url_module = "{% url 'api:course:module-list' %}";
NB : pas de filtre dept, week, year

l.44 var url_tutor = "{% url 'api:people:tutor-list' %}";
l.45 var url_all_tutors = "{% url 'api:people:tutor_username-list' %}";
NB : pas de filtre dept, week, year

l.46 var url_user_pref = "{% url 'api:user-actual-list' %}";
l.47 var url_user_pref_default = "{% url 'api:user-def-list' %}";
NB : pas de filtre dept et teach-only

l.49 var url_bknews = "{% url 'api:extra:bknews-list' %}";
NB : on ne trouve pas id 

---Requetes non faites : 
l62. var url_unavailable_rooms = "{% url 'api:fetch:unavailablerooms-list' %}";
NB : Pas de model associé à UnavalaibleRoom
