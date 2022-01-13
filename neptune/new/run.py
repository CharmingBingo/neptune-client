#
# Copyright (c) 2020, Neptune Labs Sp. z o.o.
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
#

# backwards compatibility
# pylint: disable=unused-import

from neptune.new.metadata_containers import Run
from neptune.new.handler import Handler
from neptune.new.internal.backends.neptune_backend import NeptuneBackend
from neptune.new.internal.background_job import BackgroundJob
from neptune.new.internal.container_type import ContainerType
from neptune.new.internal.operation_processors.operation_processor import (
    OperationProcessor,
)
from neptune.new.internal.state import ContainerState
from neptune.new.attributes.attribute import Attribute
from neptune.new.attributes.namespace import (
    NamespaceBuilder,
    Namespace as NamespaceAttr,
)
from neptune.new.exceptions import (
    MetadataInconsistency,
    InactiveRunException,
    NeptunePossibleLegacyUsageException,
)
from neptune.new.internal.backends.api_model import AttributeType
from neptune.new.internal.operation import DeleteAttribute
from neptune.new.internal.run_structure import ContainerStructure as RunStructure
from neptune.new.internal.utils import (
    is_bool,
    is_float,
    is_float_like,
    is_int,
    is_string,
    is_string_like,
    verify_type,
    is_dict_like,
)
from neptune.new.internal.utils.paths import parse_path
from neptune.new.internal.value_to_attribute_visitor import ValueToAttributeVisitor
from neptune.new.types import Boolean, Integer
from neptune.new.types.atoms.datetime import Datetime
from neptune.new.types.atoms.float import Float
from neptune.new.types.atoms.string import String
from neptune.new.types.namespace import Namespace
from neptune.new.types.value import Value

RunState = ContainerState
