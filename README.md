# Systèmes Multi-Agents Project

*BRILLAND Thomas, GUEDON Arthur*

Jusqu'à la partie 9, nous avons suivi les questions et implémenté les fonctions demandées dans le TP.  
Nous avons ensuite fait des choix différents pour notre modèle final de négociation.

On appellera A1 l'agent qui débute le dialogue, et A2 celui qui répond.

### Description du modèle
Les deux agents tombent d'accord lorsqu'ils ont *COMMIT* le même item chacun leur tour. Lorsqu'un agent reçoit un *COMMIT*(item), s'il ne l'a pas déjà fait précédemment, il renvoit le même *COMMIT*(item).  
Au long du dialogue, on stocke les arguments donnés par un agent dans une liste *arguments_given*.

Voici les stratégies que nous avons implémenté :
- A1 commence par *PROPOSE* son item préféré.  
- Lorsqu'A2 reçoit une proposition, il peut :  
  - Si l'item est dans les 10% des items préférés, il *ACCEPT*: A1 peut alors *COMMIT* l'item, les 2 agents sont tombés d'accord.
  - Sinon, il *ASK WHY* et A1 doit argumenter.
- Sinon, il *ASK WHY*, et A1 doit argumenter.
- A1 donne son meilleur argument : il s'agit du critère le plus important pour A1 qui a une valeur supérieure à 4 (Good ou Very Good).
- A2 vérifie s'il peut attaquer l'argument : on suit la méthode donnée dans le TP (*List_attacking_proposal*); sinon il *ACCEPT* l'item, le dialogue se termine après les deux *COMMIT*
- Lorsque A1 reçoit un contre-argument, il peut :
  - *ARGUE* son meilleur argument qui n'a pas encore été donné (retour à l'étape précédente)
  - s'il n'en a plus, il *PROPOSE* son nouvel item préféré (retour à l'étape 2). 
  - s'il a déjà argumenté sur tous les items, il *GIVE UP*.
- Si A1 *GIVE UP*, A2 peut directement *COMMIT* son item préféré, A1 doit répondre par un *COMMIT* et le dialogue est fini.