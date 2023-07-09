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
    abuko = models.IntegerField()
    brufut_Taf = models.IntegerField()
    brufut_heights = models.IntegerField()
    brikama = models.IntegerField()
    barra = models.IntegerField()
    banjul = models.IntegerField()
    bakau = models.IntegerField()
    batokunku = models.IntegerField()
    brusubi = models.IntegerField()
    bijilo = models.IntegerField()
    busumbala = models.IntegerField()
    banjulinding = models.IntegerField()
    bundung = models.IntegerField()
    bakoteh = models.IntegerField()
    churchill_Town = models.IntegerField()
    coastal_Road = models.IntegerField()
    dippa_kunda = models.IntegerField()
    dalaba_estate = models.IntegerField()
    ebou_town = models.IntegerField()
    fajara = models.IntegerField()
    farato = models.IntegerField()
    pipline = models.IntegerField()
    faraba = models.IntegerField()
    faji_kunda = models.IntegerField()
    gunjur = models.IntegerField()
    jabang = models.IntegerField()
    jimpex = models.IntegerField()
    jamburr = models.IntegerField()
    jambanjelly = models.IntegerField()
    kanifing = models.IntegerField()
    kartong = models.IntegerField()
    kotu = models.IntegerField()
    kololi = models.IntegerField()
    kerr_sering = models.IntegerField()
    latriya = models.IntegerField()
    lamin = models.IntegerField()
    latrikunda_german = models.IntegerField()
    latrikunda_sabigi = models.IntegerField()
    manjai = models.IntegerField()
    mariamakunda = models.IntegerField()
    marakesa = models.IntegerField()
    madinabaa = models.IntegerField()
    madinari = models.IntegerField()
    madiyana = models.IntegerField()
    nema_su = models.IntegerField()
    new_jeshwang = models.IntegerField()
    old_jeshwang = models.IntegerField()
    old_yundum = models.IntegerField()
    paradise_view = models.IntegerField()
    paradise_estate = models.IntegerField()
    salaji = models.IntegerField()
    sanchaba = models.IntegerField()
    serekunda = models.IntegerField()
    senegambia = models.IntegerField()
    sinchu = models.IntegerField()
    sukuta = models.IntegerField()
    sanyang = models.IntegerField()
    turntable = models.IntegerField()
    traffic_lights = models.IntegerField()
    tallinding = models.IntegerField()
    tabokoto = models.IntegerField()
    tipper_garage = models.IntegerField()
    tanji = models.IntegerField()
    tujereng = models.IntegerField()
    wulinkama = models.IntegerField()
    westfield = models.IntegerField()
    yundum = models.IntegerField()
    yuna = models.IntegerField()
    yarambamba = models.IntegerField()
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