#!/usr/bin/env python3
"""Fill django.po catalogs for MyAutoHub application locales."""
from __future__ import annotations

import polib

# msgid -> {lang: msgstr}
# Plural: msgid -> {lang: (singular, plural)} or for more forms a tuple

SINGULAR: dict[str, dict[str, str]] = {}
PLURAL: dict[str, dict[str, tuple[str, ...]]] = {}


def t(msgid: str, **langs: str) -> None:
    SINGULAR[msgid] = langs


def tp(msgid: str, msgid_plural: str, **langs: tuple[str, ...]) -> None:
    PLURAL[msgid] = langs
    # also store plural form lookups if needed
    _ = msgid_plural


# --- Nav / sections ---
t("Emergency", fa="اورژانسی", ar="الطوارئ", fr="Urgence", de="Notfall", es="Emergencia", ru="Аварийная помощь")
t("Pricing", fa="خدمات رایج", ar="الأسعار", fr="Tarifs", de="Preise", es="Precios", ru="Цены")
t("Marketplace", fa="بازار", ar="السوق", fr="Marché", de="Marktplatz", es="Mercado", ru="Маркетплейс")
t("Cars", fa="خودروها", ar="السيارات", fr="Voitures", de="Autos", es="Coches", ru="Автомобили")
t("YouTube", fa="یوتیوب", ar="يوتيوب", fr="YouTube", de="YouTube", es="YouTube", ru="YouTube")
t("Stories", fa="داستان‌ها", ar="القصص", fr="Histoires", de="Geschichten", es="Historias", ru="Истории")
t(
    "Roadside help when you need it-request, track, and buzz operators.",
    fa="کمک کنار جاده وقتی لازم دارید-درخواست، پیگیری و بازرسان را باز بزنید.",
    ar="مساعدة على الطريق عند الحاجة-اطلب وتتبع ونبّه المشغّلين.",
    fr="Aide routière quand vous en avez besoin-demandez, suivez et alertez les opérateurs.",
    de="Pannenhilfe wenn Sie sie brauchen-anfordern, verfolgen und Operatoren buzzern.",
    es="Ayuda en carretera cuando la necesites-solicita, sigue y avisa a los operadores.",
    ru="Помощь на дороге когда нужно-запросите, отслеживайте и сигнальте операторам.",
)
t(
    "Reference prices for cars and common service packages.",
    fa="قیمت‌های مرجع برای خودروها و بسته‌های خدماتی رایج.",
    ar="أسعار مرجعية للسيارات وباقات الخدمات الشائعة.",
    fr="Prix de référence pour les voitures et forfaits de service courants.",
    de="Richtpreise für Autos und gängige Servicepakete.",
    es="Precios de referencia para coches y paquetes de servicio habituales.",
    ru="Справочные цены на автомобили и типовые пакеты услуг.",
)
t(
    "Buy and sell cars with clear listings from real people.",
    fa="خرید و فروش خودرو با آگهی‌های شفاف از افراد واقعی.",
    ar="اشترِ وبِع سيارات بإعلانات واضحة من أشخاص حقيقيين.",
    fr="Achetez et vendez des voitures avec des annonces claires de vraies personnes.",
    de="Autos kaufen und verkaufen mit klaren Inseraten von echten Menschen.",
    es="Compra y vende coches con anuncios claros de personas reales.",
    ru="Покупайте и продавайте авто с понятными объявлениями от реальных людей.",
)
t(
    "Browse the catalog-brands, models, and specs.",
    fa="مرور کاتالوگ-برندها، مدل‌ها و مشخصات.",
    ar="تصفح الكتالوج-العلامات والنماذج والمواصفات.",
    fr="Parcourez le catalogue-marques, modèles et caractéristiques.",
    de="Katalog durchsuchen-Marken, Modelle und Daten.",
    es="Explora el catálogo-marcas, modelos y especificaciones.",
    ru="Смотрите каталог-марки, модели и характеристики.",
)
t(
    "Watch guides, reviews, and hub stories on video.",
    fa="راهنماها، بررسی‌ها و داستان‌های هاب را ویدیویی ببینید.",
    ar="شاهد الأدلة والمراجعات وقصص المركز على الفيديو.",
    fr="Regardez guides, avis et histoires du hub en vidéo.",
    de="Anleitungen, Reviews und Hub-Geschichten als Video ansehen.",
    es="Mira guías, reseñas e historias del hub en vídeo.",
    ru="Смотрите гайды, обзоры и истории хаба на видео.",
)
t(
    "Human stories from the road and the MyAutoHub community.",
    fa="داستان‌های انسانی از جاده و جامعه MyAutoHub.",
    ar="قصص إنسانية من الطريق ومجتمع ماي أوتو هب.",
    fr="Histoires humaines de la route et de la communauté MyAutoHub.",
    de="Menschliche Geschichten von der Straße und der MyAutoHub-Community.",
    es="Historias humanas de la carretera y la comunidad MyAutoHub.",
    ru="Человеческие истории с дороги и сообщества MyAutoHub.",
)

# Errors
t("Bad request", fa="درخواست نامعتبر", ar="طلب غير صالح", fr="Requête incorrecte", de="Ungültige Anfrage", es="Solicitud incorrecta", ru="Неверный запрос")
t(
    "The request could not be understood. Please try again.",
    fa="درخواست قابل فهم نبود. لطفاً دوباره تلاش کنید.",
    ar="تعذر فهم الطلب. يرجى المحاولة مرة أخرى.",
    fr="La requête n'a pas pu être comprise. Veuillez réessayer.",
    de="Die Anfrage konnte nicht verstanden werden. Bitte erneut versuchen.",
    es="No se pudo entender la solicitud. Inténtalo de nuevo.",
    ru="Не удалось понять запрос. Попробуйте ещё раз.",
)
t("Access denied", fa="دسترسی مجاز نیست", ar="الوصول مرفوض", fr="Accès refusé", de="Zugriff verweigert", es="Acceso denegado", ru="Доступ запрещён")
t(
    "You do not have permission to view this page.",
    fa="اجازه مشاهده این صفحه را ندارید.",
    ar="ليس لديك إذن لعرض هذه الصفحة.",
    fr="Vous n'avez pas la permission de voir cette page.",
    de="Sie haben keine Berechtigung, diese Seite anzuzeigen.",
    es="No tienes permiso para ver esta página.",
    ru="У вас нет прав для просмотра этой страницы.",
)
t("Page not found", fa="صفحه پیدا نشد", ar="الصفحة غير موجودة", fr="Page introuvable", de="Seite nicht gefunden", es="Página no encontrada", ru="Страница не найдена")
t(
    "This road does not lead anywhere. Head back to the hub.",
    fa="این مسیر به جایی نمی‌رسد. به هاب برگردید.",
    ar="هذا الطريق لا يؤدي إلى أي مكان. عد إلى المركز.",
    fr="Cette route ne mène nulle part. Retournez au hub.",
    de="Dieser Weg führt nirgendwohin. Zurück zum Hub.",
    es="Este camino no lleva a ninguna parte. Vuelve al hub.",
    ru="Эта дорога никуда не ведёт. Вернитесь в хаб.",
)
t("Something went wrong", fa="مشکلی پیش آمد", ar="حدث خطأ ما", fr="Une erreur s'est produite", de="Etwas ist schiefgelaufen", es="Algo salió mal", ru="Что-то пошло не так")
t(
    "We hit a snag on our side. Please try again in a moment.",
    fa="در سمت ما مشکلی رخ داد. کمی بعد دوباره تلاش کنید.",
    ar="واجهنا مشكلة من جانبنا. يرجى المحاولة بعد لحظات.",
    fr="Un problème est survenu de notre côté. Réessayez dans un instant.",
    de="Bei uns ist etwas schiefgelaufen. Bitte gleich nochmal versuchen.",
    es="Tuvimos un problema de nuestra parte. Inténtalo en un momento.",
    ru="Сбой на нашей стороне. Попробуйте через минуту.",
)

# Accounts
t("Log in-MyAutoHub", fa="ورود-MyAutoHub", ar="تسجيل الدخول-ماي أوتو هب", fr="Connexion-MyAutoHub", de="Anmelden-MyAutoHub", es="Iniciar sesión-MyAutoHub", ru="Вход-MyAutoHub")
t("Welcome back", fa="خوش آمدید", ar="مرحباً بعودتك", fr="Bon retour", de="Willkommen zurück", es="Bienvenido de nuevo", ru="С возвращением")
t(
    "Log in to request emergency help, manage listings, and save locations.",
    fa="وارد شوید تا کمک اورژانسی بخواهید، آگهی‌ها را مدیریت کنید و مکان‌ها را ذخیره کنید.",
    ar="سجّل الدخول لطلب المساعدة الطارئة وإدارة الإعلانات وحفظ المواقع.",
    fr="Connectez-vous pour demander de l'aide d'urgence, gérer vos annonces et enregistrer des lieux.",
    de="Melden Sie sich an, um Notfallhilfe anzufordern, Inserate zu verwalten und Orte zu speichern.",
    es="Inicia sesión para pedir ayuda de emergencia, gestionar anuncios y guardar ubicaciones.",
    ru="Войдите, чтобы запросить помощь, управлять объявлениями и сохранять места.",
)
t("Log in", fa="ورود", ar="تسجيل الدخول", fr="Connexion", de="Anmelden", es="Iniciar sesión", ru="Войти")
t("No account yet?", fa="هنوز حساب ندارید؟", ar="ليس لديك حساب بعد؟", fr="Pas encore de compte ?", de="Noch kein Konto?", es="¿Aún no tienes cuenta?", ru="Ещё нет аккаунта?")
t("Join MyAutoHub", fa="عضویت در MyAutoHub", ar="انضم إلى ماي أوتو هب", fr="Rejoindre MyAutoHub", de="MyAutoHub beitreten", es="Únete a MyAutoHub", ru="Присоединиться к MyAutoHub")
t("Join-MyAutoHub", fa="عضویت-MyAutoHub", ar="انضمام-ماي أوتو هب", fr="Inscription-MyAutoHub", de="Beitreten-MyAutoHub", es="Unirse-MyAutoHub", ru="Регистрация-MyAutoHub")
t(
    "Create an account to submit emergency requests and use the marketplace.",
    fa="حساب بسازید تا درخواست اورژانسی ثبت کنید و از بازار استفاده کنید.",
    ar="أنشئ حساباً لإرسال طلبات الطوارئ واستخدام السوق.",
    fr="Créez un compte pour envoyer des demandes d'urgence et utiliser le marché.",
    de="Konto erstellen, um Notfallanfragen zu stellen und den Marktplatz zu nutzen.",
    es="Crea una cuenta para enviar solicitudes de emergencia y usar el mercado.",
    ru="Создайте аккаунт, чтобы отправлять заявки и пользоваться маркетплейсом.",
)
t("Create account", fa="ایجاد حساب", ar="إنشاء حساب", fr="Créer un compte", de="Konto erstellen", es="Crear cuenta", ru="Создать аккаунт")
t("Profile-MyAutoHub", fa="پروفایل-MyAutoHub", ar="الملف-ماي أوتو هب", fr="Profil-MyAutoHub", de="Profil-MyAutoHub", es="Perfil-MyAutoHub", ru="Профиль-MyAutoHub")
t(
    "Saved places you can reuse when requesting emergency help.",
    fa="مکان‌های ذخیره‌شده که هنگام درخواست کمک اورژانسی دوباره استفاده می‌کنید.",
    ar="أماكن محفوظة يمكنك إعادة استخدامها عند طلب المساعدة الطارئة.",
    fr="Lieux enregistrés réutilisables pour les demandes d'urgence.",
    de="Gespeicherte Orte für Notfallanfragen.",
    es="Lugares guardados para reutilizar al pedir ayuda de emergencia.",
    ru="Сохранённые места для повторного использования при запросе помощи.",
)
t("Saved locations", fa="مکان‌های ذخیره‌شده", ar="المواقع المحفوظة", fr="Lieux enregistrés", de="Gespeicherte Orte", es="Ubicaciones guardadas", ru="Сохранённые места")
t("Label", fa="برچسب", ar="التسمية", fr="Libellé", de="Bezeichnung", es="Etiqueta", ru="Метка")
t("Address", fa="آدرس", ar="العنوان", fr="Adresse", de="Adresse", es="Dirección", ru="Адрес")
t("Coordinates", fa="مختصات", ar="الإحداثيات", fr="Coordonnées", de="Koordinaten", es="Coordenadas", ru="Координаты")
t("Default", fa="پیش‌فرض", ar="افتراضي", fr="Par défaut", de="Standard", es="Predeterminado", ru="По умолчанию")
t("Remove", fa="حذف", ar="إزالة", fr="Supprimer", de="Entfernen", es="Eliminar", ru="Удалить")
t("No saved locations yet.", fa="هنوز مکان ذخیره‌شده‌ای نیست.", ar="لا توجد مواقع محفوظة بعد.", fr="Aucun lieu enregistré pour l'instant.", de="Noch keine gespeicherten Orte.", es="Aún no hay ubicaciones guardadas.", ru="Пока нет сохранённых мест.")
t("Add a location", fa="افزودن مکان", ar="إضافة موقع", fr="Ajouter un lieu", de="Ort hinzufügen", es="Añadir ubicación", ru="Добавить место")
t("Save location", fa="ذخیره مکان", ar="حفظ الموقع", fr="Enregistrer le lieu", de="Ort speichern", es="Guardar ubicación", ru="Сохранить место")

