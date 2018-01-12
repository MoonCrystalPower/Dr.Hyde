import os
from shutil import rmtree
from hyde.app import app
from flask import request
import json
import requests

from flask import url_for
from tests.commands.test_base import BaseTestCase
from flask.ext.testing import TestCase
from flask.ext.login import current_user

test_dir = 'test_dir'


class TestViews(BaseTestCase):

    def setUp(self):
        os.mkdir(test_dir)
        self.app = app
        self.client = app.test_client()
        self.repo_url = 'https://github.com/sh92/sh92.github.io'
        repo_path = test_dir+'/'+self.repo_url.split('/')[-1]
        self.header = {'title': 'blabla', 'category': 'blog'}
        self.repo_path = os.path.abspath(repo_path)

    def tearDown(self):
        rmtree(test_dir)

    def test_success_branch(self):
        data = {'repo_url': self.repo_url, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('clone_repository'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        branch_name = 'test_branch'
        data = {'branch_name': branch_name, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('create_branch'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        name = 'test'
        file_path = './'+test_dir + '/' + name + '.md'
        body = '<strong>aaaa</strong>'
        data = {'body': body, 'repo_path': self.repo_path,
                'file_path': file_path, 'header': self.header}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('write_html2md'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        comment = 'This comment is Test'
        data = {'comment': comment, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('commit'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        remote_name = 'origin'
        branch_name = 'test_branch'
        data = {'remote_name': remote_name,
                'repo_path': self.repo_path, 'branch_name': branch_name}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('pull'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        response = self.client.post(
            url_for('push'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

    def test_success_delete_branch(self):
        data = {'repo_url': self.repo_url, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('clone_repository'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        branch_name = 'test_branch'
        data = {'branch_name': branch_name, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('create_branch'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        branch_name = 'master'
        data = {'branch_name': branch_name, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('checkout_branch'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        branch_name = 'test_branch'
        data = {'branch_name': branch_name, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('delete_branch'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

    def test_not_json_clone(self):
        data = {'repo_url': self.repo_url, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
                url_for('clone_repository'),
                data=json_data)
        self.assert_400(response)

    def test_not_json_branch(self):
        data = {'repo_url': self.repo_url, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('clone_repository'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        branch_name = 'test_branch'
        data = {'branch_name': branch_name, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
                url_for('checkout_branch'),
                data=json_data)
        self.assert_400(response)

    def test_not_json_new_branch(self):
        data = {'repo_url': self.repo_url, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('clone_repository'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        branch_name = 'test_branch'
        data = {'branch_name': branch_name, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(url_for('create_branch'), data=json_data)
        self.assert_400(response)

    def test_not_json_filewrite(self):
        data = {'repo_url': self.repo_url, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('clone_repository'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        branch_name = 'test_branch'
        data = {'branch_name': branch_name, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('create_branch'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        name = 'test'
        file_path = './'+test_dir + '/' + name + '.md'
        body = '<strong>aaaa</strong>'
        data = {'body': body, 'repo_path': self.repo_path,
                'file_path': file_path, 'header': self.header}
        json_data = json.dumps(data)
        response = self.client.post(url_for('write_html2md'), data=json_data)
        self.assert_400(response)

    def test_not_json_commit(self):
        data = {'repo_url': self.repo_url, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('clone_repository'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        branch_name = 'test_branch'
        data = {'branch_name': branch_name, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('create_branch'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        name = 'test'
        file_path = './'+test_dir + '/' + name + '.md'
        body = '<strong>aaaa</strong>'
        data = {'body': body, 'repo_path': self.repo_path,
                'file_path': file_path, 'header': self.header}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('write_html2md'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        comment = 'This comment is Test'
        data = {'comment': comment, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(url_for('commit'), data=json_data)
        self.assert_400(response)

    def test_not_json_pull(self):
        data = {'repo_url': self.repo_url, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('clone_repository'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        branch_name = 'test_branch'
        data = {'branch_name': branch_name, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('create_branch'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        name = 'test'
        file_path = './'+test_dir + '/' + name + '.md'
        body = '<strong>aaaa</strong>'
        data = {'body': body, 'repo_path': self.repo_path,
                'file_path': file_path, 'header': self.header}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('write_html2md'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        comment = 'This comment is Test'
        data = {'comment': comment, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('commit'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        remote_name = 'origin'
        branch_name = 'test_branch'
        data = {'remote_name': remote_name,
                'repo_path': self.repo_path, 'branch_name': branch_name}
        json_data = json.dumps(data)
        response = self.client.post(url_for('pull'), data=json_data)
        self.assert_400(response)

    def test_not_json_push(self):
        data = {'repo_url': self.repo_url, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('clone_repository'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        branch_name = 'test_branch'
        data = {'branch_name': branch_name, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('create_branch'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        name = 'test'
        file_path = './'+test_dir + '/' + name + '.md'
        body = '<strong>aaaa</strong>'
        data = {'body': body, 'repo_path': self.repo_path,
                'file_path': file_path, 'header': self.header}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('write_html2md'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        comment = 'This comment is Test'
        data = {'comment': comment, 'repo_path': self.repo_path}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('commit'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        remote_name = 'origin'
        branch_name = 'test_branch'
        data = {'remote_name': remote_name,
                'repo_path': self.repo_path, 'branch_name': branch_name}
        json_data = json.dumps(data)
        response = self.client.post(
            url_for('pull'),
            data=json_data,
            content_type='application/json')
        self.assert_200(response)

        response = self.client.post(url_for('push'), data=json_data)
        self.assert_400(response)
