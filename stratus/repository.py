#!/usr/bin/env python3

import os
import contextlib

from git import Repo
from stratus.shell_commands import command_output


def repo_directory():
    """
    helper method that extracts the current git repo directory
    using a callout to git rev-parse.
    If in a repo, this returns the path to the top level dir,
    if not, it returns None
    """
    return command_output(['git', 'rev-parse', '--show-toplevel'], split=False)



class Committer(object):
    """
    context helper to add and commit a group of files
    to a branch in a git repo
    """
    def __init__(self, repo, branch):
        self._repo = repo
        self._branch = branch
        self._files = set()

    def add_file(self, filename):
        """
        add_file

        Add a file to the index, equivalent of git add <file>

        :param filename: path to file to be added
        :return:
        """
        self._files.add(filename)

    def diffs(self):
        """
        list filenames that have been added but not committed

        :return: list of filenames in repo with changes
        """
        changes = self._repo.index.diff(None)
        diffs = []
        for diff in changes:
            diffs.append(diff.a_blob.path)
        return diffs

    def commit(self, msg):
        """
        commit changes to repo, also preserves executable bits if set

        :param msg: commit message
        :return:
        """
        self._repo.index.add(list(self._files))
        for f in self._files:
            if os.access(f, os.X_OK):
                repo.git.update_index(f, chmod='+x')
        # commits with message
        self._repo.index.commit(msg)