# Shell
t(
    "MyAutoHub-cars, help, and community on the road.",
    fa="MyAutoHub-خودرو، کمک و جامعه در جاده.",
    ar="ماي أوتو هب-سيارات ومساعدة ومجتمع على الطريق.",
    fr="MyAutoHub-voitures, aide et communauté sur la route.",
    de="MyAutoHub-Autos, Hilfe und Community unterwegs.",
    es="MyAutoHub-coches, ayuda y comunidad en la carretera.",
    ru="MyAutoHub-авто, помощь и сообщество на дороге.",
)
t("Primary", fa="اصلی", ar="رئيسي", fr="Principal", de="Primär", es="Principal", ru="Основная")
t("Light theme", fa="تم روشن", ar="مظهر فاتح", fr="Thème clair", de="Helles Design", es="Tema claro", ru="Светлая тема")
t("Dark theme", fa="تم تیره", ar="مظهر داكن", fr="Thème sombre", de="Dunkles Design", es="Tema oscuro", ru="Тёмная тема")
t("Toggle theme", fa="تغییر تم", ar="تبديل المظهر", fr="Changer de thème", de="Design umschalten", es="Cambiar tema", ru="Сменить тему")
t("Language", fa="زبان", ar="اللغة", fr="Langue", de="Sprache", es="Idioma", ru="Язык")
t("Log out", fa="خروج", ar="تسجيل الخروج", fr="Déconnexion", de="Abmelden", es="Cerrar sesión", ru="Выйти")
t("Join", fa="عضویت", ar="انضمام", fr="Rejoindre", de="Beitreten", es="Unirse", ru="Регистрация")

