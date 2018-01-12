import json
from flask import (request, Response, abort, render_template,
                   flash, redirect, url_for, session)
import pyhtml2md
from github import Github
from hyde.app import app
import git
from git import Repo


def write_header(header):
    s = ''
    head_list = []
    head_list.append('---\n')
    for k, v in header.items():
        head_list.append(k+' : ' + v+'\n')
    head_list.append('---\n')
    result = s.join(str(x) for x in head_list)
    return result


def get_html2md(html):
    html2md = pyhtml2md.html2md()
    md_data = html2md.get_md(html)
    return md_data


def get_repo(repo_path):
    repo = git.Repo(repo_path)
    return repo


def git_clone(url, repo_path, branch='master'):
    repo = Repo.clone_from(url, repo_path, branch=branch)
    return repo


def git_checkout_b(repo, branch_name):
    git = repo.git
    git.checkout('HEAD', b=branch_name)


def git_checkout(repo, branch_name):
    branch = repo.create_head(branch_name)
    repo.head.reference = branch


def git_delete_branch(repo, branch_name):
    branch = repo.create_head(branch_name)
    repo.delete_head(branch)


def git_add(repo, file_list):
    repo.index.add(file_list)


def git_commit(repo, comment):
    repo.index.commit(comment)


def git_pull(repo, remote_name, branch_name):
    repo.git.pull(remote_name, branch_name)


def git_push(repo, remote_name, branch_name):
    repo.git.push(remote_name, branch_name)


def get_untracked_files(repo):
    return repo.untracked_files


@app.route('/api/branch', methods=['POST'])
def get_branch_list():
    if not request.is_json:
        return json.dumps({'success': False}), 400,\
                          {'ContentType': 'application/json'}
    data = request.get_json(force=True)
    g = Github(data['user'], data['password'])
    cur_repo = None
    for repo in g.get_user().get_repos():
        if repo.name == data['repository']:
            cur_repo = repo
    branch_list = []
    for branch in cur_repo.get_branches():
        branch_list.append({'name': branch.name})
    return json.dumps({'success': True, 'repo_list': branch_list})


@app.route('/api/repository', methods=['POST'])
def get_repository_list():
    if not request.is_json:
        return json.dumps({'success': False}), 400,\
                          {'ContentType': 'application/json'}
    data = request.get_json(force=True)
    g = Github(data['user'], data['password'])
    repo_list = []
    for repo in g.get_user().get_repos():
        repo_list.append({'name': repo.name})
    return json.dumps({'success': True, 'repo_list': repo_list})


@app.route('/api/clone', methods=['POST'])
def clone_repository():
    if not request.is_json:
        return json.dumps({'success': False}), 400,\
                          {'ContentType': 'application/json'}
    data = request.get_json(force=True)
    git_clone(data['repo_url'], data['repo_path'])
    return json.dumps({'success': True, 'repo_path': data['repo_path']}), 200,\
        {'ContentType': 'application/json'}


@app.route('/api/delete', methods=['POST'])
def delete_branch():
    if not request.is_json:
        return json.dumps({'success': False}), 400,\
                          {'ContentType': 'application/json'}
    data = request.get_json(force=True)
    repo = get_repo(data['repo_path'])
    git_delete_branch(repo, data['branch_name'])
    return json.dumps({'success': True, 'branch_name': data['branch_name']}),\
        200, {'ContentType': 'application/json'}


@app.route('/api/checkout', methods=['POST'])
def checkout_branch():
    if not request.is_json:
        return json.dumps({'success': False}), 400, \
                          {'ContentType': 'application/json'}
    data = request.get_json(force=True)
    repo = get_repo(data['repo_path'])
    git_checkout(repo, data['branch_name'])
    return json.dumps({'success': True}), 200,\
        {'ContentType': 'application/json'}


@app.route('/api/checkout_new', methods=['POST'])
def create_branch():
    if not request.is_json:
        return json.dumps({'success': False}), 400,\
                          {'ContentType': 'application/json'}
    data = request.get_json(force=True)
    repo = get_repo(data['repo_path'])
    git_checkout_b(repo, data['branch_name'])
    return json.dumps({'success': True}), 200,\
        {'ContentType': 'application/json'}


@app.route('/api/write_md', methods=['POST'])
def write_html2md():
    if not request.is_json:
        return json.dumps({'success': False}), 400,\
                          {'ContentType': 'application/json'}
    data = request.get_json(force=True)
    repo = get_repo(data['repo_path'])
    md = get_html2md(data['body'])
    # TODO try except test code
    # try
    with open(data['file_path'], 'w') as f:
        f.write(write_header(data['header']))
        f.write(md)
    # except IOError:
    #    print("Fail to write file")
    #    return "IOERROR"
    untracked_files = get_untracked_files(repo)
    git_add(repo, untracked_files)
    return json.dumps({'success': True}), 200,\
        {'ContentType': 'application/json'}


@app.route('/api/commit', methods=['POST'])
def commit():
    if not request.is_json:
        return json.dumps({'success': False}), 400,\
                          {'ContentType': 'application/json'}
    data = request.get_json(force=True)
    repo = get_repo(data['repo_path'])
    git_commit(repo, data['comment'])
    return json.dumps({'success': True}), 200,\
        {'ContentType': 'application/json'}


@app.route('/api/pull', methods=['POST'])
def pull():
    if not request.is_json:
        return json.dumps({'success': False}), 400, \
                          {'ContentType': 'application/json'}
    data = request.get_json(force=True)
    repo = get_repo(data['repo_path'])
    git_pull(repo, data['remote_name'], data['branch_name'])
    return json.dumps({'success': True}), 200,\
        {'ContentType': 'application/json'}


@app.route('/api/push', methods=['POST'])
def push():
    if not request.is_json:
        return json.dumps({'success': False}), 400,\
                          {'ContentType': 'application/json'}
    data = request.get_json(force=True)
    repo = get_repo(data['repo_path'])
    git_push(repo, data['remote_name'], data['branch_name'])
    return json.dumps({'success': True}), 200, \
        {'ContentType': 'application/json'}
