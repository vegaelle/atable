# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20150511_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(verbose_name='unité', max_length=100, choices=[('g', 'g'), ('kg', 'kg'), ('cl', 'cl'), ('l', 'l'), ('unit', 'unité')]),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='licence',
            field=models.TextField(blank=True, verbose_name='licence', default='<h2> CC0 1.0 universel (CC0 1.0)</h2>\n<em>Transfert dans le Domaine Public</em>\n\n<h3>Cette licence est acceptable pour des œuvres culturelles libres.</h3>\n\n<p>La personne qui a associé une œuvre à cet acte a dédié l’œuvre au domaine\npublic en renonçant dans le monde entier à ses droits sur l’œuvre selon les\nlois sur le droit d’auteur, droit voisin et connexes, dans la mesure permise\npar la loi.</p>\n\n<p>Vous pouvez copier, modifier, distribuer et représenter l’œuvre, même à des\nfins commerciales, sans avoir besoin de demander l’autorisation. Voir d’autres\ninformations ci-dessous.</p>\n\n<h3>Autres informations</h3>\n\n<ul>\n<li>Les brevets et droits de marque commerciale qui peuvent être détenus par\nautrui ne sont en aucune façon affectés par CC0, de même pour les droits que\npourraient détenir d’autres personnes sur l’œuvre ou sur la façon dont elle est\nutilisée, comme le droit à l’image ou à la vie privée.</li>\n<li>À moins d’une mention expresse contraire, la personne qui a identifié une\nœuvre à cette notice ne concède aucune garantie sur l’œuvre et décline toute\nresponsabilité de toute utilisation de l’œuvre, dans la mesure permise par la\nloi.</li>\n<li>Quand vous utilisez ou citez l’œuvre, vous ne devez pas sous-entendre le\nsoutien de l’auteur ou de la personne qui affirme.</li>\n</ul>'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='parent_recipes',
            field=models.ManyToManyField(blank=True, verbose_name='recettes de base', related_name='parent_recipes_rel_+', to='recipes.Recipe'),
        ),
    ]