# Home
t("MyAutoHub-Hub", fa="MyAutoHub-هاب", ar="ماي أوتو هب-المركز", fr="MyAutoHub-Hub", de="MyAutoHub-Hub", es="MyAutoHub-Hub", ru="MyAutoHub-Хаб")
t("Hero", fa="بخش اصلی", ar="القسم الرئيسي", fr="Héro", de="Hero", es="Héroe", ru="Герой")
t(
    "Automotive ecosystem platform",
    fa="پلتفرم اکوسیستم خودرو",
    ar="منصة النظام البيئي للسيارات",
)
t(
    "Pin your location for towing, battery jump-start, or explore the marketplace.",
    fa="موقعیت خود را برای بکسل، استارت باتری، یا کاوش در بازار پین کنید.",
    ar="ثبّت موقعك للقطر أو تشغيل البطارية أو استكشف السوق.",
)
t("Request emergency", fa="درخواست اورژانسی", ar="طلب طوارئ")
t("Explore marketplace", fa="کاوش در بازار", ar="استكشف السوق")
t("Live Map", fa="نقشه زنده", ar="الخريطة المباشرة")
t("Pin your location", fa="موقعیت خود را پین کنید", ar="ثبّت موقعك")
t(
    "Open live map for roadside help",
    fa="باز کردن نقشه زنده برای کمک کنار جاده",
    ar="افتح الخريطة المباشرة للمساعدة على الطريق",
)
t(
    "Live map preview-open to pin your location for roadside help",
    fa="پیش‌نمایش نقشه زنده-برای پین کردن موقعیت و کمک کنار جاده باز کنید",
    ar="معاينة الخريطة المباشرة-افتح لتثبيت موقعك للمساعدة على الطريق",
)
t("Loading map", fa="در حال بارگذاری نقشه", ar="جاري تحميل الخريطة")
t("Emergency Assistance", fa="کمک اورژانسی", ar="المساعدة الطارئة")
t("Car Marketplace", fa="بازار خودرو", ar="سوق السيارات")
t("Maintenance & Specs", fa="نگهداری و مشخصات", ar="الصيانة والمواصفات")
t("Browse cars", fa="مرور خودروها", ar="تصفح السيارات")
t("Quick paths", fa="مسیرهای سریع", ar="مسارات سريعة")
t("Roadside help", fa="کمک کنار جاده", ar="مساعدة على الطريق")
t("Specs & models", fa="مشخصات و مدل‌ها", ar="المواصفات والنماذج")
t("Dealers & shops", fa="نمایندگی‌ها و تعمیرگاه‌ها", ar="الوكلاء والورش")
t("How to start", fa="چطور شروع کنید", ar="كيف تبدأ")
t(
    "Use Emergency to pin yourself on the map, Marketplace to buy or sell, and Cars for specs. Switch language anytime from FA / EN / AR in the header.",
    fa="از اورژانسی برای پین روی نقشه، از بازار برای خرید و فروش، و از خودروها برای مشخصات استفاده کنید. زبان را هر وقت از FA / EN / AR در هدر عوض کنید.",
    ar="استخدم الطوارئ لتثبيت موقعك على الخريطة، والسوق للبيع والشراء، والسيارات للمواصفات. بدّل اللغة في أي وقت من FA / EN / AR في الرأس.",
)
t("Learn tip", fa="نکته آموزشی", ar="نصيحة تعليمية")
t("Dismiss tip", fa="بستن نکته", ar="إخفاء النصيحة")
t(
    "Log in, tap New request, then drop a pin on the map (or pick a saved place) so operators can find you fast.",
    fa="وارد شوید، روی درخواست جدید بزنید، سپس روی نقشه پین بگذارید (یا مکان ذخیره‌شده را انتخاب کنید) تا اپراتورها سریع پیدایتان کنند.",
    ar="سجّل الدخول، اضغط طلب جديد، ثم ضع دبوساً على الخريطة (أو اختر مكاناً محفوظاً) ليجدك المشغّلون بسرعة.",
)
t(
    "Browse listings to buy, or sell your car with photos and titles in فارسی, English, and العربية so more buyers can find you.",
    fa="آگهی‌ها را برای خرید ببینید، یا خودروی خود را با عکس و عنوان به فارسی، English و العربية بفروشید تا خریداران بیشتری شما را پیدا کنند.",
    ar="تصفح الإعلانات للشراء، أو بِع سيارتك مع صور وعناوين بالفارسية والإنجليزية والعربية ليجدك المزيد من المشترين.",
)
t(
    "Filter by brand, model, or year. Open a car for specs, then jump to marketplace deals for that model.",
    fa="با برند، مدل یا سال فیلتر کنید. خودرو را برای مشخصات باز کنید، سپس به معاملات بازار همان مدل بروید.",
    ar="صفِّ حسب العلامة أو النموذج أو السنة. افتح سيارة للمواصفات، ثم انتقل إلى عروض السوق لذلك النموذج.",
)
t(
    "Filter by country flag, brand, model, or year. Open a car for specs, then jump to marketplace deals for that model.",
    fa="با پرچم کشور، برند، مدل یا سال فیلتر کنید. خودرو را برای مشخصات باز کنید، سپس به معاملات بازار همان مدل بروید.",
    ar="صفِّ بعلم الدولة أو العلامة أو النموذج أو السنة. افتح سيارة للمواصفات، ثم انتقل إلى عروض السوق لذلك النموذج.",
)
t("Open menu", fa="باز کردن منو", ar="فتح القائمة")
t("Close menu", fa="بستن منو", ar="إغلاق القائمة")
t("Country", fa="کشور", ar="الدولة")
t("Filter by country", fa="فیلتر بر اساس کشور", ar="التصفية حسب الدولة")
t("All countries", fa="همه کشورها", ar="كل الدول")
t("All", fa="همه", ar="الكل")
t("Iran", fa="ایران", ar="إيران")
t("USA", fa="آمریکا", ar="الولايات المتحدة")
t("Japan", fa="ژاپن", ar="اليابان")
t("Germany", fa="آلمان", ar="ألمانيا")
t("South Korea", fa="کره جنوبی", ar="كوريا الجنوبية")
t("France", fa="فرانسه", ar="فرنسا")
t("Italy", fa="ایتالیا", ar="إيطاليا")
t("China", fa="چین", ar="الصين")
t("United Kingdom", fa="بریتانیا", ar="المملكة المتحدة")
t("Brands", fa="برندها", ar="العلامات")
t("Brands-MyAutoHub", fa="برندها-مای‌اتوهاب", ar="العلامات-ماي أوتو هب")
t(
    "Browse car brands on MyAutoHub by country and manufacturer.",
    fa="برندهای خودرو را در مای‌اتوهاب بر اساس کشور و سازنده مرور کنید.",
    ar="تصفح علامات السيارات في ماي أوتو هب حسب الدولة والشركة المصنعة.",
)
t(
    "Explore manufacturers and marques-filter the catalog by brand or open a brand page for models.",
    fa="سازندگان و برندها را ببینید-کاتالوگ را بر اساس برند فیلتر کنید یا صفحه برند را برای مدل‌ها باز کنید.",
    ar="استكشف الشركات والموديلات-صفِّ الكتالوج حسب العلامة أو افتح صفحة العلامة للنماذج.",
)
t("No brands in the catalog yet.", fa="هنوز برندی در کاتالوگ نیست.", ar="لا توجد علامات في الكتالوج بعد.")
t("Other", fa="سایر", ar="أخرى")
t("All brands", fa="همه برندها", ar="كل العلامات")
t("View in catalog", fa="مشاهده در کاتالوگ", ar="عرض في الكتالوج")
t("No models for this brand yet.", fa="هنوز مدلی برای این برند نیست.", ar="لا توجد نماذج لهذه العلامة بعد.")
t("Models", fa="مدل‌ها", ar="النماذج")
t("See all", fa="مشاهده همه", ar="عرض الكل")
t("Car catalog", fa="کاتالوگ خودرو", ar="كتالوج السيارات")
tp(
    "%(counter)s brand",
    "%(counter)s brands",
    fa=("%(counter)s برند", "%(counter)s برند"),
    ar=(
        "%(counter)s علامة",
        "%(counter)s علامات",
        "%(counter)s علامتان",
        "%(counter)s علامات",
        "%(counter)s علامة",
        "%(counter)s علامة",
    ),
)
tp(
    "%(counter)s model",
    "%(counter)s models",
    fa=("%(counter)s مدل", "%(counter)s مدل"),
    ar=(
        "%(counter)s نموذج",
        "%(counter)s نماذج",
        "%(counter)s نموذجان",
        "%(counter)s نماذج",
        "%(counter)s نموذجاً",
        "%(counter)s نموذج",
    ),
)
t(
    "Models and cars for %(name)s on MyAutoHub.",
    fa="مدل‌ها و خودروهای %(name)s در مای‌اتوهاب.",
    ar="نماذج وسيارات %(name)s في ماي أوتو هب.",
)
t("Marketplace listings", fa="آگهی‌های بازار", ar="إعلانات السوق")
t("Price references", fa="قیمت‌های مرجع", ar="أسعار مرجعية")
t("Site administration", fa="مدیریت سایت", ar="إدارة الموقع")
t(
    "Change records across every hub model-multilingual fields use FA / EN / AR tabs.",
    fa="رکوردها را در همه مدل‌های هاب ویرایش کنید-فیلدهای چندزبانه با تب‌های فارسی / انگلیسی / عربی.",
    ar="عدّل السجلات عبر كل نماذج المركز-الحقول متعددة اللغات عبر تبويبات FA / EN / AR.",
)
t("New listing", fa="آگهی جدید", ar="إعلان جديد")
t("Edit listing", fa="ویرایش آگهی", ar="تعديل الإعلان")
t("New price", fa="قیمت جدید", ar="سعر جديد")
t("Edit price", fa="ویرایش قیمت", ar="تعديل السعر")
t("Listing created.", fa="آگهی ساخته شد.", ar="تم إنشاء الإعلان.")
t("Listing updated.", fa="آگهی به‌روز شد.", ar="تم تحديث الإعلان.")
t("Price reference created.", fa="قیمت مرجع ساخته شد.", ar="تم إنشاء السعر المرجعي.")
t("Price reference updated.", fa="قیمت مرجع به‌روز شد.", ar="تم تحديث السعر المرجعي.")
t("No listings yet.", fa="هنوز آگهی‌ای نیست.", ar="لا توجد إعلانات بعد.")
t("No price references yet.", fa="هنوز قیمت مرجعی نیست.", ar="لا توجد أسعار مرجعية بعد.")
t("Catalog", fa="کاتالوگ", ar="الكتالوج")
t("Content", fa="محتوا", ar="المحتوى")
t("Change", fa="تغییر", ar="تغيير")
t("Add", fa="افزودن", ar="إضافة")
t("Inquiries", fa="پیام‌ها", ar="الاستفسارات")
t(
    "Open a dealer or shop for contact details and linked brands from the catalog.",
    fa="یک نمایندگی یا تعمیرگاه را برای جزئیات تماس و برندهای مرتبط از کاتالوگ باز کنید.",
    ar="افتح وكيلاً أو ورشة لمعرفة تفاصيل الاتصال والعلامات المرتبطة من الكتالوج.",
)
t(
    "Choose a service, then tap the map to drop your pin-or use a saved place from your profile.",
    fa="یک خدمت را انتخاب کنید، سپس روی نقشه بزنید تا پین بگذارید-یا از مکان ذخیره‌شده در پروفایل استفاده کنید.",
    ar="اختر خدمة، ثم اضغط الخريطة لوضع دبوسك-أو استخدم مكاناً محفوظاً من ملفك.",
)
t(
    "These are reference prices for context-not a formal quote. Compare with marketplace listings too.",
    fa="این‌ها قیمت‌های مرجع برای زمینه هستند-نه پیشنهاد رسمی. با آگهی‌های بازار هم مقایسه کنید.",
    ar="هذه أسعار مرجعية للسياق-وليست عرضاً رسمياً. قارن أيضاً مع إعلانات السوق.",
)
t("Pin roadside emergencies on the map", fa="اورژانس کنار جاده را روی نقشه پین کنید", ar="ثبّت طوارئ الطريق على الخريطة")
t("Buy and sell cars on the marketplace", fa="خرید و فروش خودرو در بازار", ar="اشترِ وبِع السيارات في السوق")
t("Reuse saved places for faster help", fa="از مکان‌های ذخیره‌شده برای کمک سریع‌تر استفاده کنید", ar="أعد استخدام الأماكن المحفوظة لمساعدة أسرع")
t("Use your MyAutoHub username and password.", fa="از نام کاربری و رمز عبور MyAutoHub استفاده کنید.", ar="استخدم اسم مستخدم وكلمة مرور ماي أوتو هب.")
t(
    "After login you can open Profile to save map pins, or Marketplace to sell a car.",
    fa="بعد ورود می‌توانید پروفایل را برای ذخیره پین نقشه باز کنید، یا در بازار خودرو بفروشید.",
    ar="بعد تسجيل الدخول يمكنك فتح الملف لحفظ دبابيس الخريطة، أو السوق لبيع سيارة.",
)
t("One account for help, catalog, and trade", fa="یک حساب برای کمک، کاتالوگ و معامله", ar="حساب واحد للمساعدة والكتالوج والتجارة")
t(
    "Listings in فارسی, English, and العربية",
    fa="آگهی‌ها به فارسی، English و العربية",
    ar="إعلانات بالفارسية والإنجليزية والعربية",
)
t("Theme and language stay with your browser", fa="تم و زبان با مرورگر شما می‌مانند", ar="المظهر واللغة يبقيان مع متصفحك")
t("A few fields and you are ready to use the hub.", fa="چند فیلد و آماده استفاده از هاب هستید.", ar="حقول قليلة وتكون جاهزاً لاستخدام المركز.")
t(
    "Pick a username you can share with buyers. You can add saved locations from Profile after joining.",
    fa="نام کاربری‌ای انتخاب کنید که بتوانید با خریداران به اشتراک بگذارید. بعد از عضویت از پروفایل مکان ذخیره کنید.",
    ar="اختر اسم مستخدم يمكنك مشاركته مع المشترين. يمكنك إضافة أماكن محفوظة من الملف بعد الانضمام.",
)
t("Already have an account?", fa="از قبل حساب دارید؟", ar="هل لديك حساب بالفعل؟")
t(
    "Your hub desk-listings, saved places, and shortcuts for roadside help.",
    fa="میز هاب شما-آگهی‌ها، مکان‌های ذخیره‌شده و میان‌برهای کمک کنار جاده.",
    ar="مكتب مركزك-الإعلانات والأماكن المحفوظة واختصارات المساعدة على الطريق.",
)
t(
    "Save places you use often, then pick them when requesting emergency help. Sell cars from Marketplace.",
    fa="مکان‌هایی که زیاد استفاده می‌کنید ذخیره کنید، سپس هنگام درخواست اورژانسی انتخابشان کنید. خودرو را از بازار بفروشید.",
    ar="احفظ الأماكن التي تستخدمها كثيراً، ثم اخترها عند طلب الطوارئ. بِع السيارات من السوق.",
)
t("Shortcuts", fa="میان‌برها", ar="اختصارات")
t("Edit, mark sold, or read buyer messages.", fa="ویرایش، علامت فروخته‌شده، یا خواندن پیام خریدار.", ar="عدّل أو علّم كمباع أو اقرأ رسائل المشتري.")
t(
    "Create a listing with photos and multilingual titles.",
    fa="آگهی با عکس و عنوان چندزبانه بسازید.",
    ar="أنشئ إعلاناً مع صور وعناوين متعددة اللغات.",
)
t("Pin yourself on the map or use a saved place.", fa="خود را روی نقشه پین کنید یا از مکان ذخیره‌شده استفاده کنید.", ar="ثبّت نفسك على الخريطة أو استخدم مكاناً محفوظاً.")
t("Open the catalog for specs and models.", fa="کاتالوگ را برای مشخصات و مدل‌ها باز کنید.", ar="افتح الكتالوج للمواصفات والنماذج.")
t("Map", fa="نقشه", ar="الخريطة")
t("No address note", fa="بدون یادداشت آدرس", ar="بدون ملاحظة عنوان")
t(
    "No saved locations yet. Add one below for faster emergency requests.",
    fa="هنوز مکان ذخیره‌شده‌ای نیست. یکی را پایین اضافه کنید تا درخواست اورژانسی سریع‌تر شود.",
    ar="لا أماكن محفوظة بعد. أضف واحداً أدناه لطلبات طوارئ أسرع.",
)
t("Tap the map to drop a pin before saving.", fa="قبل ذخیره روی نقشه بزنید تا پین بگذارید.", ar="اضغط الخريطة لوضع دبوس قبل الحفظ.")
t(
    "Open a listing to edit details or read buyer messages. Start a new sale anytime.",
    fa="یک آگهی را برای ویرایش جزئیات یا خواندن پیام خریدار باز کنید. هر وقت فروش جدید شروع کنید.",
    ar="افتح إعلاناً لتعديل التفاصيل أو قراءة رسائل المشتري. ابدأ بيعاً جديداً في أي وقت.",
)
tp(
    "%(counter)s place",
    "%(counter)s places",
    fa=("%(counter)s مکان", "%(counter)s مکان"),
    ar=("%(counter)s مكان", "%(counter)s مكان", "%(counter)s مكانان", "%(counter)s أماكن", "%(counter)s مكاناً", "%(counter)s مكان"),
)
t(
    "Your car hub, ready when you are",
    fa="هاب خودروی شما، آماده وقتی شما آماده‌اید",
    ar="مركز سيارتك، جاهز عندما تكون جاهزاً",
    fr="Votre hub auto, prêt quand vous l'êtes",
    de="Ihr Auto-Hub, bereit wenn Sie es sind",
    es="Tu hub de coches, listo cuando tú lo estés",
    ru="Ваш автохаб-готов, когда готовы вы",
)
t(
    "Request roadside help, check pricing, buy or sell, browse cars, and catch stories-all in one calm place.",
    fa="کمک کنار جاده بخواهید، قیمت ببینید، بخرید یا بفروشید، خودروها را مرور کنید و داستان‌ها را دنبال کنید-همه در یک جای آرام.",
    ar="اطلب مساعدة الطريق، تحقق من الأسعار، اشترِ أو بِع، تصفح السيارات، وتابع القصص-كل ذلك في مكان هادئ واحد.",
    fr="Demandez de l'aide routière, consultez les tarifs, achetez ou vendez, parcourez les voitures et suivez les histoires-tout en un lieu calme.",
    de="Pannenhilfe anfordern, Preise prüfen, kaufen oder verkaufen, Autos browsen und Geschichten lesen-alles an einem ruhigen Ort.",
    es="Pide ayuda en carretera, consulta precios, compra o vende, explora coches y sigue historias-todo en un lugar tranquilo.",
    ru="Запросите помощь на дороге, смотрите цены, покупайте или продавайте, изучайте авто и читайте истории-всё в одном спокойном месте.",
)
t("Create an account", fa="ایجاد حساب", ar="إنشاء حساب", fr="Créer un compte", de="Konto erstellen", es="Crear una cuenta", ru="Создать аккаунт")
t("See emergency services", fa="مشاهده خدمات اورژانسی", ar="عرض خدمات الطوارئ", fr="Voir les services d'urgence", de="Notfalldienste ansehen", es="Ver servicios de emergencia", ru="Смотреть аварийные услуги")
t("Explore the hub", fa="کاوش در هاب", ar="استكشف المركز", fr="Explorer le hub", de="Hub erkunden", es="Explorar el hub", ru="Исследовать хаб")

