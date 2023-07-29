from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username


def CreateUserProfile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()

post_save.connect(CreateUserProfile, sender=User)


class Usercreatedpage(models.Model):
    page_name = models.CharField(max_length=255, unique=True)
    page_description = models.TextField(blank=True)
    theme_photo = models.ImageField(null=True, blank=True)
    location = models.CharField(max_length=255)
    user = models.ForeignKey(User,
                             related_name="pages",
                             on_delete=models.DO_NOTHING,
                             default=1)
    business_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.page_name

    def get_absolute_url(self):
        return reverse("wriber", kwargs={"pk": self.pk})


class User_Page(models.Model):
    page = models.OneToOneField(Usercreatedpage, on_delete=models.CASCADE)

    def __str__(self):
        return self.page.page_name


def CreateUserPage(sender, instance, created, **kwargs):
    if created:
        user_page = User_Page(page=instance)
        user_page.save()

post_save.connect(CreateUserPage, sender=Usercreatedpage)


class Product_info(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.FloatField()
    stock_available = models.IntegerField()
    image_url = models.ImageField(null=True, blank=True)
    image_url2 = models.ImageField(null=True, blank=True, default='no-photo.png')
    image_url3 = models.ImageField(null=True, blank=True, default='no-photo.png')
    image_url4 = models.ImageField(null=True, blank=True, default='no-photo.png')
    product_description = models.TextField(null=True, max_length=2600)
    user = models.ForeignKey(User, related_name="products", on_delete=models.DO_NOTHING, default=1)
    page_owner = models.ForeignKey(Usercreatedpage,
                                   related_name="Userproducts",
                                   on_delete=models.DO_NOTHING,
                                   blank=True,
                                   null=True,
                                   default=1)

    def get_absolute_url(self):
        return reverse("wriber-viewproducts", kwargs={"pk": self.pk})

    def __str__(self):
        return self.product_name


class Service_info(models.Model):
    service_name = models.CharField(max_length=255)
    service_price = models.FloatField()
    location = models.CharField(max_length=255)
    image_url = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="services", on_delete=models.DO_NOTHING, default=1)
    page_owner = models.ForeignKey(Usercreatedpage,
                                   related_name="Userservices",
                                   on_delete=models.DO_NOTHING,
                                   default=1)

    def get_absolute_url(self):
        return reverse("wriber-viewservices", kwargs={"pk": self.pk})


