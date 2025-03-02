#!/usr/bin/env python

# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Game Servers sample for updating the rollout of a game
server deployment to set the override config.

Example usage:
    python update_rollout_override.py --project-id <project-id> --deployment-id <deployment-id> --config-id <config-id> --realm-location <realm-location> --realm-id <realm-id>
"""

import argparse

from google.cloud import gaming
from google.cloud.gaming_v1.types import common
from google.cloud.gaming_v1.types import game_server_deployments
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


# [START cloud_game_servers_deployment_rollout_override]
def update_rollout_override(
    project_id, deployment_id, config_id, realm_location, realm_id
):
    """Update the rollout of a game server deployment to set the override config."""

    client = gaming.GameServerDeploymentsServiceClient()

    # Location is hard coded as global, as game server deployments can
    # only be created in global.  This is done for all operations on
    # game Server deployments, as well as for its child resource types.
    request = game_server_deployments.UpdateGameServerDeploymentRolloutRequest()
    request.rollout.name = (
        f"projects/{project_id}/locations/global/gameServerDeployments/{deployment_id}"
    )
    realm_name = f"projects/{project_id}/locations/{realm_location}/realms/{realm_id}"
    config_override = game_server_deployments.GameServerConfigOverride(
        realms_selector=common.RealmSelector(realms=[realm_name]),
        config_version=config_id,
    )
    request.rollout.game_server_config_overrides = [config_override]
    request.update_mask = field_mask.FieldMask(paths=["game_server_config_overrides"])

    operation = client.update_game_server_deployment_rollout(request)
    print(f"Update deployment rollout operation: {operation.operation.name}")
    operation.result(timeout=120)


# [END cloud_game_servers_deployment_rollout_override]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", help="Your cloud project ID.", required=True)
    parser.add_argument(
        "--deployment-id", help="Your game server deployment ID.", required=True
    )
    parser.add_argument(
        "--config-id", help="Your game server config ID.", required=True
    )
    parser.add_argument(
        "--realm-location", help="Your game server config ID.", required=True
    )
    parser.add_argument("--realm-id", help="Your game server config ID.", required=True)

    args = parser.parse_args()

    update_rollout_override(
        args.project_id,
        args.deployment_id,
        args.config_id,
        args.realm_location,
        args.realm_id,
    )