# Emergency
t("Emergency-MyAutoHub", fa="اورژانسی-MyAutoHub", ar="الطوارئ-ماي أوتو هب", fr="Urgence-MyAutoHub", de="Notfall-MyAutoHub", es="Emergencia-MyAutoHub", ru="Авария-MyAutoHub")
t("Emergency services", fa="خدمات اورژانسی", ar="خدمات الطوارئ", fr="Services d'urgence", de="Notfalldienste", es="Servicios de emergencia", ru="Аварийные услуги")
t(
    "Request roadside help, track progress, and buzz operators when you need attention fast.",
    fa="کمک کنار جاده بخواهید، پیشرفت را پیگیری کنید و وقتی نیاز به توجه سریع دارید باز بزنید.",
    ar="اطلب مساعدة الطريق، وتتبع التقدم، ونبّه المشغّلين عندما تحتاج انتباهاً سريعاً.",
    fr="Demandez de l'aide, suivez l'avancement et alertez les opérateurs quand vous avez besoin d'attention rapide.",
    de="Pannenhilfe anfordern, Fortschritt verfolgen und Operatoren buzzern, wenn Sie schnell Hilfe brauchen.",
    es="Pide ayuda en carretera, sigue el progreso y avisa a los operadores cuando necesites atención rápida.",
    ru="Запросите помощь, отслеживайте прогресс и сигнальте операторам, когда нужно быстрое внимание.",
)
t("New request", fa="درخواست جدید", ar="طلب جديد", fr="Nouvelle demande", de="Neue Anfrage", es="Nueva solicitud", ru="Новая заявка")
t("Log in to request help", fa="برای درخواست کمک وارد شوید", ar="سجّل الدخول لطلب المساعدة", fr="Connectez-vous pour demander de l'aide", de="Anmelden, um Hilfe anzufordern", es="Inicia sesión para pedir ayuda", ru="Войдите, чтобы запросить помощь")
t("Operator view", fa="نمای اپراتور", ar="عرض المشغّل", fr="Vue opérateur", de="Operatoransicht", es="Vista de operador", ru="Вид оператора")
t("Search", fa="جستجو", ar="بحث", fr="Rechercher", de="Suchen", es="Buscar", ru="Поиск")
t("ID", fa="شناسه", ar="المعرّف", fr="ID", de="ID", es="ID", ru="ID")
t("Service", fa="خدمت", ar="الخدمة", fr="Service", de="Service", es="Servicio", ru="Услуга")
t("Status", fa="وضعیت", ar="الحالة", fr="Statut", de="Status", es="Estado", ru="Статус")
t("When", fa="زمان", ar="الوقت", fr="Quand", de="Wann", es="Cuándo", ru="Когда")
t("Buzz", fa="باز", ar="تنبيه", fr="Buzz", de="Buzz", es="Buzz", ru="Сигнал")
t("Open", fa="باز کردن", ar="فتح", fr="Ouvrir", de="Öffnen", es="Abrir", ru="Открыть")
t("No emergency requests to show.", fa="درخواست اورژانسی برای نمایش نیست.", ar="لا توجد طلبات طوارئ للعرض.", fr="Aucune demande d'urgence à afficher.", de="Keine Notfallanfragen anzuzeigen.", es="No hay solicitudes de emergencia.", ru="Нет аварийных заявок для показа.")
t("—", fa="—", ar="—", fr="—", de="—", es="—", ru="—")
t("Details", fa="جزئیات", ar="التفاصيل", fr="Détails", de="Details", es="Detalles", ru="Детали")
t("Location:", fa="موقعیت:", ar="الموقع:", fr="Lieu :", de="Standort:", es="Ubicación:", ru="Место:")
t("Buzz!", fa="باز!", ar="تنبيه!", fr="Buzz !", de="Buzz!", es="¡Buzz!", ru="Сигнал!")
t("Cancel", fa="لغو", ar="إلغاء", fr="Annuler", de="Abbrechen", es="Cancelar", ru="Отмена")
t("Back to list", fa="بازگشت به فهرست", ar="العودة إلى القائمة", fr="Retour à la liste", de="Zurück zur Liste", es="Volver a la lista", ru="Назад к списку")
t("Update status", fa="به‌روزرسانی وضعیت", ar="تحديث الحالة", fr="Mettre à jour le statut", de="Status aktualisieren", es="Actualizar estado", ru="Обновить статус")
t("New status", fa="وضعیت جدید", ar="حالة جديدة", fr="Nouveau statut", de="Neuer Status", es="Nuevo estado", ru="Новый статус")
t("Note", fa="یادداشت", ar="ملاحظة", fr="Note", de="Notiz", es="Nota", ru="Заметка")
t("Apply", fa="اعمال", ar="تطبيق", fr="Appliquer", de="Anwenden", es="Aplicar", ru="Применить")
t("Public review", fa="نظر عمومی", ar="مراجعة عامة", fr="Avis public", de="Öffentliche Bewertung", es="Reseña pública", ru="Публичный отзыв")
t("Share experience", fa="اشتراک تجربه", ar="مشاركة التجربة", fr="Partager l'expérience", de="Erfahrung teilen", es="Compartir experiencia", ru="Поделиться опытом")
t("No review yet.", fa="هنوز نظری ثبت نشده.", ar="لا توجد مراجعة بعد.", fr="Pas encore d'avis.", de="Noch keine Bewertung.", es="Aún no hay reseña.", ru="Отзыва пока нет.")
t("Timeline", fa="خط زمان", ar="الجدول الزمني", fr="Chronologie", de="Zeitlinie", es="Cronología", ru="Хронология")
t("No transitions yet.", fa="هنوز انتقالی نیست.", ar="لا توجد انتقالات بعد.", fr="Aucune transition pour l'instant.", de="Noch keine Übergänge.", es="Aún no hay transiciones.", ru="Переходов пока нет.")
t("Buzz history", fa="تاریخچه باز", ar="سجل التنبيهات", fr="Historique des buzz", de="Buzz-Verlauf", es="Historial de buzz", ru="История сигналов")
t("Unread", fa="خوانده‌نشده", ar="غير مقروء", fr="Non lu", de="Ungelesen", es="No leído", ru="Непрочитано")
t(
    "No buzzes yet. Use Buzz! when you need faster attention.",
    fa="هنوز بازی ثبت نشده. وقتی نیاز به توجه سریع‌تر دارید از باز! استفاده کنید.",
    ar="لا توجد تنبيهات بعد. استخدم تنبيه! عندما تحتاج انتباهاً أسرع.",
    fr="Aucun buzz pour l'instant. Utilisez Buzz ! pour une attention plus rapide.",
    de="Noch keine Buzzes. Nutzen Sie Buzz!, wenn Sie schnellere Aufmerksamkeit brauchen.",
    es="Aún no hay buzzes. Usa ¡Buzz! cuando necesites atención más rápida.",
    ru="Сигналов пока нет. Используйте «Сигнал!», когда нужно быстрее привлечь внимание.",
)
t("New emergency request-MyAutoHub", fa="درخواست اورژانسی جدید-MyAutoHub", ar="طلب طوارئ جديد-ماي أوتو هب", fr="Nouvelle demande d'urgence-MyAutoHub", de="Neue Notfallanfrage-MyAutoHub", es="Nueva solicitud de emergencia-MyAutoHub", ru="Новая аварийная заявка-MyAutoHub")
t("Request emergency help", fa="درخواست کمک اورژانسی", ar="طلب مساعدة طارئة", fr="Demander de l'aide d'urgence", de="Notfallhilfe anfordern", es="Pedir ayuda de emergencia", ru="Запросить аварийную помощь")
t(
    "Pick a service and tell us where you are-map pin or a saved location.",
    fa="یک خدمت انتخاب کنید و بگویید کجا هستید-پین نقشه یا مکان ذخیره‌شده.",
    ar="اختر خدمة وأخبرنا بموقعك-دبوس خريطة أو موقع محفوظ.",
    fr="Choisissez un service et indiquez où vous êtes-pin carte ou lieu enregistré.",
    de="Service wählen und Standort angeben-Kartenpin oder gespeicherter Ort.",
    es="Elige un servicio y dinos dónde estás-pin del mapa o ubicación guardada.",
    ru="Выберите услугу и укажите, где вы-метка на карте или сохранённое место.",
)
t("Location", fa="موقعیت", ar="الموقع", fr="Lieu", de="Standort", es="Ubicación", ru="Местоположение")
t("Latitude", fa="عرض جغرافیایی", ar="خط العرض", fr="Latitude", de="Breitengrad", es="Latitud", ru="Широта")
t("Longitude", fa="طول جغرافیایی", ar="خط الطول", fr="Longitude", de="Längengrad", es="Longitud", ru="Долгота")
t(
    "Tip: paste coordinates from your map app for now.",
    fa="نکته: فعلاً مختصات را از اپ نقشه کپی کنید.",
    ar="نصيحة: الصق الإحداثيات من تطبيق الخرائط حالياً.",
    fr="Astuce : collez pour l'instant les coordonnées depuis votre app carte.",
    de="Tipp: Koordinaten vorerst aus der Karten-App einfügen.",
    es="Consejo: por ahora pega las coordenadas desde tu app de mapas.",
    ru="Подсказка: пока вставьте координаты из картографического приложения.",
)
t("Saved location", fa="مکان ذخیره‌شده", ar="موقع محفوظ", fr="Lieu enregistré", de="Gespeicherter Ort", es="Ubicación guardada", ru="Сохранённое место")
t("Manage saved locations", fa="مدیریت مکان‌های ذخیره‌شده", ar="إدارة المواقع المحفوظة", fr="Gérer les lieux enregistrés", de="Gespeicherte Orte verwalten", es="Gestionar ubicaciones guardadas", ru="Управлять сохранёнными местами")
t("What happened?", fa="چه اتفاقی افتاد؟", ar="ماذا حدث؟", fr="Que s'est-il passé ?", de="Was ist passiert?", es="¿Qué pasó?", ru="Что случилось?")
t("Submit request", fa="ثبت درخواست", ar="إرسال الطلب", fr="Envoyer la demande", de="Anfrage senden", es="Enviar solicitud", ru="Отправить заявку")

