# Rapport de test
### Elyne Beaudeau
### *Langage utilisé : Python*

---

###### <u>Lamport</u>

###### 1 - Modifier l'exemple fourni pour que le Process possède une horloge de Lamport
On veut que les processus aient une horloge : variable d'objet "horloge". Quand il envoit un message : On fait "+ 1"; Quand il reçoit il compare l'horloge du msg reçu et le sien : il prend le plus grand et ajoute 1.
Avec le programme initial, on a une horloge à 10 à la fin de l'exécution des processus.

###### 2 - Créez votre Classe de messages qui puisse à la fois intégrer un estampillage et un message (payload). Le message n'est pas forcément un « String ».
Nous créons la classe "MessageWithTime" qui permet de renseigner un message et la valeur d'estampillage. En Python, les variables n'étant pas typée, le message peut être de n'importe quel type.

---

###### <u>Diffusion</u>
###### 1 - Créez une classe de messages de diffusion « BroadcastMessage »
On crée la classe avec  3 variables d'objet : Message, Sender et Time. Elles permettent de savoir qui envoie le message et à quel temps de son horloge.
###### 2 - Ajoutez à la classe Process les méthodes de diffusion et réception associées : (broadcast(Object o) et onBroadcast(BroadcastMessage m))
Dans la méthode de réception, on regarde si l'envoyeur du message est le récepteur, si c'est le cas, on ne traite pas le message (pas d'incrémentation de l'horloge). Pour la méthode broadcast on envoie un message avec l'identifiant du processus qui envoie et son horloge.
###### 3 - Mettez en évidence son bon fonctionnement (la mise à jour correcte de l'horloge sur les Process)
Nous avons maintenant une horloge à 5 pour le processus 1 (celui qui envoie les broadcast) et une horloge à 6 pour les deux autres processus.

---

###### <u>Messages dédiés</u>
###### 1 - Créez une classe de messages dédiés, c'est à dire qu'il ne seront à destination que d'un seul processus
On crée la classe "MessageTo" avec les variables : message, receiver et time.
###### 2 - Ajoutez à la classe Process les méthodes d'envoi et réception associées : (sendTo(Object o, int to) et onReceive(MessageTo m))
Cette fois, on regarde si notre id est le receiver, dans ce cas on traite le message. Dans la méthode d'envoie on dit à quel processus on souhaite envoyé le message.
###### 3 - Mettez en évidence son bon fonctionnement (la mise à jour correcte de l'horloge sur les Process)
Avec P1 qui envoie un message P0, P0 a une horloge à 6, P1 à 5 et P2 à 0.

---

###### <u>Section Critique</u>
###### 1 - Implantez un système de gestion de section critique en anneau au sein de vos Process.
- Le principe consiste à faire tourner un jeton – sans fin – sur l'anneau.
- Le lancement du jeton « Token » doit s'effectuer à la création du dernier Process.

On crée une classe Token, il contient son recépteur et l'horloge de l'émetteur.
###### 2 - Ajouter à la classe Process les méthodes : (onToken() : qui gère le passage du jeton sur l'anneau, request() : qui est bloquante jusqu'à l'obtention du jeton et bloque le jeton sur l'anneau et release() : qui sort de la section critique et libère le jeton sur l'anneau)
On crée également la fonction sendTokenToNext() qui envoie la fonction au suivant.
Pour attendre d'avoir le token dans le request, le processus fait sleep(1) tant qu'il n'a pas reçu le token.
###### 3 - Mettez en évidence son bon fonctionnement (la mise à jour correcte de l'horloge sur les Process)
~~~
P0 Loop: 0
P1 Loop: 0
P2 Loop: 0
P1 Request token
P2 send: Token to 0
P0 Loop: 1
P0 Processes event: Getting Token
P2 Loop: 1
P0 send: Token to 1
P2 Loop: 2
P1 Processes event: Getting Token
P0 Loop: 2
P0 Loop: 3
P1 send: Hey !
P2 Loop: 3
P0 Processes event: Hey !
P1 send: Token to 2
P2 Processes event: Getting Token
P1 Loop: 1
P0 Loop: 4
P1 Request token
P2 send: Token to 0
P0 Processes event: Getting Token
P2 Loop: 4
P2 stopped
P0 send: Token to 1
P1 Processes event: Getting Token
P0 stopped
P1 send: Hey !
P0 Processes event: Hey !
P1 send: Token to 2
P2 Processes event: Getting Token
P1 stopped
P0 end with 8 as time.
P1 end with 7 as time.
P2 end with 8 as time. 
 ~~~ 
Quand on regarde les différents print, on peut voir que le token fonctionne bien, mais on n'a pas d'information précise avec la mise à jour de l'horloge.

---

###### <u>Synchronisation</u>
###### 1 - Créez une méthode de synchronisation dans votre Process.
- Cette méthode est bloquante et doit être appelée par tous les process. Quand tous l’ont invoquée la méthode se débloque et les process passent à la suite.
- A vous de créer votre protocole et la topologie de communication sur laquelle vous vous appuyez (centralisé, anneau, all2all...).
On remarque que ça ressemble à l'exercise sur la barrière.
###### 2 - Ajouter à la classe Process les méthodes : (synchronize() : qui bloque un process jusqu’à ce que tous les autres l’ai également appelée et les autres méthodes nécessaires au fonctionnement de la synchronisation)
Les fonctions créées : requestSynchronized() et onSynchronize().
On ajoute également la variable waitSynchronize au processus.
###### 3 - Mettez en évidence son bon fonctionnement (la mise à jour correcte de l'horloge sur les Process)
Pour mettre en évidence l'attente, on simule manuellement que P0 attend quelques seconde avant d'être synchronisé.
Les processus finissent leurs tâchent avant d'être synchronisée.
~~~~
P0 Loop: 0
P1 Loop: 0
P2 Loop: 0
P1 Request token
P2 send: Token to 0
P0 Loop: 1
P0 Processes event: Getting Token
P2 Loop: 1
P0 send: Token to 1
P2 Loop: 2
P1 Processes event: Getting Token
P0 Loop: 2
P1 send: Hey !
P0 Loop: 3
P2 Loop: 3
P0 Processes event: Hey !
P1 send: Token to 2
P2 Processes event: Getting Token
P1 send: Synchronized request
P0 Processes event: Synchronized
P0 Waiting synchronize
P2 Processes event: Synchronized
P2 Waiting synchronize
P1 Waiting synchronize
P2 send: Token to 0
P0 Processes event: Getting Token
P2 Synchronized !
P2 Loop: 4
P1 Synchronized !
P1 stopped
P0 Synchronized !
P0 stopped
P2 stopped
P0 end with 10 as time.
P1 end with 7 as time.
P2 end with 9 as time.
~~~~
