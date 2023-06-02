# Description
## Description des fonctionnalités
L'objectif de cette fonctionnalité est de permettre à tous les utilisateurs connectés de réserver une salle. Si un utilisateur est désigné comme responsable de la salle réservée, il recevra une demande de confirmation par e-mail, avec la possibilité de l'accepter ou de la refuser.  L'utilisateur ayant formulé la demande de réservation peut aussi la supprimer.
## Fonctionnalités ajoutées
- Tous les utilisateurs connectés peuvent faire une réservation de salle
  **api/roomreservation/views.py**
  class RoomReservationViewSet(viewsets.ModelViewSet):
  #permission_classes = [IsAdminOrReadOnly]
  serializer_class = serializers.RoomReservationSerializer
  *ligne 2 commentée permettant à tous les utilisateurs de réserver une salle*
- Un responsable peut désormais être attribué à une salle
  **base/models.py**
- Si la salle a un responsable, celui-ci devra valider la dem ande de réservation de salle qui lui aura été envoyée par mail. Sinon, la réservation prend automatiquement effet
- La réservation de salle peut être supprimée par un administrateur
- Une fenêtre modale apparait pour informer que la réservation est confirmée
- Une fenêtre modale apparait pour confirmer si une réservation est refusé
- Une fenêtre modale d'erreur apparait si le lien est erroné ou si la réservation a été supprimé avant la réponse du responsable
- Une fenêtre modale de confirmation apparait lors de la suppression d'une réservation de salle
- Un mail est envoyé au demandeur si la demande de réservation est accepté ou refusé par le responsable de la salle
## Fonctionnalités manquantes/futurs
- Vérification de l'utilisateur lors de la suppression : seuls les utilisateurs admin ou ayant créé la demande peuvent la supprimer
- Amélioration de l'affichage des réservations en attente de validation. Exemple : affichage transparent, bord pointillé
- Interface pour ajouter des responsables aux salles 