class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    paid_amount = models.IntegerField(blank=True, null=True)
    merchant_id = models.CharField(max_length=255, null=True)
    created_by = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    message = models.TextField(max_length=2000, null=True)
    phone_number = models.IntegerField(null=True)

    def get_absolute_url(self):
        return reverse("order-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.first_name


class Ordered(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.order.first_name


def CreateOrder(sender, instance, created, **kwargs):
    if created:
        ordered = Ordered(order=instance)
        ordered.save()

post_save.connect(CreateOrder, sender=Order)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderfrom', null=True, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product_info, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.product_name


class Tariffs(models.Model):
    name = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User,
                             related_name="tariff",
                             on_delete=models.DO_NOTHING,
                             default=1)
    page_owner = models.ForeignKey(Usercreatedpage,
                                   related_name="tariff_page_owner",
                                   on_delete=models.DO_NOTHING,
                                   blank=True,
                                   null=True,
                                   default=1)

    def get_absolute_url(self):
        return reverse("tariff-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Tariff_query(models.Model):
    tariff = models.OneToOneField(Tariffs, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("tariff-page", kwargs={"pk": self.pk})

    def __str__(self):
        return self.tariff.user.username


def CreateTariff(sender, instance, created, **kwargs):
    if created:
        user_tariff = Tariff_query(tariff=instance)
        user_tariff.save()

post_save.connect(CreateTariff, sender=Tariffs)


class location_gambia(models.Model):
    abuko = models.IntegerField(null=True, blank=True)
    brufut_Taf = models.IntegerField(null=True, blank=True)
    brufut_heights = models.IntegerField(null=True, blank=True)
    brikama = models.IntegerField(null=True, blank=True)
    barra = models.IntegerField(null=True, blank=True)
    banjul = models.IntegerField(null=True, blank=True)
    bakau = models.IntegerField(null=True, blank=True)
    batokunku = models.IntegerField(null=True, blank=True)
    brusubi = models.IntegerField(null=True, blank=True)
    bijilo = models.IntegerField(null=True, blank=True)
    busumbala = models.IntegerField(null=True, blank=True)
    banjulinding = models.IntegerField(null=True, blank=True)
    bundung = models.IntegerField(null=True, blank=True)
    bakoteh = models.IntegerField(null=True, blank=True)
    churchill_Town = models.IntegerField(null=True, blank=True)
    coastal_Road = models.IntegerField(null=True, blank=True)
    dippa_kunda = models.IntegerField(null=True, blank=True)
    dalaba_estate = models.IntegerField(null=True, blank=True)
    ebou_town = models.IntegerField(null=True, blank=True)
    fajara = models.IntegerField(null=True, blank=True)
    farato = models.IntegerField(null=True, blank=True)
    pipline = models.IntegerField(null=True, blank=True)
    faraba = models.IntegerField(null=True, blank=True)
    faji_kunda = models.IntegerField(null=True, blank=True)
    gunjur = models.IntegerField(null=True, blank=True)
    jabang = models.IntegerField(null=True, blank=True)
    jimpex = models.IntegerField(null=True, blank=True)
    jamburr = models.IntegerField(null=True, blank=True)
    jambanjelly = models.IntegerField(null=True, blank=True)
    kanifing = models.IntegerField(null=True, blank=True)
    kartong = models.IntegerField(null=True, blank=True)
    kotu = models.IntegerField(null=True, blank=True)
    kololi = models.IntegerField(null=True, blank=True)
    kerr_sering = models.IntegerField(null=True, blank=True)
    latriya = models.IntegerField(null=True, blank=True)
    lamin = models.IntegerField(null=True, blank=True)
    latrikunda_german = models.IntegerField(null=True, blank=True)
    latrikunda_sabigi = models.IntegerField(null=True, blank=True)
    manjai = models.IntegerField(null=True, blank=True)
    mariamakunda = models.IntegerField(null=True, blank=True)
    marakesa = models.IntegerField(null=True, blank=True)
    madinabaa = models.IntegerField(null=True, blank=True)
    madinari = models.IntegerField(null=True, blank=True)
    madiyana = models.IntegerField(null=True, blank=True)
    nema_su = models.IntegerField(null=True, blank=True)
    new_jeshwang = models.IntegerField(null=True, blank=True)
    old_jeshwang = models.IntegerField(null=True, blank=True)
    old_yundum = models.IntegerField(null=True, blank=True)
    paradise_view = models.IntegerField(null=True, blank=True)
    paradise_estate = models.IntegerField(null=True, blank=True)
    salaji = models.IntegerField(null=True, blank=True)
    sanchaba = models.IntegerField(null=True, blank=True)
    serekunda = models.IntegerField(null=True, blank=True)
    senegambia = models.IntegerField(null=True, blank=True)
    sinchu = models.IntegerField(null=True, blank=True)
    sukuta = models.IntegerField(null=True, blank=True)
    sanyang = models.IntegerField(null=True, blank=True)
    turntable = models.IntegerField(null=True, blank=True)
    traffic_lights = models.IntegerField(null=True, blank=True)
    tallinding = models.IntegerField(null=True, blank=True)
    tabokoto = models.IntegerField(null=True, blank=True)
    tipper_garage = models.IntegerField(null=True, blank=True)
    tanji = models.IntegerField(null=True, blank=True)
    tujereng = models.IntegerField(null=True, blank=True)
    wulinkama = models.IntegerField(null=True, blank=True)
    westfield = models.IntegerField(null=True, blank=True)
    yundum = models.IntegerField(null=True, blank=True)
    yuna = models.IntegerField(null=True, blank=True)
    yarambamba = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="user_tariff", on_delete=models.DO_NOTHING, default=1)
    tariff_owner = models.ForeignKey(Tariffs, related_name="page_tariff", on_delete=models.DO_NOTHING, blank=True,
                                     null=True, default=1)
    page_owner = models.ForeignKey(Usercreatedpage, related_name="locations_page",
                                   on_delete=models.DO_NOTHING,
                                   blank=True,
                                   null=True,
                                   default=1)

    def get_absolute_url(self):
        return reverse("tariff-detail", kwargs={"pk": self.pk})


#class feedback(models.Model):
    #name = models.CharField(max_length=255)
    #email = models.EmailField()
    #feedback = models.TextField()

    #def __str__(self):
        #return self.name



# the application ordering system will never work till i make every 'orderitem' specific to every order. ITS OFFICIALLY DONE!!!!