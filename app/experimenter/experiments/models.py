from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.utils.functional import cached_property

from experimenter.experiments.constants import ExperimentConstants


class ExperimentManager(models.Manager):

    def most_recently_changed(self):
        return (
            self.all()
            .annotate(latest_change=Max('changes__changed_on'))
            .order_by('-latest_change')
        )


class Experiment(ExperimentConstants, models.Model):
    project = models.ForeignKey(
        'projects.Project',
        blank=False,
        null=False,
        related_name='experiments',
    )
    status = models.CharField(
        max_length=255,
        default=ExperimentConstants.STATUS_CREATED,
        choices=ExperimentConstants.STATUS_CHOICES,
    )
    name = models.CharField(
        max_length=255, unique=True, blank=False, null=False)
    slug = models.SlugField(
        max_length=255, unique=True, blank=False, null=False)
    short_description = models.TextField(default='', blank=True, null=True)
    pref_key = models.CharField(max_length=255, blank=True, null=True)
    pref_type = models.CharField(
        max_length=255,
        choices=ExperimentConstants.PREF_TYPE_CHOICES,
    )
    pref_branch = models.CharField(
        max_length=255,
        choices=ExperimentConstants.PREF_BRANCH_CHOICES,
        default=ExperimentConstants.PREF_BRANCH_DEFAULT,
    )
    population_percent = models.DecimalField(
        max_digits=7, decimal_places=4, default='0')
    firefox_version = models.CharField(max_length=255, choices=ExperimentConstants.VERSION_CHOICES)
    firefox_channel = models.CharField(
        max_length=255, choices=ExperimentConstants.CHANNEL_CHOICES)
    client_matching = models.TextField(default='', blank=True)
    objectives = models.TextField(default='')
    analysis = models.TextField(default='', blank=True, null=True)
    total_users = models.PositiveIntegerField(default=0)
    enrollment_dashboard_url = models.URLField(blank=True, null=True)
    dashboard_url = models.URLField(blank=True, null=True)
    dashboard_image_url = models.URLField(blank=True, null=True)

    objects = ExperimentManager()

    def __str__(self):  # pragma: no cover
        return self.name

    class Meta:
        verbose_name = 'Experiment'
        verbose_name_plural = 'Experiments'

    def clean_status(self):
        if not self.pk:
            return

        old_status = Experiment.objects.get(pk=self.pk).status
        new_status = self.status
        expected_new_status = new_status in self.STATUS_TRANSITIONS[old_status]

        if old_status != new_status and not expected_new_status:
            raise ValidationError({'status': (
                'You can not change an Experiment\'s status '
                'from {old_status} to {new_status}'
            ).format(
                old_status=old_status, new_status=new_status)})

    def clean(self, validate=False):
        if validate:
            self.clean_status()

    def save(self, validate=False, *args, **kwargs):
        self.clean(validate=validate)
        return super().save(*args, **kwargs)

    @cached_property
    def control(self):
        return self.variants.filter(is_control=True).first()

    @cached_property
    def variant(self):
        return self.variants.filter(is_control=False).first()

    @property
    def is_readonly(self):
        return self.status != self.STATUS_CREATED

    def _transition_date(self, start_state, end_state):
        change = self.changes.filter(
            old_status=start_state,
            new_status=end_state,
        )

        if change.count() == 1:
            return change.get().changed_on

    @property
    def population(self):
        return '{percent:g}% of Firefox {version} {channel}'.format(
            percent=float(self.population_percent),
            version=self.firefox_version,
            channel=self.firefox_channel,
        )

    @property
    def variant_ratios(self):
        return ' : '.join([
            '{r} {v}'.format(r=variant.ratio, v=variant.name)
            for variant in self.variants.all()
        ])

    @property
    def start_date(self):
        return self._transition_date(
            self.STATUS_ACCEPTED,
            self.STATUS_LAUNCHED,
        )

    @property
    def end_date(self):
        return self._transition_date(
            self.STATUS_LAUNCHED,
            self.STATUS_COMPLETE,
        )

    @property
    def experiment_slug(self):
        return 'pref-flip-{project_slug}-{experiment_slug}'.format(
            project_slug=self.project.slug,
            experiment_slug=self.slug,
        )

    @property
    def experiment_url(self):
        return urljoin(
            'https://{host}'.format(host=settings.HOSTNAME),
            reverse('admin:experiments_experiment_change', args=[self.pk])
        )

    @property
    def accept_url(self):
        return urljoin(
            'https://{host}'.format(host=settings.HOSTNAME),
            reverse('experiments-accept', kwargs={'slug': self.slug})
        )

    @property
    def reject_url(self):
        return urljoin(
            'https://{host}'.format(host=settings.HOSTNAME),
            reverse('experiments-reject', kwargs={'slug': self.slug})
        )

    @property
    def experiments_viewer_url(self):
        return (
            'https://moz-experiments-viewer.herokuapp.com/?ds={slug}'
            '&metrics=ALL&next=%2F&pop=ALL&scale=linear&showOutliers=false'
        ).format(slug=self.slug)


class ExperimentVariant(models.Model):
    experiment = models.ForeignKey(
        Experiment, blank=False, null=False, related_name='variants')
    name = models.CharField(
        max_length=255, blank=False, null=False)
    slug = models.SlugField(
        max_length=255, blank=False, null=False)
    is_control = models.BooleanField(default=False)
    description = models.TextField(default='')
    ratio = models.PositiveIntegerField(default=1)
    value = JSONField(default=False)

    def __str__(self):  # pragma: no cover
        return self.name

    class Meta:
        verbose_name = 'Experiment Variant'
        verbose_name_plural = 'Experiment Variants'
        unique_together = (
            ('slug', 'experiment'),
            ('is_control', 'experiment'),
        )


class ExperimentChangeLogManager(models.Manager):

    def latest(self):
        return self.all().order_by('-changed_on').first()


class ExperimentChangeLog(models.Model):
    def current_datetime():
        return timezone.now()

    experiment = models.ForeignKey(
        Experiment, blank=False, null=False, related_name='changes')
    changed_on = models.DateTimeField(default=current_datetime)
    changed_by = models.ForeignKey(get_user_model())
    old_status = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=Experiment.STATUS_CHOICES,
    )
    new_status = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        choices=Experiment.STATUS_CHOICES,
    )
    message = models.TextField(blank=True, null=True)

    objects = ExperimentChangeLogManager()

    def __str__(self):  # pragma: no cover
        return '{status} by {updater} on {datetime}'.format(
          status=self.new_status,
          updater=self.changed_by,
          datetime=self.changed_on.date(),
        )

    class Meta:
        verbose_name = 'Experiment Change Log'
        verbose_name_plural = 'Experiment Change Logs'
        ordering = ('changed_on',)
