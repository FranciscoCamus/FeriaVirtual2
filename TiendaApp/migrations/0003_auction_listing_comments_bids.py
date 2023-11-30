# Generated by Django 4.2.2 on 2023-11-12 02:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TiendaApp', '0002_producto_created_producto_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction_listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('starting_bid', models.DecimalField(decimal_places=2, default=0, max_digits=17)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('img_url', models.CharField(blank=True, help_text='Optional', max_length=256, null=True)),
                ('active_status', models.BooleanField(default=True)),
                ('category', models.CharField(choices=[('FA', 'Fashion'), ('BM', 'Books, Moves & Music'), ('EL', 'Electronics'), ('CO', 'Collectibles & Art'), ('HG', 'Home & Garden'), ('SG', 'Sporting Goods'), ('TH', 'Toys & Hobbies'), ('BI', 'Business & Industrial'), ('HB', 'Health & Beauty'), ('OT', 'Others')], default='OT', help_text='If not specified it will be set as Others', max_length=2)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('watchlist', models.ManyToManyField(blank=True, related_name='user_watchlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-creation_date',),
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentary_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(null=True)),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_comments', to='TiendaApp.auction_listing')),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('listing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='listing_bid', serialize=False, to='TiendaApp.auction_listing')),
                ('highest_bid', models.DecimalField(decimal_places=2, default=0, max_digits=17)),
                ('last_bid_date', models.DateTimeField(auto_now=True)),
                ('highest_bid_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('last_bid_date',),
            },
        ),
    ]
