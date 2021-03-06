from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_metadata.constants import REQUIRED


def get_required_crf(subject_visit=None, subject_identifier=None,
                     visit_code=None, **kwargs):
    """ Returns model class for a CRF required for the referral
    but not yet keyed.
    """
    crf_metadata_model_cls = django_apps.get_model('edc_metadata.crfmetadata')
    if subject_visit:
        subject_identifier = subject_visit.subject_identifier
        visit_code = subject_visit.visit_code

    crfs = [
        'bcpp_subject.subjectlocator',
        'bcpp_subject.residencymobility',
        'bcpp_subject.hivresult',
        'bcpp_subject.elisahivresult',
        'bcpp_subject.hivresultdocumentation',
        'bcpp_subject.hivtestreview',
        'bcpp_subject.pimacd4',
        'bcpp_subject.hivtestinghistory']

    for crf in crfs:
        try:
            crf_metadata_model_cls.objects.get(
                model=crf,
                subject_identifier=subject_identifier,
                entry_status=REQUIRED,
                visit_code=visit_code)
            return django_apps.get_app_config(
                crf.split('.')[0]).get_model(crf.split('.')[1])
        except ObjectDoesNotExist:
            pass
    return None