# Pricing / marketplace / cars / youtube / stories
t("Pricing-MyAutoHub", fa="خدمات رایج-MyAutoHub", ar="الأسعار-ماي أوتو هب", fr="Tarifs-MyAutoHub", de="Preise-MyAutoHub", es="Precios-MyAutoHub", ru="Цены-MyAutoHub")
t("Pricing reference", fa="مرجع قیمت", ar="مرجع الأسعار", fr="Référence tarifaire", de="Preisreferenz", es="Referencia de precios", ru="Справочник цен")
t(
    "Ballpark figures for cars and common services-useful context, not a quote.",
    fa="اعداد تقریبی برای خودروها و خدمات رایج-زمینه مفید، نه پیشنهاد قیمت.",
    ar="أرقام تقريبية للسيارات والخدمات الشائعة-سياق مفيد وليس عرض سعر.",
    fr="Ordres de grandeur pour voitures et services courants-contexte utile, pas un devis.",
    de="Richtwerte für Autos und gängige Services-nützlicher Kontext, kein Angebot.",
    es="Cifras aproximadas para coches y servicios comunes-contexto útil, no un presupuesto.",
    ru="Ориентировочные цифры по авто и услугам-полезный контекст, не оферта.",
)
t("Title", fa="عنوان", ar="العنوان", fr="Titre", de="Titel", es="Título", ru="Название")
t("Category", fa="دسته", ar="الفئة", fr="Catégorie", de="Kategorie", es="Categoría", ru="Категория")
t("Amount", fa="مبلغ", ar="المبلغ", fr="Montant", de="Betrag", es="Importe", ru="Сумма")
t("Updated", fa="به‌روزرسانی", ar="محدّث", fr="Mis à jour", de="Aktualisiert", es="Actualizado", ru="Обновлено")
t("No pricing references published yet.", fa="هنوز مرجع قیمتی منتشر نشده.", ar="لم تُنشر مراجع أسعار بعد.", fr="Aucune référence tarifaire publiée pour l'instant.", de="Noch keine Preisreferenzen veröffentlicht.", es="Aún no hay referencias de precios.", ru="Справочники цен пока не опубликованы.")
t("General reference", fa="مرجع عمومی", ar="مرجع عام", fr="Référence générale", de="Allgemeine Referenz", es="Referencia general", ru="Общий справочник")
t("Back", fa="بازگشت", ar="رجوع", fr="Retour", de="Zurück", es="Volver", ru="Назад")
t("Marketplace-MyAutoHub", fa="بازار-MyAutoHub", ar="السوق-ماي أوتو هب", fr="Marché-MyAutoHub", de="Marktplatz-MyAutoHub", es="Mercado-MyAutoHub", ru="Маркетплейс-MyAutoHub")
t("Buy & sell", fa="خرید و فروش", ar="شراء وبيع", fr="Acheter et vendre", de="Kaufen & verkaufen", es="Comprar y vender", ru="Купить и продать")
t(
    "Towing, jump start, lockout-pin yourself on the map.",
    fa="یدک‌کش، جامپ‌استارت، قفل‌شدن-خودتان را روی نقشه پین کنید.",
    ar="قطر، تشغيل بالبطارية، فتح الأبواب-ثبّت موقعك على الخريطة.",
    fr="Remorquage, démarrage, ouverture-épinglez-vous sur la carte.",
    de="Abschleppen, Starthilfe, Aufsperren-pinne dich auf der Karte.",
    es="Grúa, arranque, apertura-pincha tu ubicación en el mapa.",
    ru="Эвакуатор, прикурить, вскрытие-отметьте себя на карте.",
)
t(
    "Specs and models-then jump to live marketplace deals.",
    fa="مشخصات و مدل‌ها-سپس به معاملات زنده بازار بروید.",
    ar="المواصفات والطرازات-ثم انتقل إلى صفقات السوق المباشرة.",
    fr="Fiches et modèles-puis passez aux offres live du marché.",
    de="Daten und Modelle-dann zu Live-Angeboten auf dem Marktplatz.",
    es="Fichas y modelos-luego pasa a ofertas en vivo del mercado.",
    ru="Характеристики и модели-затем к живым сделкам маркетплейса.",
)
t(
    "Browse cars from other drivers, or list yours.",
    fa="خودروهای دیگران را ببینید یا خودروی خود را آگهی کنید.",
    ar="تصفح سيارات السائقين الآخرين، أو أدرج سيارتك.",
    fr="Parcourez les voitures d'autres conducteurs, ou publiez la vôtre.",
    de="Autos anderer Fahrer durchsuchen oder Ihres inserieren.",
    es="Explora coches de otros conductores, o publica el tuyo.",
    ru="Смотрите авто других водителей или разместите своё.",
)
t(
    "Listings from people in the hub-browse openly, sell when you are ready.",
    fa="آگهی‌ها از افراد هاب-آزاد مرور کنید، وقتی آماده‌اید بفروشید.",
    ar="إعلانات من أشخاص في المركز-تصفح بحرية، وبِع عندما تكون جاهزاً.",
    fr="Annonces des membres du hub-parcourez librement, vendez quand vous êtes prêt.",
    de="Inserate von Menschen im Hub-offen browsen, verkaufen wenn Sie bereit sind.",
    es="Anuncios de personas del hub-explora libremente, vende cuando estés listo.",
    ru="Объявления людей из хаба-смотрите свободно, продавайте когда готовы.",
)
t("Sell a car", fa="فروش خودرو", ar="بيع سيارة", fr="Vendre une voiture", de="Auto verkaufen", es="Vender un coche", ru="Продать авто")
t("Log in to sell", fa="برای فروش وارد شوید", ar="سجّل الدخول للبيع", fr="Connectez-vous pour vendre", de="Anmelden zum Verkaufen", es="Inicia sesión para vender", ru="Войдите, чтобы продавать")
t("No active listings yet.", fa="هنوز آگهی فعالی نیست.", ar="لا توجد إعلانات نشطة بعد.", fr="Aucune annonce active pour l'instant.", de="Noch keine aktiven Inserate.", es="Aún no hay anuncios activos.", ru="Активных объявлений пока нет.")
t("Back to marketplace", fa="بازگشت به بازار", ar="العودة إلى السوق", fr="Retour au marché", de="Zurück zum Marktplatz", es="Volver al mercado", ru="Назад к маркетплейсу")
t("Sell a car-MyAutoHub", fa="فروش خودرو-MyAutoHub", ar="بيع سيارة-ماي أوتو هب", fr="Vendre une voiture-MyAutoHub", de="Auto verkaufen-MyAutoHub", es="Vender un coche-MyAutoHub", ru="Продать авто-MyAutoHub")
t("Create a listing", fa="ایجاد آگهی", ar="إنشاء إعلان", fr="Créer une annonce", de="Inserat erstellen", es="Crear un anuncio", ru="Создать объявление")
t(
    "Share what you are selling in plain language.",
    fa="آنچه می‌فروشید را به زبان ساده بنویسید.",
    ar="شارك ما تبيعه بلغة بسيطة.",
    fr="Décrivez ce que vous vendez en langage simple.",
    de="Beschreiben Sie Ihr Angebot in klarer Sprache.",
    es="Describe lo que vendes con claridad.",
    ru="Опишите то, что продаёте, простым языком.",
)
t("Publish listing", fa="انتشار آگهی", ar="نشر الإعلان", fr="Publier l'annonce", de="Inserat veröffentlichen", es="Publicar anuncio", ru="Опубликовать объявление")
t("Description", fa="توضیحات", ar="الوصف", fr="Description", de="Beschreibung", es="Descripción", ru="Описание")
t("Cover photo", fa="عکس کاور", ar="صورة الغلاف", fr="Photo de couverture", de="Titelbild", es="Foto de portada", ru="Обложка")
t("Price", fa="قیمت", ar="السعر", fr="Prix", de="Preis", es="Precio", ru="Цена")
t("Currency", fa="واحد پول", ar="العملة", fr="Devise", de="Währung", es="Moneda", ru="Валюта")
t("Year", fa="سال", ar="السنة", fr="Année", de="Jahr", es="Año", ru="Год")
t("Mileage (km)", fa="کارکرد (کیلومتر)", ar="المسافة المقطوعة (كم)", fr="Kilométrage (km)", de="Kilometerstand (km)", es="Kilometraje (km)", ru="Пробег (км)")
t("City", fa="شهر", ar="المدينة", fr="Ville", de="Stadt", es="Ciudad", ru="Город")
t("Brand", fa="برند", ar="العلامة", fr="Marque", de="Marke", es="Marca", ru="Бренд")
t("Model", fa="مدل", ar="الطراز", fr="Modèle", de="Modell", es="Modelo", ru="Модель")
t("Trim", fa="تریم", ar="الفئة", fr="Finition", de="Ausstattung", es="Acabado", ru="Комплектация")
t("Select brand", fa="انتخاب برند", ar="اختر العلامة", fr="Choisir une marque", de="Marke wählen", es="Elegir marca", ru="Выберите бренд")
t("Select model", fa="انتخاب مدل", ar="اختر الطراز", fr="Choisir un modèle", de="Modell wählen", es="Elegir modelo", ru="Выберите модель")
t(
    "Choose the car brand from the catalog (optional).",
    fa="برند خودرو را از کاتالوگ انتخاب کنید (اختیاری).",
    ar="اختر علامة السيارة من الكتالوج (اختياري).",
)
t(
    "Choose the model for the selected brand (optional).",
    fa="مدل برند انتخاب‌شده را برگزینید (اختیاری).",
    ar="اختر الطراز للعلامة المحددة (اختياري).",
)
t(
    "Trim or variant, e.g. SE, Limited (optional).",
    fa="تریم یا نسخه، مثل SE یا Limited (اختیاری).",
    ar="الفئة أو الطراز الفرعي مثل SE أو Limited (اختياري).",
)
t(
    "Selected model does not belong to the chosen brand.",
    fa="مدل انتخاب‌شده متعلق به این برند نیست.",
    ar="الطراز المحدد لا ينتمي إلى العلامة المختارة.",
)
t(
    "A short headline buyers will see first.",
    fa="عنوان کوتاهی که خریداران اول می‌بینند.",
    ar="عنوان قصير يراه المشترون أولاً.",
)
t(
    "Be honest and specific-it builds trust.",
    fa="صادق و مشخص باشید-اعتماد می‌سازد.",
    ar="كن صادقاً ومحدداً-هذا يبني الثقة.",
)
t(
    "Optional, but listings with a photo sell faster.",
    fa="اختیاری، اما آگهی با عکس سریع‌تر فروش می‌رود.",
    ar="اختياري، لكن الإعلانات مع صورة تُباع أسرع.",
)
t(
    "Ask a fair market price.",
    fa="قیمت منصفانه بازار را بگذارید.",
    ar="اطلب سعراً عادلاً في السوق.",
)
t(
    "3-letter code such as USD, IRR, AED.",
    fa="کد سه‌حرفی مثل USD، IRR، AED.",
    ar="رمز من 3 أحرف مثل USD أو IRR أو AED.",
)
t(
    "Model year (optional).",
    fa="سال ساخت (اختیاری).",
    ar="سنة الطراز (اختياري).",
)
t(
    "Odometer reading in kilometres (optional).",
    fa="عدد کیلومتر کارکرد (اختیاری).",
    ar="قراءة العداد بالكيلومتر (اختياري).",
)
t(
    "Where the car is located (optional).",
    fa="محل قرارگیری خودرو (اختیاری).",
    ar="مكان وجود السيارة (اختياري).",
)
t(
    "Active listings appear in the marketplace.",
    fa="آگهی‌های فعال در بازار نمایش داده می‌شوند.",
    ar="تظهر الإعلانات النشطة في السوق.",
)
t("e.g. 2018 Toyota Corolla", fa="مثلاً تویوتا کرولا ۲۰۱۸", ar="مثال: تويوتا كورولا 2018")
t(
    "Condition, extras, reason for selling…",
    fa="وضعیت، امکانات، دلیل فروش…",
    ar="الحالة، الإضافات، سبب البيع…",
)
t("e.g. Tehran", fa="مثلاً تهران", ar="مثال: طهران")
t("Listing steps", fa="مراحل آگهی", ar="خطوات الإعلان")
t("Basics", fa="اطلاعات پایه", ar="الأساسيات")
t("Specs", fa="مشخصات", ar="المواصفات")
t("Photo", fa="عکس", ar="صورة")
t("Describe the car", fa="خودرو را توصیف کنید", ar="صف السيارة")
t(
    "Add a title and description in at least one language. Other languages are optional.",
    fa="عنوان و توضیحات را حداقل در یک زبان بنویسید. زبان‌های دیگر اختیاری‌اند.",
    ar="أضف عنوانًا ووصفًا بلغة واحدة على الأقل. اللغات الأخرى اختيارية.",
)
t("Sell faster tip", fa="نکته فروش سریع‌تر", ar="نصيحة للبيع أسرع")
t(
    "MyAutoHub is an international platform. Completing all language fields (فارسی, English, and العربية) helps more buyers find your car-so you can sell sooner and often at a better price.",
    fa="MyAutoHub یک پلتفرم بین‌المللی است. پر کردن همه فیلدهای زبانی (فارسی، انگلیسی و عربی) کمک می‌کند خریداران بیشتری خودروی شما را پیدا کنند-تا زودتر و اغلب با قیمت بهتر بفروشید.",
    ar="ماي أوتو هب منصة دولية. إكمال حقول كل اللغات (الفارسية والإنجليزية والعربية) يساعد مزيدًا من المشترين على إيجاد سيارتك-فتبيع أسرع وغالبًا بسعر أفضل.",
)
t(
    "Add a title and description in at least one language (فارسی, English, or العربية).",
    fa="عنوان و توضیحات را حداقل در یک زبان بنویسید (فارسی، انگلیسی یا عربی).",
    ar="أضف عنوانًا ووصفًا بلغة واحدة على الأقل (الفارسية أو الإنجليزية أو العربية).",
)
t(
    "Start with a clear title and what buyers need to know.",
    fa="با عنوان واضح و آنچه خریدار باید بداند شروع کنید.",
    ar="ابدأ بعنوان واضح وما يحتاج المشتري معرفته.",
)
t("Specs & location", fa="مشخصات و مکان", ar="المواصفات والموقع")
t(
    "Optional details that help buyers filter and decide.",
    fa="جزئیات اختیاری که به فیلتر و تصمیم خریدار کمک می‌کند.",
    ar="تفاصيل اختيارية تساعد المشتري على التصفية والقرار.",
)
t("Add a cover photo", fa="عکس کاور اضافه کنید", ar="أضف صورة غلاف")
t(
    "A clear exterior shot works best. You can skip this for now.",
    fa="عکس واضح از بیرون بهترین است. فعلاً می‌توانید رد شوید.",
    ar="لقطة خارجية واضحة هي الأفضل. يمكنك التخطي الآن.",
)
t("Choose an image", fa="یک تصویر انتخاب کنید", ar="اختر صورة")
t("Set your price", fa="قیمت را مشخص کنید", ar="حدد سعرك")
t("Price & status", fa="قیمت و وضعیت", ar="السعر والحالة")
t(
    "Almost done-set a price and publish.",
    fa="تقریباً تمام-قیمت بگذارید و منتشر کنید.",
    ar="أوشكت على الانتهاء-حدد سعراً وانشر.",
)
t(
    "Adjust pricing or listing visibility.",
    fa="قیمت یا نمایش آگهی را تنظیم کنید.",
    ar="عدّل التسعير أو ظهور الإعلان.",
)
t("Continue", fa="ادامه", ar="متابعة")
t("Cars-MyAutoHub", fa="خودروها-MyAutoHub", ar="السيارات-ماي أوتو هب", fr="Voitures-MyAutoHub", de="Autos-MyAutoHub", es="Coches-MyAutoHub", ru="Автомобили-MyAutoHub")
t("Car catalog", fa="کاتالوگ خودرو", ar="كتالوج السيارات", fr="Catalogue de voitures", de="Autokatalog", es="Catálogo de coches", ru="Каталог автомобилей")
t(
    "Browse brands and models with the essentials-year, power, and trim.",
    fa="برندها و مدل‌ها را با ضروریات مرور کنید-سال، قدرت و تریم.",
    ar="تصفح العلامات والنماذج مع الأساسيات-السنة والقوة والتجهيز.",
    fr="Parcourez marques et modèles avec l'essentiel-année, puissance et finition.",
    de="Marken und Modelle mit dem Wesentlichen browsen-Jahr, Leistung und Ausstattung.",
    es="Explora marcas y modelos con lo esencial-año, potencia y acabado.",
    ru="Смотрите марки и модели с главным-год, мощность и комплектация.",
)
t("All", fa="همه", ar="الكل", fr="Tous", de="Alle", es="Todos", ru="Все")
t("No cars in the catalog yet.", fa="هنوز خودرویی در کاتالوگ نیست.", ar="لا توجد سيارات في الكتالوج بعد.", fr="Aucune voiture dans le catalogue pour l'instant.", de="Noch keine Autos im Katalog.", es="Aún no hay coches en el catálogo.", ru="В каталоге пока нет автомобилей.")
t("Back to catalog", fa="بازگشت به کاتالوگ", ar="العودة إلى الكتالوج", fr="Retour au catalogue", de="Zurück zum Katalog", es="Volver al catálogo", ru="Назад к каталогу")
t("YouTube-MyAutoHub", fa="یوتیوب-MyAutoHub", ar="يوتيوب-ماي أوتو هب", fr="YouTube-MyAutoHub", de="YouTube-MyAutoHub", es="YouTube-MyAutoHub", ru="YouTube-MyAutoHub")
t("YouTube contents", fa="محتوای یوتیوب", ar="محتويات يوتيوب", fr="Contenus YouTube", de="YouTube-Inhalte", es="Contenidos de YouTube", ru="Контент YouTube")
t(
    "Guides, reviews, and hub stories-watch without leaving the app.",
    fa="راهنماها، بررسی‌ها و داستان‌های هاب-بدون ترک اپ ببینید.",
    ar="أدلة ومراجعات وقصص المركز-شاهد دون مغادرة التطبيق.",
    fr="Guides, avis et histoires du hub-regardez sans quitter l'app.",
    de="Anleitungen, Reviews und Hub-Geschichten-ansehen ohne die App zu verlassen.",
    es="Guías, reseñas e historias del hub-mira sin salir de la app.",
    ru="Гайды, обзоры и истории хаба-смотрите, не покидая приложение.",
)
t("Recently added", fa="تازه‌افزوده‌شده", ar="أُضيف مؤخراً", fr="Ajouté récemment", de="Kürzlich hinzugefügt", es="Añadido recientemente", ru="Недавно добавлено")
t("No videos published yet.", fa="هنوز ویدیویی منتشر نشده.", ar="لم تُنشر فيديوهات بعد.", fr="Aucune vidéo publiée pour l'instant.", de="Noch keine Videos veröffentlicht.", es="Aún no hay vídeos publicados.", ru="Видео пока не опубликованы.")
t("Back to videos", fa="بازگشت به ویدیوها", ar="العودة إلى الفيديوهات", fr="Retour aux vidéos", de="Zurück zu den Videos", es="Volver a los vídeos", ru="Назад к видео")
t("Stories-MyAutoHub", fa="داستان‌ها-MyAutoHub", ar="القصص-ماي أوتو هب", fr="Histoires-MyAutoHub", de="Geschichten-MyAutoHub", es="Historias-MyAutoHub", ru="Истории-MyAutoHub")
t(
    "Human moments from the road and the MyAutoHub community.",
    fa="لحظات انسانی از جاده و جامعه MyAutoHub.",
    ar="لحظات إنسانية من الطريق ومجتمع ماي أوتو هب.",
    fr="Moments humains de la route et de la communauté MyAutoHub.",
    de="Menschliche Momente von der Straße und der MyAutoHub-Community.",
    es="Momentos humanos de la carretera y la comunidad MyAutoHub.",
    ru="Человеческие моменты с дороги и сообщества MyAutoHub.",
)
t("No stories published yet.", fa="هنوز داستانی منتشر نشده.", ar="لم تُنشر قصص بعد.", fr="Aucune histoire publiée pour l'instant.", de="Noch keine Geschichten veröffentlicht.", es="Aún no hay historias publicadas.", ru="Истории пока не опубликованы.")
t("Back to stories", fa="بازگشت به داستان‌ها", ar="العودة إلى القصص", fr="Retour aux histoires", de="Zurück zu den Geschichten", es="Volver a las historias", ru="Назад к историям")
t("Back to hub", fa="بازگشت به هاب", ar="العودة إلى المركز", fr="Retour au hub", de="Zurück zum Hub", es="Volver al hub", ru="Назад в хаб")