class PackageRepo(object):
    """
    Git Repo utils for doing package related git operations


    """
    def __init__(self, repo_dir=None):
        self.dir = repo_dir or repo_directory()
        if self.dir is None:
            msg = "Unable to determine repo dir"
            raise RuntimeError(msg)
        self.git = Repo(self.dir)
        self.gitconfig = None


    @property
    def remotes(self):
        """dict of remote name: remote instance"""
        return {r.name:r for r in self.git.remotes}

    @property
    def heads(self):
        """dict of head name: head instance"""
        return {h.name:h for h in self.git.heads}

    @property
    def tags(self):
        """dict of tag name: tag reference object """
        return {ref.name: ref for ref in self.git.tags}

    @property
    def branches(self):
        """list of branch names"""
        return list(self.heads.keys())

    def head_of(self, branch_name):
        """get reference to current head of named branch"""
        return getattr(self.git.heads, branch_name)

    @property
    def current_head(self):
        """property to access current head of current branch"""
        return self.git.head

    @property
    def head_commit(self):
        """get commit of current head"""
        return self.git.head.commit

    def remote(self, remote_name):
        """get a remote instance for the given name"""
        return self.remotes.get(remote_name)

    def remote_exists(self, remote_name):
        return self.remote(remote_name) is not None

    def fetch(self, remote=None):
        """
        fetch remote, if remote not specified, fetch all

        :param remote: remote name or None for all
        :return: None
        """
        if remote:
            self.remote(remote).fetch()
        else:
            for rem in self.git.remotes:
                rem.fetch()

    def tag_ref(self, tag):
        """get reference object for given tag"""
        return self.tags.get(tag)

    def remote_url(self, remote_name):
        """
        get the first url for the given remote

        """
        rem = self.remote(remote_name)
        urls = list(rem.urls)
        return urls[0]

    @property
    def active_branch(self):
        """current active branch reference, None if detached"""
        if self.current_head.is_detached:
            return None
        return self.git.active_branch

    @active_branch.setter
    def active_branch(self, branch_name):
        """setting the active_branch property checks out that branch"""
        if self.active_branch_name == branch_name:
            return

        if branch_name in self.heads:
            branch_ref = self.head_of(branch_name)
            branch_ref.checkout()
        else:
            self.git.git.checkout(b=branch_name)

    @property
    def active_branch_name(self):
        """get active branch name as a string"""
        if self.is_detached_head:
            return None
        return str(self.active_branch)

    @property
    def is_detached_head(self):
        """helper to check for detached head conditions"""
        return self.current_head.is_detached

    def has_untracked_files(self):
        """
        check for untracked files present in repo

        :return: True if untracked files are present
        """
        output = self.git.git.status(
            '--untracked-files=no', '--porcelain'
        ).split()
        if output:
            return True
        return False

    def remote_branches(self, remote_name):
        """
        remote_branches

        list remote branches for named remote

        :param remote_name:
        :return: list of branch names
        """
        br = self.git.git.branch(r=True)
        result = [x.strip() for x in br.split() if br.split()]
        return result

    def remote_branch_exists(self, remote, branch):
        """
        check named branch exists on specified remote

        :param remote: remote name
        :param branch: branch name
        :return: True if branch exists on remote
        """
        match = branch
        if not match.startswith(f"{remote}/"):
            match = f"{remote}/{branch}"
        return match in self.remote_branches(remote)

    def push(self, remote):
        """
        _push_

        Push current local branch to remote
        """
        rem = self.remote(remote)
        if rem is None:
            # no remote exists
            return None
        ret = rem.push(self.git.head)
        # Check to make sure that we haven't errored out.
        for r in ret:
            if r.flags >= r.ERROR:
                raise RuntimeError(r.summary)
        return ret

    def pull(self, remote):
        """
        pull current branch from remote

        :param remote:
        :return:
        """
        rem = self.remote(remote)
        rem.pull()

    def tag_release(self, tag, master_branch, remote=None, force=False):
        """
        _tag_release_

        Checkout master branch, tag it and push tags

        """
        if tag in self.tags:
            msg = (
                "Attempting to create tag {0} on "
                "{1} but tag exists already"
            ).format(tag, master_branch)
            raise RuntimeError(msg)

        with self.on_branch(master_branch):
            self.git.create_tag(tag, force=force)
            if remote:
                self.push(remote)

    def checkout_remote_branch(self, branch, remote, track=True, remote_branch=None):
        """
        checkout specified branch, updating to pull in latest remotes'
        remote name assumed as {remote}/{branch}
            if not overridden by remote_branch arg

        :param branch: name of branch to be checked out,
        :param remote: name of the remote on which the remote branch resides
        :param track: Track remote branch if True
        :param remote_branch: Name of remote branch if not same as branch

        """
        self.fetch(remote)
        remote_br = remote_branch or f"{remote}/{branch}"
        if track:
            self.git.git.checkout(
                remote_br,
                b=branch,
                track=True
            )
        else:
            self.git.git.checkout(
                remote_br,
                b=branch
            )
        self.active_branch = branch
        return

    def update_to_tag(self, tag, remote, onto_branch=True, onto_branch_name=None):
        """
        checkout specified tag, pulling remote tags first

        :param tag: tag name
        :param remote: remote name
        :param onto_branch: If True, checkout onto a branch, otherwise detach head
        :param onto_branch_name: Name of branch to checkout onto, defaults to tag/<TAG>

        """
        rem = self.remote(remote)
        rem.fetch(tags=True)

        ref = self.tag_ref(tag)
        print(f"ref={ref}")
        if onto_branch:
            branch_name = onto_branch_name or f"tag/{tag}"
            if branch_name not in self.branches:
                self.git.git.checkout(ref, b=branch_name)
            else:
                self.active_branch = branch_name
        else:
            # checkout tag commit, gives detached head state
            self.git.git.checkout(ref)
        return

    def release_notes(self, start_tag, end_tag):
        """
        generate release notes from commit messages between the two
        tags given.
        For each commit a dict entry is created containing date, author, message fields

        :param start_tag: previous tag
        :param end_tag:  current tag
        :return: list of dicts
        """
        start_ref = self.tag_ref(start_tag).commit
        end_ref = self.tag_ref(end_tag).commit
        result = self.git.git.log(start_ref, end_ref, pretty="format:%ci --- %an --- %s")
        lines = result.split('\n')
        messages = []
        for line in lines:
            elems = line.split('---', 2)
            date = elems[0].strip()
            author = elems[1].strip()
            message = elems[2].strip()
            messages.append({'date': date, 'author': author, 'message': message})
        return messages

    @contextlib.contextmanager
    def on_branch(self, branch_name, remote=None, push=False, pull=False):
        """
        context based branch helper. Checkout a branch and allow caller
        to do work on it, before reverting to previous branch

        :param branch_name: name of branch to work on
        :param remote: name of remote to sync branch with
        :return:
        """
        prev_branch = self.active_branch_name
        self.active_branch = branch_name
        if remote and pull:
            self.pull(remote)
        yield self.active_branch
        if remote and push:
            self.push(remote)
        # revert to prev
        self.active_branch = prev_branch

    def merge(self, source_branch, target_branch, remote=None, strategy=None, strategy_option=None, fastforward=True):
        """
        _merge_

        Merge source branch into destination branch

        :returns: sha of the last commit from the merged branch

        """
        with self.on_branch(target_branch) as target_br:
            if remote:
                self.pull(remote)
            kwargs = {}
            if strategy_option:
                kwargs['strategy-option'] = strategy_option
            if fastforward:
                kwargs['ff'] = True
            if strategy:
                kwargs['strategy'] = strategy
            self.git.git.merge(source_branch, target_branch, **kwargs)
            merge_ref = self.current_head.ref
        return merge_ref

    def get_diff_files(repo_dir):
        """
        _get_diff_files_

        Returns a list of paths to files that have been changed on
        the working directory
        """
        changes = self.git.index.diff(None)
        diffs = []
        for diff in changes:
            diffs.append(diff.a_blob.path)
        return diffs

    @contextlib.contextmanager
    def committer(self, branch, msg, remote=None):
        """
        work with a Committer context to add files/changes to the index

        :param branch: branch name to work on
        :param msg: commit message
        :param remote: remote name to push changes to
        :return:
        """
        comm = Committer(self.git, branch)
        with self.on_branch(branch, remote=remote, push=True):
            # yield committer to start context and add files
            yield comm
            # commit when done & push if remote provided
            comm.commit(msg)

    def initialize_branch(self, branch, remote):
        """
        branch initializer to ensure basics like 
        branch exists locally and remote and track 
        each other, plus have at least one commit
       
        :param branch: name of branch
        :param remote: remote name
        :return: 
        """
        if remote not in self.remotes:
            self.fetch()

        remote_exists = self.remote_exists(remote)
        local_br_exists = branch in self.branches
        if not remote_exists:
            remote_br_exists = False
        else:
            remote_br_exists = self.remote_branch_exists(remote, branch)
            
        with self.on_branch(branch, remote) as br:
            # checkout the branch, will create if not present
            if not local_br_exists:
                # new branch, ensure commit
                self.git.git.commit(allow_empty=True, message=f"initialize branch {branch}")
                self.git.create_head(branch, 'HEAD')

            if remote_exists and (not remote_br_exists):
                self.push(remote)

            tracking_branch = br.tracking_branch()
            if remote_exists and (not tracking_branch):
                remote_ref = self.remote(remote).refs[branch]
                br.set_tracking_branch(remote_ref)



