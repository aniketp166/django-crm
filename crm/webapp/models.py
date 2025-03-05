from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class Record(models.Model):
    COUNTRY_CHOICES = [
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('UK', 'United Kingdom'),
        # Add more countries as needed
    ]

    creation_date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100, validators=[
        RegexValidator(
            regex=r'^[A-Za-z\s-]+$',
            message='First name can only contain letters, spaces, and hyphens'
        )
    ])
    last_name = models.CharField(max_length=100, validators=[
        RegexValidator(
            regex=r'^[A-Za-z\s-]+$',
            message='Last name can only contain letters, spaces, and hyphens'
        )
    ])
    email = models.EmailField(
        max_length=255,
        unique=True,
        validators=[EmailValidator()]
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Enter a valid phone number'
            )
        ]
    )
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(
        max_length=125,
        choices=COUNTRY_CHOICES,
        default='US'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-creation_date']
        verbose_name_plural = "Records"
