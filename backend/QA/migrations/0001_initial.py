# Generated by Django 2.0 on 2017-12-23 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approve', models.IntegerField(default=0, verbose_name='赞同数')),
                ('against', models.IntegerField(default=0, verbose_name='反对数')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('detail', models.TextField(verbose_name='描述')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answered', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('detail', models.TextField(verbose_name='描述')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=20)),
                ('introduction', models.TextField()),
                ('heat', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ManyToManyField(related_name='questions', to='QA.Topic'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QA.Question'),
        ),
    ]
