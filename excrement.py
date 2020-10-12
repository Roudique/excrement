#!/usr/bin/env python3

import sys, os, re, subprocess
from enum import Enum


class Subversion(Enum):
    MAJOR = 0
    MINOR = 1
    PATCH = 2


class Operation(Enum):
    INCREMENT = 0
    DECREMENT = 1


class Version_Parser(object):
    def __init__(self, string):
        super(Version_Parser, self).__init__()
        self.string = string
    
    def _versions(self, string):
        versions = string.split('.')
        if len(versions) == 0:
            return
            
        major, minor, patch = None, None, None
        
        major = int(versions[0])
        
        if len(versions) > 1:
            minor = int(versions[1])
        if len(versions) > 2:
            patch = int(versions[2])
        
        return (major, minor, patch)
    
    def _apply(self, operation: Operation, to_number):
        if operation is Operation.INCREMENT:
            return to_number + 1
        elif operation is Operation.DECREMENT:
            result = to_number - 1
            return result if result > 0 else 0

    def update(self, version: Subversion, operation: Operation):
        major, minor, patch = self._versions(self.string)
        
        if version == Subversion.MAJOR:
            if major is None:
                major = 0
            major = self._apply(operation, major)
        elif version == Subversion.MINOR:
            if major is None:
                major = 0
            if minor is None:
                minor = 0
            minor = self._apply(operation, minor)
        elif version == Subversion.PATCH:
            if major is None:
                major = 0
            if minor is None:
                minor = 0
            if patch is None:
                patch = 0
            patch = self._apply(operation, patch)
        
        incremented = f"{major}"
        
        for item in (minor, patch):
            if item is not None:
                incremented += f".{item}"
        
        return incremented


class Reader(object):
    def __init__(self):
        super(Reader, self).__init__()

    def _get_version(self, line, version_name):
        if version_name in line:
            result = re.search(' = (.*);', line)
            version = result.group(1)
            return version
        else:
            return None

    def _find_pbxproj(self):
        directory_contents = os.listdir('.')
        
        for item in directory_contents:
            if not os.path.isdir(item):
                pass
            if 'xcodeproj' in item:
                return f"{item}/project.pbxproj"
        
        return None

    def _find_xcode_projfile(self):
        """Finds and returns project version and build version
        """
        project_version = None
        build_version = None
        
        path_to_proj = self._find_pbxproj()
        if path_to_proj is None:
            raise SomeException()
        
        f = open(path_to_proj)
        lines = f.readlines()
        
        for line in lines:
            if build_version is None:
                version = self._get_version(line, 'CURRENT_PROJECT_VERSION')
                if version is not None:
                    build_version = version
            
            if project_version is None:
                version = self._get_version(line, 'MARKETING_VERSION')
                if version is not None:
                    project_version = version
        
        f.close
        
        return (project_version, build_version)

    def _replace_versions_if_needed(self, 
        string, 
        project, build):
    
        build_version = re.search('CURRENT_PROJECT_VERSION = (.*);', string)
        if build_version is not None:
            return string.replace(build_version.group(1), build)
        
        project_version = re.search('MARKETING_VERSION = (.*);', string)
        if project_version is not None:
            return string.replace(project_version.group(1), project)
        
        return string

    def _write(self, project_version, build_version):
        path_to_proj = self._find_pbxproj()
        if path_to_proj is None:
            raise SomeException()
        
        lines = None
        
        with open(path_to_proj, 'r') as file:
            lines = file.readlines()
        
        new_lines = [self._replace_versions_if_needed(l, project_version, build_version) for l in lines]
        
        with open(path_to_proj, 'w') as file:
            data = ''.join(new_lines)
            file.write(data)

    def read_project_version(self):
        return self._find_xcode_projfile()


def help():
    print(
        '''
        This is help message.
        Read it.
        '''
        )

def current():
    reader = Reader()
    project, build = reader.read_project_version()
    s = "Project version: {project}\nBuild: {build}".format(project=project, build=build)
    print(s)

def commit():
    reader = Reader()
    project, build = reader.read_project_version()
    commit_message = f'Upgrade to version {project}, build {build}'
    
    print(f">>>>> Commiting changes with commit message: {commit_message}")
    subprocess.run(["git", "add", "-A"])
    subprocess.run(["git", "commit", "-m", commit_message])

def tag():
    reader = Reader()
    project, _ = reader.read_project_version()
    print(f">>>>> Creating tag: {project}")
    subprocess.run(["git", "tag", project])

def increment(to_version):
    reader = Reader()
    project, build = reader.read_project_version()
    parser = Version_Parser(project)
    new_project = parser.update(to_version, operation=Operation.INCREMENT)
    new_build = int(build) + 1
    new_build = f"{new_build}"
    reader._write(new_project, new_build)

def main(argv):
    if len(argv) == 0:
        return
    
    argument = argv[0]
    
    if argument == 'help' or argument == '-h':
        help()
    elif argument == 'current':
        current()
    elif argument == 'major':
        increment(Subversion.MAJOR)
    elif argument == 'minor':
        increment(Subversion.MINOR)
    elif argument == 'patch':
        increment(Subversion.PATCH)
    
    if len(argv) <= 1:
        return
    argument2 = argv[1]
    if argument2 == 'git':
        commit()
    
    if len(argv) <= 2:
        return
    argument3 = argv[2]
    if argument3 == 'tag':
        tag()

if __name__ == "__main__":
    main(sys.argv[1:])

