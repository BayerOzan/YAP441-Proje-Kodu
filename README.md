# YAP441-Projesi (2025)
## İçerikler
Bu okuma yazısında YAP441 dersi içerisinde oluşturulmuş olan proje hakkında bilgiler verilmiştir.

Proje içerisinde incelenen problem, problem için düşünülen çözüm, bu çözüm için oluşturulan yöntemler ve bu yöntemlerin kodları hakkında bilgiler verilmiştir.

## Proje Problemi
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

Algoritma kontrolü hücre hücre gittiğinden ve doğrulama kodunun uzunluğundan Algoritma üzerinde büyük bir yavaşlama gözlemlenmektedir.
### Yöntem 3
Bu yöntem için 2. yöntemde oluşturulan algoritmanın daha hızlı çalışmasını sağlamaktı. Bunu gerçekleştirirken algoritma içerisinde skor açısından kayıplar gerçekleştirilmiştir. 
Ancak bu kayıplar elde edilen hız kazancına karşın daha düşüktür

A* algoritması içerisinde sadece tek bir seferlik kuyruk kovalama doğrulaması gerçekleştirilmektedir.

Ayrıca oluşabilecek sonsuz döngüler de azaltılmıştır. Bu durumlarda ancak yılanın hareketlerini tahmin etmek oldukça zordur.

### Yöntem 4

Proje sonrası üretilen en son ve en gelişmiş yöntemdir

Bu yöntemde yılanın A* algoritması bir hareket yönü vermek yerine bir hareket yolu vermektedir. Hareket yolu alındıktan sonra, A* algoritması yol gidilene kadar tekrar çağırılmamaktadır.

A* algoritmasında döngü gerçekleştirilmemesi için 

Bu yöntem oyunun bitimine kadar ilerleyebildiği için, oyunun bitiş koşulu eklenmiştir. Bitiş koşulu meyveyede yeniden düzenlenen hareket fonksiyonunun içindedir.

Güncellenen meyve fonksiyonunda çeşitli özellikler eklenmiştir:

1- Eski fonksiyonu kaldırılmıştır.

2- Engeli bulunan bütün hücreleri giriş olarak almaktadır.

3- Oyun haritasının haritasını çıkarmaktadır.

4- Oyun haritasında bulunan bütün engelli hücreleri çıkardıktan sonra bir set elde edilmektedir.

5- Bu setten rastgere bir hücre seçilip bu hücre meyvenin gideceği konumu belirlemektedir.

6- Eğer seçilebilecek herhangi bir hücre yok ise oyun bitmiş olarak kabul edilir çünkü meyvenin gidebileceği başka bir hücre yoktur.

Yapılan değişiklikler sayesinde oyunun hızı artırılmıştır. Oyun skorunda yüksek bir artış gözlemlenmektedir ve oyunların büyük bir kısmı artık bir kazanç ile bitmektedir.

Kazanılmayan oyunlar, meyvenin rastgere hareketlerinden veya hücre kısıtlamasından kaynaklanmaktadır. Kayıp edildiğinde bile yılan yüksek bir skor elde edebilmektedir.

Kuyruk kovalama fonksiyonu artık A* algoritmasını çağırmamaktadır. Bu algoritma çağırıldığında bir hamiltonian döngüsüne benzer bir algoritma çağırılmaktadır. (yön öncelikleri: olarak sol -> aşağı -> yukarı -> sağ)

### Kodlar
Yazılmış olan bütün yöntemlerin kodları Bu sayfada mevcuttur.
