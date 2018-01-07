# Generated by Django 2.0 on 2018-01-07 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('email', models.EmailField(max_length=64, null=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('time', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'activity',
                'ordering': ('-time',),
            },
        ),
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
            options={
                'db_table': 'answer',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(max_length=500)),
                ('add_time', models.DateField(auto_now_add=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.Answer')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comment',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_read', models.BooleanField(default=False)),
                ('time', models.DateField(auto_now_add=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='api.Answer')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'message',
                'ordering': ('-time',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='', upload_to='avatar')),
                ('nickname', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=500)),
                ('agreed', models.ManyToManyField(related_name='agreedUser', to='api.Answer')),
                ('disagreed', models.ManyToManyField(related_name='disagreedUser', to='api.Answer')),
                ('favorites', models.ManyToManyField(to='api.Answer')),
            ],
            options={
                'db_table': 'profile',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='标题')),
                ('detail', models.TextField(verbose_name='描述')),
                ('visit_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='published', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=20, unique=True)),
                ('introduction', models.TextField()),
                ('heat', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'topic',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='topics',
            field=models.ManyToManyField(related_name='questions', to='api.Topic'),
        ),
        migrations.AddField(
            model_name='profile',
            name='history',
            field=models.ManyToManyField(related_name='history', to='api.Question'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='watchedQuestion',
            field=models.ManyToManyField(related_name='watchedUser', to='api.Question'),
        ),
        migrations.AddField(
            model_name='profile',
            name='watchedUser',
            field=models.ManyToManyField(related_name='watchedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='api.Question'),
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='api.Question'),
        ),
        migrations.AddField(
            model_name='activity',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Answer'),
        ),
        migrations.AddField(
            model_name='activity',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Question'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='api.Profile'),
        ),
        migrations.AddField(
            model_name='activity',
            name='watch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Profile'),
        ),
    ]