# Format strings
t("Emergency #%(id)s-MyAutoHub", fa="اورژانسی #%(id)s-MyAutoHub", ar="طوارئ #%(id)s-ماي أوتو هب", fr="Urgence #%(id)s-MyAutoHub", de="Notfall #%(id)s-MyAutoHub", es="Emergencia #%(id)s-MyAutoHub", ru="Авария #%(id)s-MyAutoHub")
t("Request #%(id)s", fa="درخواست #%(id)s", ar="طلب #%(id)s", fr="Demande #%(id)s", de="Anfrage #%(id)s", es="Solicitud #%(id)s", ru="Заявка #%(id)s")
t("Opened %(when)s", fa="باز شده %(when)s", ar="فُتح %(when)s", fr="Ouvert %(when)s", de="Eröffnet %(when)s", es="Abierto %(when)s", ru="Открыто %(when)s")
t("Requester: %(name)s", fa="درخواست‌کننده: %(name)s", ar="مقدّم الطلب: %(name)s", fr="Demandeur : %(name)s", de="Anforderer: %(name)s", es="Solicitante: %(name)s", ru="Заявитель: %(name)s")
t("Rating: %(rating)s/5", fa="امتیاز: %(rating)s/۵", ar="التقييم: %(rating)s/5", fr="Note : %(rating)s/5", de="Bewertung: %(rating)s/5", es="Valoración: %(rating)s/5", ru="Оценка: %(rating)s/5")
t("Buzz from %(name)s · %(when)s", fa="باز از %(name)s · %(when)s", ar="تنبيه من %(name)s · %(when)s", fr="Buzz de %(name)s · %(when)s", de="Buzz von %(name)s · %(when)s", es="Buzz de %(name)s · %(when)s", ru="Сигнал от %(name)s · %(when)s")
t("Source: %(source)s", fa="منبع: %(source)s", ar="المصدر: %(source)s", fr="Source : %(source)s", de="Quelle: %(source)s", es="Fuente: %(source)s", ru="Источник: %(source)s")
t("Updated %(when)s", fa="به‌روز شده %(when)s", ar="حُدّث %(when)s", fr="Mis à jour %(when)s", de="Aktualisiert %(when)s", es="Actualizado %(when)s", ru="Обновлено %(when)s")
t("Seller: %(name)s", fa="فروشنده: %(name)s", ar="البائع: %(name)s", fr="Vendeur : %(name)s", de="Verkäufer: %(name)s", es="Vendedor: %(name)s", ru="Продавец: %(name)s")
t("Year: %(year)s", fa="سال: %(year)s", ar="السنة: %(year)s", fr="Année : %(year)s", de="Jahr: %(year)s", es="Año: %(year)s", ru="Год: %(year)s")
t("By %(name)s · ", fa="از %(name)s · ", ar="بقلم %(name)s · ", fr="Par %(name)s · ", de="Von %(name)s · ", es="Por %(name)s · ", ru="Автор %(name)s · ")

