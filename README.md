# Systèmes Multi-Agents Project

_BRILLAND Thomas, GUEDON Arthur_

### Execution du projet

Pour executer le projet en local, lancer le fichier `pw_argumentation.py`, qui contient le code initiant le dialogue entre les deux agents :

```sh
python -m pw_argumentation
```

### Description du modèle

Jusqu'à la partie 9, nous avons suivi les questions et implémenté les fonctions demandées dans le TP, et nous avons donc reproduit une partie du modèle proposé, à deux agents.  
Nous avons ensuite fait des choix différents pour notre modèle final de négociation.

On appellera A1 l'agent qui débute le dialogue, et A2 celui qui répond.

Les deux agents tombent d'accord lorsqu'ils ont _COMMIT_ le même item chacun leur tour. Lorsqu'un agent reçoit un _COMMIT_(item), s'il ne l'a pas déjà fait précédemment, il renvoit le même _COMMIT_(item).  
Au long du dialogue, on stocke les arguments donnés par un agent dans une liste _arguments_given_.

Voici les stratégies que nous avons implémenté :

- A1 commence par _PROPOSE_ son item préféré.
- Lorsqu'A2 reçoit une proposition, il peut :
  - Si l'item est dans les 10% des items préférés, il _ACCEPT_: A1 peut alors _COMMIT_ l'item, les 2 agents sont tombés d'accord.
  - Sinon, il _ASK WHY_ et A1 doit argumenter.
- A1 donne son meilleur argument : il s'agit du critère le plus important pour A1 qui a une valeur supérieure à 4 (Good ou Very Good), comme renvoyé par la fonction _List_supporting_proposal_.
- A2 vérifie s'il peut attaquer l'argument : on suit la méthode donnée dans le TP (comme renvoyé par la fonction _List_attacking_proposal_); sinon il _ACCEPT_ l'item, le dialogue se termine après les deux _COMMIT_
- Lorsque A1 reçoit un contre-argument, il peut :
  - _ARGUE_ son meilleur argument qui n'a pas encore été donné (retour à l'étape précédente)
  - s'il n'en a plus, il _PROPOSE_ son nouvel item préféré (retour à l'étape 2).
  - s'il a déjà argumenté sur tous les items, il _GIVE UP_.
- Si A1 _GIVE UP_, A2 peut directement _COMMIT_ son item préféré, A1 doit répondre par un _COMMIT_ et le dialogue est fini.

### Exemples

Voici deux exemples en se plaçant dans une configuration avec 2 moteurs et 5 critères pour ces moteurs.

![Exemple de dialogue entre deux agents 1](example1.png?raw=true "Exemple 1")

Dans ce premier exemple de dialogue, l'agent 1 propose le moteur ICED et le justifie avec les critères qui sont les plus importants pour lui (DURABILITY puis ENVIRONMENT_IMPACT et PRODUCTION_COST), les deux premiers arguments ne sont pas convaincants pour l'agent 2 qui accepte lorsque l'agent 1 met en avant l'argument PRODUCTION_COST qui est satisfaisant pour lui (GOOD ou VERY GOOD).

![Exemple de dialogue entre deux agents 2](example2.png?raw=true "Exemple 2")

Dans ce deuxième exemple de dialogue, l'agent 1 propose d'abord le moteur E qu'il essaye de justifier avec deux arguments qui ne sont pas satisfaisants pour l'agent 2. Il propose ensuite un deuxième moteur (ICED) que l'agent 2 accepte puisqu'il se situe dans le 10% de ses items préférés.

### Etude statistique

Nous avons étudié l'évolution du nombre de messages échangés en moyenne entre les agents ainsi que le nombre d'échanges se terminants par un GIVE_UP lorsque l'on fait varier deux paramètres: le nombre d'items (ICED, E...) et le nombre de critères (NOISE, CONSUMPTION, ...). Pour réaliser ces statistiques nous avons simulé 1000 dialogues à paramètres fixes et avons effectué une moyenne des deux indicateurs étudiés.

![Influence du nombre d'items](stats_items.png?raw=true "Influence du nombre d'items")

On observe ici que plus il y a d'items différents plus le nombre d'échanges moyens au cours d'un dialogue augmente. Cela s'explique par le fait que l'agent 1 aura tendance à proposer plus d'items lorsque le second agent n'est pas convaincu par les arguments proposés. De même on remarque une diminution du nombre d'échanges se terminant par un GIVE UP puisque les agents vont pouvoir se mettre plus facilement d'accord sur un autre item.

![Influence du nombre de critères](stats_criteria.png?raw=true "Influence du nombre de critères")

On observe ici que lorsque le nombre de critères augmente, le nombre de messages échangés en moyenne par dialogue évolue peu, cependant le nombre d'échanges se terminant par une GIVE UP diminue fortement. Cela s'observe car plus il y a de critères différents, plus les agents vont pouvoir trouver un critère sur lequel ils peuvent se mettre d'accord pour dire qu'un moteur est satisfaisant.
