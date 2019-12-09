import cv2
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
profil_cascade = cv2.CascadeClassifier("haarcascade_profileface.xml")
cap =cv2.VideoCapture(0)                                                                                #lire image webcam
width=int(cap.get(3))                                                                                   #determine largeur image
marge=70

class itemgetter():
    __slots__ = ('_items', '_call')
    def __init__(self, item, *items):
        if not items:
            self._items = (item,)
            def func(obj):
                return obj[item]
            self._call = func
        else:
            self._items = items = (item,) + items
            def func(obj):
                return tuple(obj[i] for i in items)
            self._call = func
    def __call__(self, obj):
        return self._call(obj)
    def __repr__(self):
        return '%s.%s(%s)' % (self.__class__.__module__,
                              self.__class__.__name__,
                              ', '.join(map(repr, self._items)))
    def __reduce__(self):
        return self.__class__, self._items


while True:
    ret, frame=cap.read()                                                                               #afficher image webcam
    tab_face=[]
    tickmark=cv2.getTickCount()                                                                         #prend des mesures de temps
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                                                        #passer image en noir et blanc

    face=face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)                           #fonction detecter visage
    for x, y, w, h in face:                                                                             #coordonées du rectangle de l'objet
        tab_face.append([x, y, x+w, y+h])                                                               #ajout a la liste tab_face

    face=profil_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)                           #fonction detecter visage
    for x, y, w, h in face:                                                                             #coordonées du rectangle de l'objet
        tab_face.append([x, y, x+w, y+h])                                                               #ajout a la liste tab_face

    gray2=cv2.flip(gray, 1)                                                                             #retourne l'image pour avoir profil inversé
    face=profil_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)                           #fonction detecter visage
    for x, y, w, h in face:                                                                             #coordonées du rectangle de l'objet
        tab_face.append([width-x, y, width-(x+w), y+h])                                                 #ajout a la liste tab_face

    tab_face=sorted(tab_face, key=itemgetter(0, 1))                                                     #trier le tableau
    index=0
    for x, y, x2, y2 in tab_face:                                                                       #afficher les rectangles
        if not index or (x-tab_face[index-1][0]>marge or y-tab_face[index-1][1]>marge):                 #affiche que si rectangle a cote inferieur a 70p
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)
        index+=1
        
    if cv2.waitKey(1)==ord('q'):                                                                        #quitter le programme
        break
    fps=cv2.getTickFrequency()/(cv2.getTickCount()-tickmark)                                            #deuxieme mesure de temps --> fps
    cv2.putText(frame, "FPS: {:05.2f}".format(fps), (10,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0),2)    #afficher le nbr de fps
    cv2.imshow('video', frame)                                                                          # afficger image avec rectangles
cap.release()                                                                                           #libérer les ressources
cv2.destroyAllWindows()                                                                                 #détruit toutes les fenètres
