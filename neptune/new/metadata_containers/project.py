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
import threading
from typing import Union, Optional, Iterable

from neptune.new.metadata_containers import MetadataContainer
from neptune.new.internal.backends.neptune_backend import NeptuneBackend
from neptune.new.internal.background_job import BackgroundJob
from neptune.new.internal.container_type import ContainerType
from neptune.new.internal.operation_processors.operation_processor import (
    OperationProcessor,
)
from neptune.new.internal.utils import verify_type, verify_collection_type
from neptune.new.metadata_containers.runs_table import RunsTable


class Project(MetadataContainer):
    """A class for managing a Neptune project and retrieving information from it.

    You may also want to check `Project docs page`_.

    .. _Project docs page:
       https://docs.neptune.ai/api-reference/project
    """

    container_type = ContainerType.PROJECT

    def __init__(
        self,
        _id: str,
        backend: NeptuneBackend,
        op_processor: OperationProcessor,
        background_job: BackgroundJob,
        lock: threading.RLock,
        workspace: str,
        project_name: str,
    ):
        super().__init__(
            _id,
            backend,
            op_processor,
            background_job,
            lock,
            project_id=_id,
            project_name=project_name,
            workspace=workspace,
        )

    @property
    def _label(self) -> str:
        return f"{self._workspace}/{self._project_name}"

    # pylint:disable=redefined-builtin
    def fetch_runs_table(
        self,
        id: Optional[Union[str, Iterable[str]]] = None,
        state: Optional[Union[str, Iterable[str]]] = None,
        owner: Optional[Union[str, Iterable[str]]] = None,
        tag: Optional[Union[str, Iterable[str]]] = None,
    ) -> RunsTable:
        """Retrieve runs matching the specified criteria.

        All parameters are optional, each of them specifies a single criterion.
        Only runs matching all of the criteria will be returned.

        Args:
            id (str or list of str, optional): A run's id or list of ids.
                E.g. `'SAN-1'` or `['SAN-1', 'SAN-2']`.
                Matching any element of the list is sufficient to pass the criterion.
                Defaults to `None`.
            state (str or list of str, optional): A run's state like or list of states.
                E.g. `'running'` or `['idle', 'running']`.
                Possible values: 'idle', 'running'.
                Defaults to `None`.
                Matching any element of the list is sufficient to pass the criterion.
            owner (str or list of str, optional): Username of the run's owner  or a list of owners.
                E.g. 'josh' or ['frederic', 'josh'].
                The user who created the tracked run is an owner.
                Defaults to `None`.
                Matching any element of the list is sufficient to pass the criterion.
            tag (str or list of str, optional): An experiment tag or list of tags.
                E.g. `'lightGBM'` or ['pytorch', 'cycleLR'].
                Defaults to `None`.
                Only experiments that have all specified tags will match this criterion.

        Returns:
            ``RunsTable``: object containing experiments matching the specified criteria.

            Use `.to_pandas()` to convert it to Pandas `DataFrame`.

        Examples:
            >>> import neptune.new as neptune

            >>> # Fetch project 'jackie/sandbox'
            ... project = neptune.get_project(name='jackie/sandbox')

            >>> # Fetch all Runs metadata as Pandas DataFrame
            ... runs_table_df = project.fetch_runs_table().to_pandas()

            >>> # Sort runs by creation time
            ... runs_table_df = runs_table_df.sort_values(by='sys/creation_time', ascending=False)

            >>> # Extract the last runs id
            ... last_run_id = runs_table_df['sys/id'].values[0]

            You can also filter the runs table by state, owner or tag or a combination:

            >>> # Fetch only inactive runs
            ... runs_table_df = project.fetch_runs_table(state='idle').to_pandas()

            >>> # Fetch only runs created by CI service
            ... runs_table_df = project.fetch_runs_table(owner='my_company_ci_service').to_pandas()

            >>> # Fetch only runs that have both 'Exploration' and 'Optuna' tag
            ... runs_table_df = project.fetch_runs_table(tag=['Exploration', 'Optuna']).to_pandas()

            >>> # You can combine conditions. Runs satisfying all conditions will be fetched
            ... runs_table_df = project.fetch_runs_table(state='idle', tag='Exploration').to_pandas()

        You may also want to check `fetch_runs_table docs page`_.

        .. _fetch_runs_table docs page:
            https://docs.neptune.ai/api-reference/project#fetch_runs_table
        """
        id = self._as_list("id", id)
        state = self._as_list("state", state)
        owner = self._as_list("owner", owner)
        tags = self._as_list("tag", tag)

        leaderboard_entries = self._backend.get_leaderboard(
            project_id=self._id, _id=id, state=state, owner=owner, tags=tags
        )

        return RunsTable(backend=self._backend, entries=leaderboard_entries)

    @staticmethod
    def _as_list(
        name: str, value: Optional[Union[str, Iterable[str]]]
    ) -> Optional[Iterable[str]]:
        verify_type(name, value, (type(None), str, Iterable))
        if value is None:
            return None
        if isinstance(value, str):
            return [value]
        verify_collection_type(name, value, str)
        return value
