# Generated by Django 4.0.5 on 2022-06-07 09:11

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instaclone', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='opinion',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='following',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='user',
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='date_updated',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='date_updated',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='email_confirmed',
        ),
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='pub_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='follow',
            name='followed',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='profile_followed', to='instaclone.profile'),
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='profile_following', to='instaclone.profile'),
        ),
        migrations.AddField(
            model_name='follow',
            name='posted',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='posts', to='instaclone.profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='instaclone.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.CharField(max_length=2200),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instaclone.profile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
