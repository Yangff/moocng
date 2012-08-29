# Copyright 2012 Rooter Analysis S.L. All rights reserved.
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

from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import (get_object_or_404, get_list_or_404,
                              render_to_response)
from django.template import RequestContext
from django.utils.translation import ugettext as _

from moocng.courses.models import Course, Unit


def home(request):
    return render_to_response('courses/home.html', {
            'courses': Course.objects.all(),
            }, context_instance=RequestContext(request))


def course_overview(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)

    if request.user.is_authenticated():
        is_enrolled = course.students.filter(id=request.user.id).exists()
    else:
        is_enrolled = False

    if request.method == 'POST':
        course.students.add(request.user)
        course.save()
        success(request,
                _(u'Congratulations, you have successfully enroll in the course %(course)s')
                % {'course': unicode(course)})
        return HttpResponseRedirect(reverse('course_overview',
                                            args=(course.slug, )))

    return render_to_response('courses/overview.html', {
            'course': course,
            'is_enrolled': is_enrolled
            }, context_instance=RequestContext(request))


@login_required
def course_classroom(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    unit_list = get_list_or_404(Unit, course=course)

    is_enrolled = course.students.filter(id=request.user.id).exists()
    if not is_enrolled:
        return HttpResponseForbidden(_('Your are not enrolled in this course'))

    return render_to_response('courses/classroom.html', {
        'course': course,
        'unit_list': unit_list,
        'is_enrolled': is_enrolled,
    }, context_instance=RequestContext(request))


@login_required
def course_progress(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    unit_list = get_list_or_404(Unit, course=course)

    is_enrolled = course.students.filter(id=request.user.id).exists()
    if not is_enrolled:
        return HttpResponseForbidden(_('Your are not enrolled in this course'))

    return render_to_response('courses/progress.html', {
        'course': course,
        'unit_list': unit_list,
        'is_enrolled': is_enrolled,
    }, context_instance=RequestContext(request))
