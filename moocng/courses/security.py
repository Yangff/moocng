# -*- coding: utf-8 -*-

# Copyright 2012 Rooter Analysis S.L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.contrib import messages
from django.http import Http404
from django.utils.translation import ugettext as _

from moocng.courses.models import CourseTeacher


def can_user_view_course(course, user):
    """Returns a pair where the first element is a bool indicating if the user
    can view the course and the second one is a string code explaining the
    reason."""
    if course.is_public:
        return True, 'public'

    if user.is_superuser:
        return True, 'is_superuser'

    if user.is_staff:
        return True, 'is_staff'

    # check if the user is a teacher of the course
    if not user.is_anonymous():
        try:
            CourseTeacher.objects.get(teacher=user, course=course)
            return True, 'is_teacher'
        except CourseTeacher.DoesNotExist:
            pass

    # at this point you don't have permissions to see a course
    return False, 'not_public'


def check_user_can_view_course(course, request):
    """Raises a 404 error if the user can't see the course"""
    yes_he_can, reason = can_user_view_course(course, request.user)

    if yes_he_can and reason != 'public':
        msg_table = {
            'is_staff': _(u'This course is not public yet. Your have access to it because you are staff member'),
            'is_superuser': _(u'This course is not public yet. Your have access to it because you are a super user'),
            'is_teacher': _(u'This course is not public yet. Your have access to it because you are a teacher of the course'),
            }
        messages.warning(request, msg_table[reason])

    else:
        raise Http404()