if __name__ == '__main__':


    pr = PackageRepo('/Users/devans/Documents/cirrus_test')
    print(pr.current_head.is_detached)
    pr.active_branch = 'develop'
    print(pr.active_branch)
    # print(pr.active_branch_name)
    # print(pr.heads)
    # pr.active_branch = 'master'
    # print(pr.active_branch)
    # print(pr.active_branch_name)
    # pr.active_branch = 'develop'
    # print(pr.active_branch_name)
    # print(pr.branches)
    #
    # with pr.on_branch('test/branch') as br:
    #     print(br.name)
    #     print(pr.active_branch_name)
    #     print(pr.branches)
    #
    print(pr.branches)
    # with pr.committer('test/test', 'Adding some files') as cmt:
    #     print(pr.active_branch_name)
    #     f = '/Users/devans/Documents/cirrus_test/test1'
    #     with open(f, 'a') as handle:
    #         handle.write("testing\n")
    #     print(pr.has_untracked_files())
    #     print(cmt.diffs())
    #     cmt.add_file(f)
    #     f = '/Users/devans/Documents/cirrus_test/test2'
    #     with open(f, 'a') as handle:
    #         handle.write("testing\n")
    #     print(pr.has_untracked_files())
    #     print(cmt.diffs())
    #     cmt.add_file(f)
    #     print(cmt.diffs())
    #     print(pr.has_untracked_files())
    #
    # print(pr.has_untracked_files())
    # print(pr.active_branch_name)

    pr.initialize_branch('test/test2', 'origin')








