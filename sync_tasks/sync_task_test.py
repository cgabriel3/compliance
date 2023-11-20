import pytest

from phabricator import Phabricator
import sync_tasks
import configparser
import json

config = configparser.ConfigParser()
config.read(sync_tasks.get_env('test'))
phabricator = Phabricator(config)

username_to_phabricator_api_token_map = json.loads(config['phabricator']['api_token_map'])
default_api_token = config['phabricator']['api_token']

test_task_fields = {
  "id": "1159680598001066107",
  "workspaceId": 67664246,
  "name": "Testing sub_task creation",
  "description": "This is testing title",
  "url": "https://www.tapd.cn/67664246/prong/stories/view/1159680598001066107",
  "status": "Open",
  "priority": "EMPTY",
  "category": "Release Hub",
  "creator": "advis.tasyah.mulia",
  "created": 1698031325000,
  "owner": "christian.gabriel.isjwara;",
  "developer": "christian.gabriel.isjwara;",
  "qa": "james.surya.seputro;",
  "modified": 1698031367000,
  "begin": 1697990400000,
  "due": 1697990400000
}

update_task_fields = {
  "id": "9999999",
  "workspaceId": 67664246,
  "name": "This is updated from Unit Testing",
  "description": "Updated Testing Description",
  "url": "https://www.tapd.cn/67664246/prong/stories/view/9999999",
  "status": "Assess Finished",
  "priority": "Nice To Have",
  "category": "Release Hub",
  "creator": "andrey.martin",
  "created": 1698031325000,
  "owner": "christian.gabriel.isjwara;",
  "developer": "andrey.martin;himawan.saputra.utama;",
  "qa": "james.surya.seputro;yulia.dewi;",
  "modified": 1698031367000,
  "begin": 1697990400000,
  "due": 1697990400000
}

create_sub_task_fields = {
  "custom_field_six": "",
  "custom_field_50": "",
  "has_attachment": "0",
  "workspace_id": "59680598",
  "custom_field_14": "",
  "custom_field_15": "",
  "custom_field_12": "",
  "custom_field_13": "",
  "custom_field_one": "",
  "custom_field_10": "",
  "custom_field_11": "",
  "exceed": "0",
  "custom_field_seven": "",
  "modified": "2023-11-17 17:24:05",
  "id": "1159680598001066124",
  "custom_field_18": "",
  "custom_field_19": "",
  "custom_field_16": "",
  "custom_field_17": "",
  "created": "2023-11-17 17:24:00",
  "remain": "0",
  "completed": None,
  "priority": "3",
  "custom_field_9": "",
  "iteration_id": "0",
  "custom_field_25": "",
  "custom_field_26": "",
  "custom_field_23": "",
  "custom_field_24": "",
  "custom_field_21": "",
  "custom_field_22": "",
  "custom_field_20": "",
  "name": "[web] refactor resource",
  "custom_field_29": "",
  "begin": "2023-11-06",
  "effort_completed": "0",
  "custom_field_27": "",
  "status": "progressing",
  "custom_field_28": "",
  "release_id": "0",
  "custom_field_four": "",
  "story_id": "1159680598001066107",
  "description": "",
  "effort": None,
  "custom_field_36": "",
  "custom_field_37": "",
  "custom_field_34": "",
  "custom_field_35": "",
  "custom_field_32": "",
  "custom_field_eight": "",
  "custom_field_33": "",
  "custom_field_30": "",
  "custom_field_31": "",
  "priority_label": "3",
  "custom_field_38": "",
  "custom_field_39": "",
  "owner": "christian.gabriel.isjwara;",
  "cc": "",
  "creator": "christian.gabriel.isjwara",
  "custom_field_40": "",
  "label": "",
  "custom_field_47": "",
  "custom_field_48": "",
  "custom_field_45": "",
  "custom_field_46": "",
  "custom_field_43": "",
  "custom_plan_field_3": "0",
  "due": "2023-11-30",
  "custom_field_44": "",
  "custom_plan_field_4": "0",
  "custom_field_41": "",
  "custom_plan_field_1": "0",
  "custom_field_three": "",
  "custom_field_42": "",
  "custom_plan_field_2": "0",
  "progress": "0",
  "custom_plan_field_5": "0",
  "custom_field_five": "",
  "custom_field_two": "",
  "custom_field_49": ""
}


@pytest.mark.run(order=1)
def test_create_task():
  sync_fields = sync_tasks.format_create_task_fields(phabricator, test_task_fields)
  sync_fields["creator_api_token"] = sync_tasks.get_creator_api_token(username_to_phabricator_api_token_map, test_task_fields["creator"], default_api_token)
  phabricator.create_update_task(sync_fields)


@pytest.mark.run(order=2)
def test_update_task():
  phabricator_task_list = phabricator.get_tasks([], None)
  story_id_to_phabricator_task_map, task_id_to_phabricator_task_map = sync_tasks.create_tapd_story_and_tapd_task_to_phabricator_task_mapping(phabricator_task_list)
  sync_fields = sync_tasks.format_create_task_fields(phabricator, update_task_fields)
  sync_fields["creator_api_token"] = sync_tasks.get_creator_api_token(username_to_phabricator_api_token_map, update_task_fields["creator"],
                                                                      default_api_token)
  phabricator.create_update_task(sync_tasks.format_update_task_fields(sync_fields, story_id_to_phabricator_task_map[test_task_fields['id']]))


@pytest.mark.run(order=3)
def test_create_comment():
  phabricator_task_list = phabricator.get_tasks([], None)
  story_id_to_phabricator_task_map, task_id_to_phabricator_task_map = sync_tasks.create_tapd_story_and_tapd_task_to_phabricator_task_mapping(phabricator_task_list)
  create_comment_fields = {
    'task_id': story_id_to_phabricator_task_map[test_task_fields['id']]['id'],
    'comment': "This is a comment made from Unit Testing",
    'commentator_api_token': default_api_token
  }
  phabricator.create_comment(create_comment_fields)


@pytest.mark.run(order=4)
def test_create_sub_task():
  phabricator_task_list = phabricator.get_tasks([], None)
  story_id_to_phabricator_task_map, task_id_to_phabricator_task_map = sync_tasks.create_tapd_story_and_tapd_task_to_phabricator_task_mapping(phabricator_task_list)
  phabricator_parent_task = story_id_to_phabricator_task_map.get(create_sub_task_fields["story_id"])
  create_sub_task_fields["phid"] = phabricator_parent_task["phid"]
  sync_fields = sync_tasks.format_create_sub_task_fields(phabricator, create_sub_task_fields)
  sync_fields["creator_api_token"] = sync_tasks.get_creator_api_token(username_to_phabricator_api_token_map, test_task_fields["creator"],
                                                                      default_api_token)
  phabricator.create_update_subtask(sync_fields)
