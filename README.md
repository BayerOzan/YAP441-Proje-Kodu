# YAP441-Projesi (2025)
## İçerikler
Bu okuma yazısında Yap441 dersi içerisinde oluşturulmuş olan proje hakkında bilgiler verilmiştir.

Proje içerisinde incelenen problem, problem için düşünülen çözüm, bu çözüm için oluşturulan yöntemler ve bu yöntemlerin kodları hakkında bilgiler verilmiştir.

## Seçilen Problem
YAP441 Projesi üzerinde birçok yapay zeka projesi mevcuttur.
Bu projeler içerisinden Yılan Oyunu Yapay Zeka Aracı Projesi seçilmiştir.
Bu problem içerisinde popüler bir oyun olan Yılan oyunu üzerinde bir yapay zeka aracısı oluşturup oyun içerisindeki maksimum skorun elde edilmesi sağlanmalıdır.
Problemin çözülebilmesi için birçok yöntem üretilmiştir.

## Üretilen Çözümler
Oyun pygame üzerinden üretilmiştir. Oyun üzerinde meyve, yılan ve oyun arayüzü tasarımı bulunmaktadır
Çözümler A* algoritması sonucu yapılmıştır
### Yöntem 1
İlk yöntem en basit mantıkla yapılmıştır.
İlk yöntemde A* algoritması sade bir biçimde üretilmiştir.
A* algoritmasının yalnız kullanılması algoritmanın en hızlı çalışmasını sağlamıştır. 
A* algoritması Yılan ile meyve arasındaki en kısa mesafeyi bulmada kullanılmıştır.
Bu yöntemdeki en büyük sorun, Meyve ile yılan arasındaki yol kapatıldığında algoritmanın çalışmamasıdır.
Algoritma çalışmadığında büyük ihtimalle oyun bitecektir.

### Yöntem 2
A* algoritmasının yanında bir kuyruk kovalama algoritması üretilmiştir.
Bu kuyruk kovalama algoritması A* algoritmasının çalışmadığı durumlarda aktifleşmektedir.
kuyruk kovalama algoritması, basitçe Yılanın kuyruğu için bir A* algoritması gerçekleştirmektedir.
Gerçekleştirilmesi gereken amaç bölümü sadece kuyruk ile değiştirilmiştir.
A* algoritmasının çalışabileceğini kontrol eden bir kuyruk erişim fonksiyonu vardır. Bu kuyruk erişim fonksiyonunu kullanarak, algoritmanın erişilebilirliği tespit edilir. 
Bu algoritmanın içinde yılanın bedeni yol üzerinden simüle edilir. Simüle yılanın kuyruğuna ulaşmımı BFS algoritması ile kontrol edilir.

### Yöntem 3


YAP441 Dersinin projesi için gerekli olan kod mevcuttur.
YAP441 Proje sunum videosunda verildiği gibi yöntemler 3 ayrı kod üzerinde yapılmıştır
