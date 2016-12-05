
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io

from __future__ import absolute_import, print_function, unicode_literals, division
from jormungandr.interfaces.v1.serializer.pt import StopAreaSerializer, LineSerializer, DisruptionSerializer
from jormungandr.interfaces.v1.serializer.fields import ErrorSerializer, FeedPublisherSerializer, PaginationSerializer
import serpy

class LinesSerializer(serpy.Serializer):
    pagination = PaginationSerializer(attr='pagination', display_none=True, required=True)
    lines = LineSerializer(many=True)
    error = ErrorSerializer(display_none=False)
    disruptions = DisruptionSerializer(attr='impacts', many=True)
    feed_publishers = FeedPublisherSerializer(many=True, display_none=False)

class DisruptionsSerializer(serpy.Serializer):
    pagination = PaginationSerializer(attr='pagination', display_none=True, required=True)
    error = ErrorSerializer(display_none=False)
    disruptions = DisruptionSerializer(attr='impacts', many=True)
    feed_publishers = FeedPublisherSerializer(many=True, display_none=False)
