# Web services REST

S'applique aux groupes : {{ groups }}

S'applique aux départments : {{ department }}

 Signifie Representational State Transfer
 Il n'est pas
 - un format
 - un protocole
 - un standard
Il est plutot un style d'architecture

## Contraintes
- Style client serveur
- communication **sans état**
	- Le client doit communiquer tt les infos
- mise en cache des réponses aux requètes
	- Surtout get
- Interface uniforme
	- représentation des ressources
	- messages auto descriptif (MIME)

## Représentation
### Représentation
- Données
- Metadata de representation
- somme de controle 

### Format de données
- Type MIME

{{"jambon"}}
{a}
## Points clefs
- Une ressource par service
- Identifier ressources par URI

## Recommandations
- URI pour chaque ressources
- Préferer les urls "logiques" aux urls "physique"
- Utiliser des noms dans les URI et pas des verbes
- GET pour recup des ressources mais pas POST
	- Pour le reste on utilise POST,PUT et DELETE

![UneImage]($domaine/fr/api/ttapp/img/ok_tutors_lunch_break.png/)
