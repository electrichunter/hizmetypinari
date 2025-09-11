Proje: Çok Sektörlü Hizmet Platformu (Kod Adı: Hizmetpınarı)
Bu doküman, Armut.com benzeri, farklı sektörlerdeki hizmet sağlayıcılar ile müşterileri bir araya getiren, SEO odaklı, modern ve ölçeklenebilir bir platformun geliştirme yol haritasını ve teknik dokümantasyonunu içerir.

🚀 1. Proje Vizyonu ve Temel Hedefler
Projenin temel amacı, belirli bir hizmet ve lokasyon ("Ankara boyacı", "İzmir avukat" vb.) için arama yapan kullanıcıları, o bölgedeki en iyi hizmet sağlayıcılarla buluşturmaktır. Sistem, programatik SEO teknikleri kullanarak binlerce dinamik sayfa üretecek ve arama motorlarında organik olarak üst sıralara çıkacaktır.

Ana Özellikler:
Çok Sektörlü Yapı: Boyacılıktan avukatlığa, elektrikçilikten web tasarıma kadar her türlü hizmet kategorisi eklenebilir.

Lokasyon Bazlı Arama: Kullanıcılar şehir ve ilçe bazında hizmet sağlayıcıları filtreleyebilir.

İş ve Teklif Sistemi: Müşteriler iş talepleri oluşturur, hizmet sağlayıcılar bu taleplere teklif verir.

Profil Yönetimi: Hizmet sağlayıcılar kendilerine detaylı profiller (hakkında, portfolyo, hizmet bölgeleri) oluşturabilir.

Puan ve Yorum Sistemi: Tamamlanan işler sonrası müşteriler, sağlayıcılara puan verip yorum yapabilir.

Güvenli ve Denetlenebilir: Yapılan her kritik işlem, hangi kullanıcı tarafından ne zaman yapıldığı bilgisiyle kayıt altına alınır.

🛠️ 2. Teknik Mimarî ve Teknoloji Yığını
Proje, modern yazılım geliştirme prensiplerine uygun olarak ayrık (decoupled) bir mimariyle geliştirilecektir. Bu, backend ve frontend'in tamamen bağımsız olarak geliştirilip ölçeklendirilmesine olanak tanır.

Backend (API Sunucusu): Frontend'in ve gelecekteki mobil uygulamaların veri ihtiyacını karşılayan merkezi beyin.

Dil/Framework: Node.js (NestJS önerilir - TypeScript ile daha düzenli ve ölçeklenebilir bir yapı sunar)

Veritabanı: MySQL 8+

API Türü: RESTful API

Kimlik Doğrulama: JWT (JSON Web Tokens)

Frontend (Web Uygulaması): Kullanıcıların gördüğü ve etkileşime girdiği vitrin.

Framework: React (Next.js önerilir - SSR ve SSG yetenekleri ile mükemmel SEO performansı sağlar)

Styling: Tailwind CSS (Hızlı ve modern arayüzler için)

State Management: React Context API veya Zustand

Deployment (Yayınlama):

Backend: AWS (EC2, RDS), DigitalOcean Droplet veya Heroku

Frontend: Vercel (Next.js için en ideal ve pratik platform)

🗄️ 3. Veritabanı Mimarisi
Veritabanı, MySQL 8+ kullanılarak oluşturulmuştur. Temel prensipler:

Soft Delete: Kayıtlar is_active = false olarak güncellenir, asla fiziksel olarak silinmez.

Audit Log: audit_logs tablosu ve trigger'lar sayesinde kritik tablolardaki tüm INSERT ve UPDATE işlemleri otomatik olarak kaydedilir.

İlişkisel Bütünlük: Foreign key kısıtlamaları ile veri tutarlılığı garanti altına alınır.

Detaylı şema için platform_schema_mysql.sql dosyasına bakınız.

🗺️ 4. Geliştirme Yol Haritası (Yapılacaklar Listesi)
Proje, yönetilebilir aşamalara bölünmüştür. Her aşama, belirli bir fonksiyon setini tamamlamaya odaklanır.

📌 Aşama 1: MVP (Minimum Uygulanabilir Ürün) - Temel Kurulum ve Çekirdek Fonksiyonlar
Bu aşamanın hedefi, sistemin temel iskeletini kurmak ve kullanıcıların hizmetleri/sağlayıcıları görebileceği bir yapı oluşturmaktır.

Backend Görevleri:

[ ] NestJS projesini oluşturma ve temel konfigürasyon (veritabanı bağlantısı, .env dosyası).

[ ] Veritabanı şemasını (platform_schema_mysql.sql) MySQL'e aktarma.

[ ] Kullanıcı Yönetimi (Auth) Modülü:

[ ] POST /auth/register (Yeni kullanıcı kaydı).

[ ] POST /auth/login (Giriş yapma ve JWT oluşturma).

[ ] GET /auth/me (Giriş yapmış kullanıcının bilgilerini döndürme - Auth Guard ile korunacak).

[ ] Genel Veri Modülü:

[ ] GET /categories (Tüm kategorileri listeleme).

[ ] GET /services (Kategoriye veya isme göre hizmetleri listeleme).

[ ] GET /locations (Şehirleri ve ilçeleri listeleme).

[ ] Sağlayıcı (Provider) Modülü:

