# Generated by Django 4.0.4 on 2022-05-15 19:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0003_remove_budget_viewer_budget_viewers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='category',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='expenses',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='incomes',
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('amount', models.IntegerField()),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='budgets.budget')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='budgets.category')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
    ]
