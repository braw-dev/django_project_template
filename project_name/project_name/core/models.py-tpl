import os
import re
import unicodedata
from datetime import date
from typing import Any

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from typeid import TypeID

_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")
_windows_device_files = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(10)),
    *(f"LPT{i}" for i in range(10)),
}


def secure_filename(filename: str) -> str:
    r"""Pass it a filename and it will return a secure version of it.  This
    filename can then safely be stored on a regular file system and passed
    to :func:`os.path.join`.  The filename returned is an ASCII only string
    for maximum portability.

    On windows systems the function also makes sure that the file is not
    named after one of the special device files.

    >>> secure_filename("My cool movie.mov")
    'My_cool_movie.mov'
    >>> secure_filename("../../../etc/passwd")
    'etc_passwd'
    >>> secure_filename("i contain cool \xfcml\xe4uts.txt")
    'i_contain_cool_umlauts.txt'

    The function might return an empty filename.  It's your responsibility
    to ensure that the filename is unique and that you abort or
    generate a random filename if the function returned an empty one.

    .. versionadded:: 0.5

    :param filename: the filename to secure

    https://github.com/pallets/werkzeug/blob/3ab332063ece8710b94809d925047f58f2471bb1/src/werkzeug/utils.py#L195-L239
    """
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")

    for sep in os.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    filename = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip("._")

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if os.name == "nt" and filename and filename.split(".")[0].upper() in _windows_device_files:
        filename = f"_{filename}"

    return filename


class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


def get_payslip_upload_path(instance: "EmployerReviewMVP", filename: str) -> str:
    """Construct a filepath for the payslip file upload.

    This embeds an instance ID and a TypeID in the filename to ensure uniqueness.

    Args:
        instance (EmployerReviewMVP): The instance of the model
        filename (str): The original filename

    Returns:
        str: A (Linux) filepath for the file upload
    """
    type_id = TypeID(prefix="payslip")
    sanitized_filename = secure_filename(filename)[-25:]
    return f"employer_reviews/payslips/{instance.id}/{type_id}-{sanitized_filename}"


def validate_not_in_future(value: Any) -> Any:
    if not isinstance(value, date):
        raise ValidationError("The value must be a date.")
    if value > date.today():
        raise ValidationError("The date cannot be in the future.")
    return value


class EmployerReviewMVP(models.Model):
    # Company info
    company_name = models.CharField(max_length=255)
    company_domain = models.CharField(
        max_length=255, validators=[validators.DomainNameValidator()], blank=True
    )
    # Employee info
    job_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    estimated_review_date = models.DateField(
        validators=[validate_not_in_future]
    )  # Approximately when is your review valid?
    tenure_months = models.PositiveSmallIntegerField()  # how long have they worked there
    current_employee = models.BooleanField(default=False)
    # Any employee proof
    payslip = models.FileField(upload_to=get_payslip_upload_path, blank=True)
    # The review
    review_title = models.CharField(max_length=255, validators=[validators.MinLengthValidator(10)])
    review = models.TextField(validators=[validators.MinLengthValidator(160)])
    # Some ratings. 1-5 where 1 is the worst and 5 is the best
    culture_rating = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(5),
        ]
    )  # How good is the company culture? 1-5
    work_life_balance_rating = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(5),
        ]
    )  # What's the work-life balance like? 1-5
    leadership_rating = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(5),
        ]
    )  # How well do you think the company is led? 1-5
    opportunities_rating = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(5),
        ]
    )  # Are there good opportunities for growth? 1-5
    compensation_rating = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(5),
        ]
    )  # How well are you compensated? 1-5
    # Pros and cons - each a list of strings
    pros = models.JSONField(default=list, blank=True)
    cons = models.JSONField(default=list, blank=True)
    # Compensation info
    currency = models.CharField(max_length=3, default="USD")
    base_annual_salary = models.PositiveIntegerField(blank=True, null=True)
    additional_annual_compensation = models.PositiveIntegerField(
        blank=True,
        null=True,
    )  # e.g. bonuses, stock options
    # Metadata
    verified = models.BooleanField(default=False)  # Have we verified this review?
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
