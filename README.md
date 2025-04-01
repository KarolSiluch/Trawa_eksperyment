Jest to program eksperymentalny. Głównym celem było napisanie interaktywnej trawy, ale rozwinęło się to też do przerobienia sposobu interakcji między elementami gry i niższymi warstwami projektu.

Ze względu na swoją prędkość, python raczej nie nadaje się do symulowania dużej ilości obiektów. Samo narysowanie 1000 obiektów na ekranie jest da pythona zbyt wymagające, nie wspominając o dodaniu dodatkowej logiki.
Żeby python wytrzymał, trzeba było obejść sam sposób rysoania. Źdźbła trawy dzielę na powtarzające się grupy, dzięki czemu generując jedną grupę mogę ją narysować w wielu miejscach. Zauważenie powtarzających się wariantów
jest ciężkie a pozwala zaoszczędzić dużo obliczeń.

W praktyce sama symulacja wygląda następująco:
https://youtu.be/S3_GDXF9Amo

Sposób w który jest to zaimplementowany jest na tyle wydajny, że jestem w stanie płynnie symulować nawet 150000 zdziebeł trawy jednocześnie:
https://youtu.be/-LsolTy1QPk.
W każdej z kratek znajduje się dokładnie 1000 zdziebeł trawy.