# Global search
t("Search the hub…", fa="جستجو در هاب…", ar="ابحث في المركز…", fr="Rechercher dans le hub…", de="Im Hub suchen…", es="Buscar en el hub…", ru="Поиск по хабу…")
t("Search-MyAutoHub", fa="جستجو-MyAutoHub", ar="بحث-ماي أوتو هب", fr="Recherche-MyAutoHub", de="Suche-MyAutoHub", es="Buscar-MyAutoHub", ru="Поиск-MyAutoHub")
t(
    "Search: %(q)s-MyAutoHub",
    fa="جستجو: %(q)s-MyAutoHub",
    ar="بحث: %(q)s-ماي أوتو هب",
    fr="Recherche : %(q)s-MyAutoHub",
    de="Suche: %(q)s-MyAutoHub",
    es="Buscar: %(q)s-MyAutoHub",
    ru="Поиск: %(q)s-MyAutoHub",
)
t(
    "Find cars, listings, stories, videos, prices, and roadside help.",
    fa="خودروها، آگهی‌ها، داستان‌ها، ویدیوها، قیمت‌ها و کمک کنار جاده را پیدا کنید.",
    ar="اعثر على السيارات والإعلانات والقصص والفيديوهات والأسعار ومساعدة الطريق.",
    fr="Trouvez voitures, annonces, histoires, vidéos, tarifs et aide routière.",
    de="Finden Sie Autos, Anzeigen, Stories, Videos, Preise und Pannenhilfe.",
    es="Encuentra coches, anuncios, historias, vídeos, precios y ayuda en carretera.",
    ru="Найдите автомобили, объявления, истории, видео, цены и помощь на дороге.",
)
t(
    "No matches. Try another word or browse the hub.",
    fa="موردی پیدا نشد. واژه دیگری امتحان کنید یا هاب را مرور کنید.",
    ar="لا توجد نتائج. جرّب كلمة أخرى أو تصفّح المركز.",
    fr="Aucun résultat. Essayez un autre mot ou parcourez le hub.",
    de="Keine Treffer. Anderes Wort versuchen oder den Hub durchstöbern.",
    es="Sin coincidencias. Prueba otra palabra o explora el hub.",
    ru="Ничего не найдено. Попробуйте другое слово или просмотрите хаб.",
)
t("Browse all", fa="مشاهده همه", ar="عرض الكل", fr="Tout parcourir", de="Alle ansehen", es="Ver todo", ru="Смотреть все")
t("Roadside help", fa="کمک کنار جاده", ar="مساعدة على الطريق", fr="Aide routière", de="Pannenhilfe", es="Ayuda en carretera", ru="Помощь на дороге")

# --- Places / compact UI ---
t("Places", fa="مکان‌ها", ar="الأماكن", fr="Lieux", de="Orte", es="Lugares", ru="Места")
t("Network", fa="شبکه", ar="شبكة", fr="Réseau", de="Netzwerk", es="Red", ru="Сеть")
t("Find car dealers and repair shops on MyAutoHub.", fa="نمایندگی‌ها و تعمیرگاه‌ها را در مای‌اتوهاب پیدا کنید.", ar="اعثر على وكلاء السيارات وورش الإصلاح في ماي أوتو هاب.", fr="Trouvez concessionnaires et garages sur MyAutoHub.", de="Händler und Werkstätten auf MyAutoHub finden.", es="Encuentra concesionarios y talleres en MyAutoHub.", ru="Найдите дилеров и сервисы на MyAutoHub.")
t("Dealers and repair shops linked to brands in the catalog.", fa="نمایندگی‌ها و تعمیرگاه‌های مرتبط با برندهای کاتالوگ.", ar="وكلاء وورش مرتبطة بعلامات الكتالوج.", fr="Concessionnaires et garages liés aux marques du catalogue.", de="Händler und Werkstätten zu Katalogmarken.", es="Concesionarios y talleres vinculados a marcas del catálogo.", ru="Дилеры и сервисы, связанные с брендами каталога.")
t("Authorized & local dealers", fa="نمایندگی‌های مجاز و محلی", ar="وكلاء معتمدون ومحليون", fr="Concessionnaires agréés et locaux", de="Autorisierte und lokale Händler", es="Concesionarios autorizados y locales", ru="Официальные и местные дилеры")
t("Service & repair", fa="سرویس و تعمیر", ar="خدمة وإصلاح", fr="Service et réparation", de="Service und Reparatur", es="Servicio y reparación", ru="Сервис и ремонт")
t("No dealers published yet.", fa="هنوز نمایندگی منتشر نشده است.", ar="لا يوجد وكلاء منشورون بعد.", fr="Aucun concessionnaire publié.", de="Noch keine Händler veröffentlicht.", es="Aún no hay concesionarios publicados.", ru="Дилеры ещё не опубликованы.")
t("No repair shops published yet.", fa="هنوز تعمیرگاهی منتشر نشده است.", ar="لا توجد ورش منشورة بعد.", fr="Aucun garage publié.", de="Noch keine Werkstätten veröffentlicht.", es="Aún no hay talleres publicados.", ru="Сервисы ещё не опубликованы.")
t("Dealer", fa="نمایندگی", ar="وكيل", fr="Concessionnaire", de="Händler", es="Concesionario", ru="Дилер")
t("Repair shop", fa="تعمیرگاه", ar="ورشة إصلاح", fr="Garage", de="Werkstatt", es="Taller", ru="Сервис")
t("Dealers & repair shops", fa="نمایندگی‌ها و تعمیرگاه‌ها", ar="الوكلاء وورش الإصلاح", fr="Concessionnaires et garages", de="Händler und Werkstätten", es="Concesionarios y talleres", ru="Дилеры и сервисы")
t("Contact", fa="تماس", ar="اتصل", fr="Contact", de="Kontakt", es="Contacto", ru="Контакты")
t("Phone", fa="تلفن", ar="الهاتف", fr="Téléphone", de="Telefon", es="Teléfono", ru="Телефон")
t("Website", fa="وب‌سایت", ar="الموقع", fr="Site web", de="Webseite", es="Sitio web", ru="Сайт")
t("Address", fa="آدرس", ar="العنوان", fr="Adresse", de="Adresse", es="Dirección", ru="Адрес")
t("All places", fa="همه مکان‌ها", ar="كل الأماكن", fr="Tous les lieux", de="Alle Orte", es="Todos los lugares", ru="Все места")
t("Explore more", fa="بیشتر ببینید", ar="استكشف المزيد", fr="Explorer plus", de="Mehr entdecken", es="Explorar más", ru="Смотреть ещё")
t("Browse other dealers, shops, and catalog models.", fa="نمایندگی‌ها، تعمیرگاه‌ها و مدل‌های کاتالوگ دیگر را ببینید.", ar="تصفّح وكلاء وورش ونماذج كتالوج أخرى.", fr="Parcourez d’autres lieux et modèles.", de="Weitere Orte und Modelle ansehen.", es="Explora más lugares y modelos.", ru="Смотрите другие места и модели.")
t("Sections", fa="بخش‌ها", ar="الأقسام", fr="Sections", de="Abschnitte", es="Secciones", ru="Разделы")
t("Specs", fa="مشخصات", ar="المواصفات", fr="Specs", de="Specs", es="Specs", ru="Характеристики")
t("Technical", fa="فنی", ar="تقني", fr="Technique", de="Technik", es="Técnico", ru="Техника")
t("Body", fa="بدنه", ar="الهيكل", fr="Carrosserie", de="Karosserie", es="Carrocería", ru="Кузов")
t("Equipment", fa="تجهیزات", ar="التجهيزات", fr="Équipement", de="Ausstattung", es="Equipamiento", ru="Оснащение")
t("Care", fa="نگهداری", ar="العناية", fr="Entretien", de="Pflege", es="Cuidado", ru="Уход")
t("Service", fa="سرویس", ar="الخدمة", fr="Service", de="Service", es="Servicio", ru="Сервис")
t("OBD", fa="OBD", ar="OBD", fr="OBD", de="OBD", es="OBD", ru="OBD")
t("Shops", fa="تعمیرگاه‌ها", ar="الورش", fr="Garages", de="Werkstätten", es="Talleres", ru="Сервисы")
t("Engine", fa="موتور", ar="المحرك", fr="Moteur", de="Motor", es="Motor", ru="Двигатель")
t("Displacement", fa="حجم موتور", ar="السعة", fr="Cylindrée", de="Hubraum", es="Cilindrada", ru="Объём")
t("Cylinders", fa="سیلندر", ar="الأسطوانات", fr="Cylindres", de="Zylinder", es="Cilindros", ru="Цилиндры")
t("Transmission", fa="گیربکس", ar="ناقل الحركة", fr="Transmission", de="Getriebe", es="Transmisión", ru="КПП")
t("Drivetrain", fa="محور محرک", ar="نظام الدفع", fr="Transmission", de="Antrieb", es="Tracción", ru="Привод")
t("Top speed", fa="حداکثر سرعت", ar="السرعة القصوى", fr="Vitesse max", de="Höchstgeschwindigkeit", es="Velocidad máx.", ru="Макс. скорость")
t("Emissions", fa="آلایندگی", ar="الانبعاثات", fr="Émissions", de="Emissionen", es="Emisiones", ru="Выбросы")
t("Length", fa="طول", ar="الطول", fr="Longueur", de="Länge", es="Longitud", ru="Длина")
t("Width", fa="عرض", ar="العرض", fr="Largeur", de="Breite", es="Ancho", ru="Ширина")
t("Height", fa="ارتفاع", ar="الارتفاع", fr="Hauteur", de="Höhe", es="Altura", ru="Высота")
t("Weight", fa="وزن", ar="الوزن", fr="Poids", de="Gewicht", es="Peso", ru="Масса")
t("Cargo", fa="صندوق", ar="الحمولة", fr="Coffre", de="Kofferraum", es="Maletero", ru="Багажник")
t("Seats", fa="صندلی", ar="المقاعد", fr="Sièges", de="Sitze", es="Asientos", ru="Сиденья")
t("Clearance", fa="ارتفاع از زمین", ar="الخلوص", fr="Garde au sol", de="Bodenfreiheit", es="Despeje", ru="Клиренс")
t("Tank", fa="باک", ar="الخزان", fr="Réservoir", de="Tank", es="Depósito", ru="Бак")
t("Battery", fa="باتری", ar="البطارية", fr="Batterie", de="Batterie", es="Batería", ru="АКБ")
t("Keep exploring", fa="ادامه کاوش", ar="واصل الاستكشاف", fr="Continuer", de="Weiter entdecken", es="Seguir explorando", ru="Продолжить")
t("Compare more models or browse cars for sale.", fa="مدل‌های بیشتر را مقایسه کنید یا خودروهای فروش را ببینید.", ar="قارن نماذج أكثر أو تصفّح سيارات للبيع.", fr="Comparez d’autres modèles ou parcourez les annonces.", de="Weitere Modelle vergleichen oder Angebote ansehen.", es="Compara más modelos o mira coches en venta.", ru="Сравните модели или смотрите объявления.")
t("Account", fa="حساب", ar="الحساب", fr="Compte", de="Konto", es="Cuenta", ru="Аккаунт")
t("Hub", fa="هاب", ar="المركز", fr="Hub", de="Hub", es="Hub", ru="Хаб")
t(
    "Find cars, listings, stories, videos, prices, places, and roadside help.",
    fa="خودرو، آگهی، داستان، ویدیو، قیمت، مکان و کمک کنار جاده را پیدا کنید.",
    ar="اعثر على سيارات وإعلانات وقصص وفيديوهات وأسعار وأماكن ومساعدة الطريق.",
    fr="Trouvez voitures, annonces, histoires, vidéos, prix, lieux et aide routière.",
    de="Finde Autos, Inserate, Stories, Videos, Preise, Orte und Pannenhilfe.",
    es="Encuentra coches, anuncios, historias, vídeos, precios, lugares y ayuda.",
    ru="Ищите авто, объявления, истории, видео, цены, места и помощь.",
)
t("City", fa="شهر", ar="المدينة", fr="Ville", de="Stadt", es="Ciudad", ru="Город")
t("Highway", fa="جاده", ar="الطريق السريع", fr="Autoroute", de="Autobahn", es="Autopista", ru="Трасса")

