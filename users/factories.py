# # pip install factory_boy

# from .models import CustomUser, UserProfile, PremiumSubscription, Payment

# class CustomUserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = CustomUser
    
#     username = factory.Sequence(lambda n: f"user{n}")
#     first_name = "FirstName"
#     last_name = "LastName"
#     email = factory.Sequence(lambda n: f"user{n}@example.com")
#     password = factory.PostGenerationMethodCall("set_password", "defaultpassword")
#     is_active = True

# class UserProfileFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = UserProfile
    
#     user = factory.SubFactory(CustomUserFactory)
#     phone = factory.Sequence(lambda n: f"09123456{n}")
#     address = "Some Address"
#     gender = "other"
#     bio = "This is a bio"

# class PremiumSubscriptionFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = PremiumSubscription
    
#     user = factory.SubFactory(CustomUserFactory)
#     start_date = factory.Faker('date_time')
#     end_date = factory.Faker('date_time')

# class PaymentFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Payment
    
#     user = factory.SubFactory(CustomUserFactory)
#     payment_id = factory.Sequence(lambda n: f"payment{n}")
#     amount = 100.00
#     payment_status = "completed"
#     payment_date = factory.Faker('date_time')
