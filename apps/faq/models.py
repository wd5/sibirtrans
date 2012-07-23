# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.utils.translation import ugettext_lazy as _
from apps.utils.managers import PublishedManager

#class QuestionCategory(models.Model):
#    title = models.CharField(verbose_name=u'Название категории', max_length=100)
#    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10, help_text=u'Чем больше число, тем выше располагается элемент')
#    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=False)
#
#    # Managers
#    objects = PublishedManager()
#
#    def get_url(self):
#        return u'/faq/%s/' % self.id
#
#    def get_questions(self):
#        return self.question_set.published()
#
#    class Meta:
#        verbose_name= _(u'question_category')
#        verbose_name_plural = _(u'question_categories')
#        ordering = ['-order']
#
#    def __unicode__(self):
#        return self.title

class Question(models.Model):
    #category = models.ForeignKey(QuestionCategory, verbose_name=u'Категория', default=1)
    pub_date = models.DateTimeField(verbose_name = u'Дата', default=datetime.datetime.now)
    email = models.CharField(verbose_name=u'E-mail',max_length=75)
    question = models.TextField(verbose_name = u'Вопрос')
    answer = models.TextField(verbose_name = u'Ответ', blank = True)
    author = models.CharField(max_length = 150, verbose_name = u'Автор ответа', help_text=u'Например: менеджер',blank=True)
    ans_date = models.DateTimeField(verbose_name = u'Дата ответа', default=datetime.datetime.now, null=True, blank=True)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=False)

    # Managers
    objects = PublishedManager()

    class Meta:
        verbose_name = _(u'question')
        verbose_name_plural = _(u'questions')
        ordering = ['-pub_date']

    def __unicode__(self):
        return u'Вопрос от %s' % self.pub_date