tp(
    "%(counter)s result for “%(q)s”",
    "%(counter)s results for “%(q)s”",
    fa=("%(counter)s نتیجه برای «%(q)s»", "%(counter)s نتیجه برای «%(q)s»"),
    ar=("%(counter)s نتيجة لـ «%(q)s»", "%(counter)s نتيجة لـ «%(q)s»", "%(counter)s نتيجتان لـ «%(q)s»", "%(counter)s نتائج لـ «%(q)s»", "%(counter)s نتيجة لـ «%(q)s»", "%(counter)s نتيجة لـ «%(q)s»"),
    fr=("%(counter)s résultat pour « %(q)s »", "%(counter)s résultats pour « %(q)s »"),
    de=("%(counter)s Treffer für „%(q)s“", "%(counter)s Treffer für „%(q)s“"),
    es=("%(counter)s resultado para “%(q)s”", "%(counter)s resultados para “%(q)s”"),
    ru=("%(counter)s результат для «%(q)s»", "%(counter)s результата для «%(q)s»", "%(counter)s результатов для «%(q)s»", "%(counter)s результатов для «%(q)s»"),
)

# Plurals (msgid_plural forms)
tp(
    "%(counter)s new",
    "%(counter)s new",
    fa=("%(counter)s جدید", "%(counter)s جدید"),
    ar=("%(counter)s جديد", "%(counter)s جديد", "%(counter)s جديد", "%(counter)s جديدة", "%(counter)s جديد", "%(counter)s جديد"),
    fr=("%(counter)s nouveau", "%(counter)s nouveaux"),
    de=("%(counter)s neu", "%(counter)s neu"),
    es=("%(counter)s nuevo", "%(counter)s nuevos"),
    ru=("%(counter)s новый", "%(counter)s новых", "%(counter)s новых", "%(counter)s новых"),
)
tp(
    "%(counter)s unread buzz",
    "%(counter)s unread buzzes",
    fa=("%(counter)s باز خوانده‌نشده", "%(counter)s باز خوانده‌نشده"),
    ar=("%(counter)s تنبيه غير مقروء", "%(counter)s تنبيه غير مقروء", "%(counter)s تنبيهان غير مقروءين", "%(counter)s تنبيهات غير مقروءة", "%(counter)s تنبيهاً غير مقروء", "%(counter)s تنبيه غير مقروء"),
    fr=("%(counter)s buzz non lu", "%(counter)s buzz non lus"),
    de=("%(counter)s ungelesener Buzz", "%(counter)s ungelesene Buzzes"),
    es=("%(counter)s buzz sin leer", "%(counter)s buzzes sin leer"),
    ru=("%(counter)s непрочитанный сигнал", "%(counter)s непрочитанных сигнала", "%(counter)s непрочитанных сигналов", "%(counter)s непрочитанных сигналов"),
)

t("No inquiries yet.", fa="هنوز پیامی نیست.", ar="لا توجد استفسارات بعد.")
t(
    "Moderate buy & sell listings. Titles and descriptions support FA / EN / AR.",
    fa="آگهی‌های خرید و فروش را مدیریت کنید. عنوان و توضیح از فارسی / انگلیسی / عربی پشتیبانی می‌کنند.",
    ar="أدِر إعلانات البيع والشراء. العناوين والأوصاف تدعم FA / EN / AR.",
)
t("Create a multilingual marketplace listing.", fa="یک آگهی چندزبانه برای بازار بسازید.", ar="أنشئ إعلاناً متعدد اللغات للسوق.")
t("Create listing", fa="ایجاد آگهی", ar="إنشاء إعلان")
t("Buyer messages on marketplace listings.", fa="پیام‌های خریداران روی آگهی‌های بازار.", ar="رسائل المشترين على إعلانات السوق.")
t("Reference prices with FA / EN / AR titles and notes.", fa="قیمت‌های مرجع با عنوان و یادداشت فارسی / انگلیسی / عربی.", ar="أسعار مرجعية بعناوين وملاحظات FA / EN / AR.")
t("Add a multilingual price reference.", fa="یک قیمت مرجع چندزبانه اضافه کنید.", ar="أضف سعراً مرجعياً متعدد اللغات.")
t("Create price", fa="ایجاد قیمت", ar="إنشاء سعر")
t("Listing", fa="آگهی", ar="إعلان")
t("Buyer", fa="خریدار", ar="المشتري")
t("Message", fa="پیام", ar="الرسالة")
t("Read", fa="خوانده‌شده", ar="مقروء")
t("Yes", fa="بله", ar="نعم")
t("No", fa="خیر", ar="لا")
t("OBD codes", fa="کدهای OBD", ar="رموز OBD")
t("Amount", fa="مبلغ", ar="المبلغ")
t("Category", fa="دسته", ar="الفئة")
t("Seller", fa="فروشنده", ar="البائع")
t("Status", fa="وضعیت", ar="الحالة")
t("Price", fa="قیمت", ar="السعر")

t(
    "Filter by country, brand, model, trim, fuel, power, transmission, or seats. Open a car for full specs.",
    fa="با کشور، برند، مدل، تریم، سوخت، قدرت، گیربکس یا صندلی فیلتر کنید. خودرو را برای مشخصات کامل باز کنید.",
    ar="صفِّ حسب الدولة أو العلامة أو النموذج أو الفئة أو الوقود أو القوة أو ناقل الحركة أو المقاعد. افتح سيارة للمواصفات الكاملة.",
)
t("All trims", fa="همه تریم‌ها", ar="كل الفئات")
t("Trim", fa="تریم", ar="الفئة")
t("All manufacturers", fa="همه سازندگان", ar="كل الشركات المصنعة")
t("Manufacturer", fa="سازنده", ar="الشركة المصنعة")
t("All transmissions", fa="همه گیربکس‌ها", ar="كل نواقل الحركة")
t("Transmission", fa="گیربکس", ar="ناقل الحركة")
t("Automatic", fa="اتوماتیک", ar="أوتوماتيك")
t("Manual", fa="دستی", ar="يدوي")
t("CVT", fa="CVT", ar="CVT")
t("All drivetrains", fa="همه سامانه‌های انتقال قدرت", ar="كل أنظمة الدفع")
t("Drivetrain", fa="محور محرک", ar="نظام الدفع")
t("FWD", fa="دیفرانسیل جلو", ar="دفع أمامي")
t("RWD", fa="دیفرانسیل عقب", ar="دفع خلفي")
t("AWD / 4WD", fa="چهار چرخ محرک", ar="دفع رباعي")
t("Any seats", fa="هر تعداد صندلی", ar="أي عدد مقاعد")
t("Seats", fa="صندلی", ar="المقاعد")
t("2 seats", fa="۲ صندلی", ar="مقعدان")
t("4 seats", fa="۴ صندلی", ar="٤ مقاعد")
t("5 seats", fa="۵ صندلی", ar="٥ مقاعد")
t("7+ seats", fa="۷+ صندلی", ar="٧+ مقاعد")
t("HP from", fa="حداقل اسب بخار", ar="الحد الأدنى للقوة")
t("HP to", fa="حداکثر اسب بخار", ar="الحد الأقصى للقوة")
t("Horsepower", fa="اسب بخار", ar="القوة الحصانية")
t("Horsepower from", fa="حداقل اسب بخار", ar="القوة من")
t("Horsepower to", fa="حداکثر اسب بخار", ar="القوة إلى")
t("Power (low → high)", fa="قدرت (کم → زیاد)", ar="القوة (من الأقل إلى الأعلى)")
t("Min", fa="حداقل", ar="الحد الأدنى")
t("Max", fa="حداکثر", ar="الحد الأقصى")

t("Back to top", fa="بازگشت به بالا", ar="العودة للأعلى")

LANGS = ("fa", "ar", "en")
NPLURALS = {"fa": 2, "ar": 6, "en": 2}


def fill_lang(lang: str) -> None:
    path = f"locale/{lang}/LC_MESSAGES/django.po"
    po = polib.pofile(path)
    po.metadata["Language"] = lang
    missing = []
    for entry in po:
        if not entry.msgid:
            continue
        if entry.msgid_plural:
            forms = PLURAL.get(entry.msgid, {}).get(lang)
            if lang == "en":
                entry.msgstr_plural = {0: entry.msgid, 1: entry.msgid_plural}
                for i in range(2, NPLURALS[lang]):
                    entry.msgstr_plural[i] = entry.msgid_plural
            elif forms:
                n = NPLURALS[lang]
                # pad with last form if needed
                padded = list(forms) + [forms[-1]] * max(0, n - len(forms))
                entry.msgstr_plural = {i: padded[i] for i in range(n)}
            else:
                missing.append(entry.msgid)
            continue
        if lang == "en":
            entry.msgstr = entry.msgid
            if "fuzzy" in entry.flags:
                entry.flags = [f for f in entry.flags if f != "fuzzy"]
            continue
        trans = SINGULAR.get(entry.msgid, {}).get(lang)
        if trans is None:
            missing.append(entry.msgid)
        else:
            entry.msgstr = trans
            if "fuzzy" in entry.flags:
                entry.flags = [f for f in entry.flags if f != "fuzzy"]
    po.save(path)
    print(f"{lang}: missing={len(missing)}")
    for m in missing:
        print(f"  {m!r}")


if __name__ == "__main__":
    for lang in LANGS:
        fill_lang(lang)
