# Copyright (c) 2015. Mount Sinai School of Medicine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import collections
import json

from .resource_collection import ResourceCollection
from .resource import Resource
from .util import exec_in_directory
from . import export

def load(filename):
    if filename.endswith(".py"):
        format = "python"
    elif filename.endswith(".json"):
        format = "json"
    else:
        raise ValueError("Unsupported file format: %s" % filename)
    
    with open(filename) as fd:
        return loads(fd.read(), format=format)

def loads(data, filename=None, format="json"):
    if format == "python":
        try:
            old_resources = export._EXPORTED_RESOURCES
            export._EXPORTED_RESOURCES = []
            exec_in_directory(filename=filename, code=data)
        finally:
            resources = export._EXPORTED_RESOURCES
            export._EXPORTED_RESOURCES = old_resources
        return ResourceCollection(resources, filename)
    elif format == "json":
        parsed = json.loads(data, object_pairs_hook=collections.OrderedDict)
        with_comments_removed = remove_keys_starting_with_hash(parsed)
        resources = [
            Resource(name=key, **value)
            for (key, value) in with_comments_removed.items()
        ]
        return ResourceCollection(resources, filename)
    else:
        raise ValueError("Unsupported file format: %s" % filename)

def remove_keys_starting_with_hash(obj):
    if isinstance(obj, dict):
        return {
            key: remove_keys_starting_with_hash(value)
            for (key, value) in obj.items()
            if not key.startswith("#")
        }
    return obj