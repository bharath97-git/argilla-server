#  coding=utf-8
#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
This module configures the api routes under /api prefix, and
set the required security dependencies if api security is enabled
"""

from fastapi import APIRouter, HTTPException, Request

from argilla_server.apis.v0.handlers import (
    authentication,
    datasets,
    info,
    metrics,
    records,
    records_search,
    records_update,
    text2text,
    text_classification,
    token_classification,
    users,
    workspaces,
)
from argilla_server.apis.v1.handlers import datasets as datasets_v1
from argilla_server.apis.v1.handlers import fields as fields_v1
from argilla_server.apis.v1.handlers import metadata_properties as metadata_properties_v1
from argilla_server.apis.v1.handlers import oauth2 as oauth2_v1
from argilla_server.apis.v1.handlers import questions as questions_v1
from argilla_server.apis.v1.handlers import records as records_v1
from argilla_server.apis.v1.handlers import responses as responses_v1
from argilla_server.apis.v1.handlers import suggestions as suggestions_v1
from argilla_server.apis.v1.handlers import users as users_v1
from argilla_server.apis.v1.handlers import vectors_settings as vectors_settings_v1
from argilla_server.apis.v1.handlers import workspaces as workspaces_v1
from argilla_server.errors.base_errors import __ALL__

api_router = APIRouter(responses={error.HTTP_STATUS: error.api_documentation() for error in __ALL__})


dependencies = []

for router in [
    authentication.router,
    users.router,
    workspaces.router,
    datasets.router,
    info.router,
    metrics.router,
    records.router,
    records_search.router,
    records_update.router,
    text_classification.router,
    token_classification.router,
    text2text.router,
]:
    api_router.include_router(router, dependencies=dependencies)

# API v1
api_router.include_router(datasets_v1.router, prefix="/v1")
api_router.include_router(fields_v1.router, prefix="/v1")
api_router.include_router(questions_v1.router, prefix="/v1")
api_router.include_router(metadata_properties_v1.router, prefix="/v1")
api_router.include_router(records_v1.router, prefix="/v1")
api_router.include_router(responses_v1.router, prefix="/v1")
api_router.include_router(suggestions_v1.router, prefix="/v1")
api_router.include_router(users_v1.router, prefix="/v1")
api_router.include_router(vectors_settings_v1.router, prefix="/v1")
api_router.include_router(workspaces_v1.router, prefix="/v1")
api_router.include_router(oauth2_v1.router, prefix="/v1")


@api_router.route("/{_:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], include_in_schema=False)
def endpoint_not_found_controller(request: Request):
    raise HTTPException(status_code=404, detail=f"Endpoint {request.url.path!r} not found")