[ ] GET /providers (Filtreleme: hizmet, şehir, ilçe bazında sağlayıcıları listeleme).

[ ] GET /providers/:id (Tek bir sağlayıcının detaylı profilini getirme).

Frontend Görevleri:

[ ] Next.js projesini oluşturma ve Tailwind CSS entegrasyonu.

[ ] Ana Sayfa: Popüler kategorileri ve hizmetleri gösterme.

[ ] Hizmet Listeleme Sayfası: site.com/hizmetler/[sehir]/[ilce]/[hizmet-slug] yapısında dinamik sayfalar oluşturma. Bu sayfa, backend'den ilgili sağlayıcıları çekecek.

[ ] Sağlayıcı Detay Sayfası: Seçilen sağlayıcının profil bilgilerini gösterme.

[ ] Basit bir kullanıcı kayıt ve giriş formu oluşturma.

📌 Aşama 2: Etkileşim Mekanizması - İş ve Teklif Sistemi
Bu aşamanın hedefi, platformu statik bir listeden, kullanıcıların etkileşime girebildiği bir pazaryerine dönüştürmektir.

Backend Görevleri:

[ ] İş (Job) Modülü (Auth Korumalı):

[ ] POST /jobs (Müşterinin yeni bir iş talebi oluşturması).

[ ] GET /jobs (Müşterinin kendi iş taleplerini listelemesi).

[ ] GET /jobs/open (Sağlayıcının kendi uzmanlık alanı ve bölgesindeki açık işleri görmesi).

[ ] Teklif (Offer) Modülü (Auth Korumalı):

[ ] POST /offers (Sağlayıcının bir işe teklif vermesi).

[ ] GET /jobs/:jobId/offers (Müşterinin kendi işine gelen teklifleri görmesi).

[ ] PATCH /offers/:offerId/accept (Müşterinin bir teklifi kabul etmesi - işin durumu assigned olarak güncellenmeli).

Frontend Görevleri:

[ ] "İş Talebi Oluştur" Formu: Müşteriler için sihirbaz (wizard) tarzı bir form.

[ ] Müşteri Paneli:

[ ] "İş Taleplerim" sayfası.

[ ] İş detayında gelen teklifleri listeleme ve kabul etme butonu.

[ ] Sağlayıcı Paneli:

[ ] "Açık İşler" sayfası.

[ ] İş detayını görme ve teklif verme formu.

📌 Aşama 3: Güven ve Kalite - Yorum ve Profil Geliştirmeleri
Bu aşamanın hedefi, platforma güven mekanizmaları eklemek ve sağlayıcıların kendilerini daha iyi tanıtmalarını sağlamaktır.

Backend Görevleri:

[ ] Yorum (Review) Modülü (Auth Korumalı):

[ ] POST /reviews (Müşterinin, durumu completed olan bir iş için yorum ve puan eklemesi).

[ ] GET /providers/:providerId/reviews (Bir sağlayıcıya yapılmış tüm yorumları listeleme).

[ ] Portfolyo (Portfolio) Modülü (Auth Korumalı):

[ ] Sağlayıcılar için portfolyo yönetimi (CRUD işlemleri).

[ ] Sağlayıcı Profili Geliştirme:

[ ] PATCH /providers/me (Sağlayıcının kendi profilini (bio, hizmet alanları vb.) güncellemesi).

Frontend Görevleri:

[ ] Sağlayıcı profil sayfasında "Yorumlar" ve "Portfolyo" sekmeleri ekleme.

[ ] Müşteri panelinde, tamamlanmış işler için "Yorum Yap" butonu ve formu.

[ ] Sağlayıcı panelinde "Profilimi Düzenle" sayfası ve portfolyo yükleme arayüzü.

📌 Aşama 4: Yönetim ve Optimizasyon - Admin Paneli
Bu aşamanın hedefi, platformun yöneticiler tarafından kontrol edilebilmesini sağlamak ve sistemi daha sağlam hale getirmektir.

Backend Görevleri:

[ ] Admin Modülü (Admin Rol Korumalı):

[ ] Kullanıcıları listeleme, aktif/pasif yapma.

[ ] Hizmet ve kategorileri yönetme (CRUD).

[ ] Sağlayıcı profillerini doğrulama (is_verified alanını güncelleme).

Frontend Görevleri:

[ ] Basit bir Admin Paneli arayüzü oluşturma (Ayrı bir sayfa veya site.com/admin altında).

[ ] Admin panelinde temel yönetim tabloları ve aksiyon butonları.

🔐 5. Güvenlik ve En İyi Pratikler
Audit Log Kullanıcı ID'si: Backend'de her istek işlenmeden önce, JWT'den gelen kullanıcı ID'si bir session değişkeni olarak ayarlanmalıdır. MySQL için: SET @current_user_id = [JWT'den gelen ID];. Bu, trigger'ların işlemi kimin yaptığını bilmesini sağlar.

Çevresel Değişkenler: Veritabanı bilgileri, JWT secret key gibi hassas veriler asla koda yazılmamalı, .env dosyaları ile yönetilmelidir.

Girdi Doğrulama (Input Validation): Backend'e gelen tüm veriler (body, params, query) class-validator gibi kütüphanelerle doğrulanmalı ve temizlenmelidir.

Şifre Güvenliği: Şifreler veritabanında asla düz metin olarak saklanmamalı, bcrypt ile hash'lenmelidir.
