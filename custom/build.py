#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-

from setuptools import Command 
from setuptools._distutils import errors 
from setuptools._distutils import log
import os
import os.path
import setuptools
import shutil
import subprocess


class BuildIDL(Command):
    description = 'generate Python stubs from the IDL files'
    user_options = [
        ('omniidl=', 'o', 'omniidl compiler executable'),
        ('stubs-dir=', 's', 'directory to generate stubs in'),
        ('idl-dir=', 'i', 'directory to place IDL files in'),
        ]

    def initialize_options(self):
        log.info('initialize_options --- start')
        self.omniidl = None
        self.stubs_dir = None
        self.idl_dir = None
        self.build_lib = None
        #self.idl_path = None

    def finalize_options(self):
        log.info('finalize_options --- start')
        #if not self.idl_path:
        #    self.idl_path = 'OpenRTM_aist/RTM_IDL'
        if not self.omniidl:
            self.omniidl = 'omniidl'
        if not self.stubs_dir:
            self.set_undefined_options('build', ('build_base', 'stubs_dir'))
            self.stubs_dir = os.path.join(self.stubs_dir, 'stubs')
        if not self.idl_dir:
            self.set_undefined_options('build', ('build_base', 'idl_dir'))
            #self.idl_dir = os.path.join(self.idl_dir, self.idl_path)
            self.idl_dir = os.path.join(self.idl_dir, 'OpenRTM_aist/RTM_IDL')
        #self.idl_src_dir = os.path.join(os.getcwd(), self.idl_path)
        self.idl_src_dir = os.path.join(os.getcwd(), 'OpenRTM_aist/RTM_IDL')
        self.set_undefined_options('build', ('build_lib', 'build_lib'))

    def compile_one_idl(self, idl_f):
        outdir_param = '-C' + self.stubs_dir
        pkg_param = '-Wbpackage=OpenRTM_aist.RTM_IDL'
        #pkg_param = '-Wbstubs=OpenRTM_aist.RTM_IDL'
        #idl_path_param = '-I' + self.idl_path
        idl_path_param = '-I' + 'OpenRTM_aist/RTM_IDL'
        p = subprocess.Popen([self.omniidl, '-bpython', idl_path_param,
                              outdir_param, pkg_param, idl_f],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise errors.DistutilsExecError(
                'Failed to compile IDL file {}\nStdout:\n{}\n---\nStderr:\n'
                '{}'.format(idl_f, stdout, stderr))

    def set_idl_list(self, list_dir):
        idl_files = [os.path.join(list_dir, f)
                     for f in os.listdir(list_dir)
                     if os.path.splitext(f)[1] == '.idl']
        for f in idl_files:
            self.compile_one_idl(f)
    

    def compile_idl(self):
        log.info('Generating Python stubs from IDL files')
        self.mkpath(self.stubs_dir)
        self.set_idl_list(self.idl_src_dir)
        #idl_files = [os.path.join(self.idl_src_dir, f)
        #             for f in os.listdir(self.idl_src_dir)
        #             if os.path.splitext(f)[1] == '.idl']
        #for f in idl_files:
        #    self.compile_one_idl(f)

        # ext/rtmCamera
        idl_target_dir = os.path.join(self.idl_src_dir, 'ext/rtmCamera')
        self.set_idl_list(idl_target_dir)
        #idl_files = [os.path.join(self.idl_target_dir, f)
        #             for f in os.listdir(self.idl_target_dir)
        #             if os.path.splitext(f)[1] == '.idl']
        #for f in idl_files:
        #    self.compile_one_idl(f)

        # ext/rtmManipulator
        idl_target_dir = os.path.join(self.idl_src_dir, 'ext/rtmManipulator')
        self.set_idl_list(idl_target_dir)
        #idl_files = [os.path.join(self.idl_target_dir, f)
        #             for f in os.listdir(self.idl_target_dir)
        #             if os.path.splitext(f)[1] == '.idl']
        #for f in idl_files:
        #    self.compile_one_idl(f)

        # ../ext/sdo/observer
        idl_target_dir = os.path.join(self.idl_src_dir, '../ext/sdo/observer')
        self.set_idl_list(idl_target_dir)
        #idl_files = [os.path.join(self.idl_target_dir, f)
        #             for f in os.listdir(self.idl_target_dir)
        #             if os.path.splitext(f)[1] == '.idl']
        #for f in idl_files:
        #    self.compile_one_idl(f)

        # ../ext/fsm4rtc_observer
        idl_target_dir = os.path.join(self.idl_src_dir, '../ext/fsm4rtc_observer')
        self.set_idl_list(idl_target_dir)
        #idl_files = [os.path.join(self.idl_target_dir, f)
        #             for f in os.listdir(self.idl_target_dir)
        #             if os.path.splitext(f)[1] == '.idl']
        #for f in idl_files:
        #    self.compile_one_idl(f)

        #../examples/SimpleService
        self.set_undefined_options('build', ('build_base', 'SimpleService_dir'))
            #self.idl_dir = os.path.join(self.idl_dir, self.idl_path)
        #self.idl_dir = os.path.join(self.idl_dir, 'OpenRTM_aist/RTM_IDL')
        #idl_target_dir = os.path.join(self.idl_src_dir, '../examples/SimpleService')
        SimpleService_dir = os.path.join(self.idl_src_dir, '../examples/SimpleService')
        self.mkpath(SimpleService_dir)
        #idl_files = [os.path.join(idl_target_dir, f)
        #             for f in os.listdir(idl_target_dir)
        idl_files = [os.path.join(SimpleService_dir, f)
                     for f in os.listdir(SimpleService_dir)
                     if os.path.splitext(f)[1] == '.idl']
        #pkg_param = '-Wbstubs=OpenRTM_aist.examples.SimpleService'
        pkg_param = '-Wbpackages=OpenRTM_aist.examples.SimpleService'
        for f in idl_files:
            self.compile_example_idl(f, pkg_param)

        #../examples/AutoTest
        idl_target_dir = os.path.join(self.idl_src_dir, '../examples/AutoTest')
        idl_files = [os.path.join(idl_target_dir, f)
                     for f in os.listdir(idl_target_dir)
                     if os.path.splitext(f)[1] == '.idl']
        #pkg_param = '-Wbstubs=OpenRTM_aist.examples.AutoTest'
        pkg_param = '-Wbpackages=OpenRTM_aist.examples.AutoTest'
        for f in idl_files:
            self.compile_example_idl(f, pkg_param)

    def move_stubs(self):
        stub_dest = os.path.join(self.build_lib, 'OpenRTM_aist', 'RTM_IDL')
        log.info('Moving stubs to package directory {}'.format(stub_dest))
        self.copy_tree(os.path.join(self.stubs_dir, 'OpenRTM_aist', 'RTM_IDL'),
                       stub_dest)
        
        stub_dest = os.path.join(self.build_lib, 'OpenRTM_aist', 'examples', 'SimpleService')
        log.info('Moving stubs to package directory {}'.format(stub_dest))
        self.copy_tree(os.path.join(self.stubs_dir, 'OpenRTM_aist', 'examples', 'SimpleService'),
                       stub_dest)
        
        stub_dest = os.path.join(self.build_lib, 'OpenRTM_aist', 'examples', 'AutoTest')
        log.info('Moving stubs to package directory {}'.format(stub_dest))
        self.copy_tree(os.path.join(self.stubs_dir, 'OpenRTM_aist', 'examples', 'AutoTest'),
                       stub_dest)

    def copy_idl(self):
        log.info('Copying IDL files')
        self.mkpath(self.idl_dir)
        idl_files = [os.path.join(self.idl_src_dir, f)
                     for f in os.listdir(self.idl_src_dir)
                     if os.path.splitext(f)[1] == '.idl']
        for f in idl_files:
            shutil.copy(f, self.idl_dir)

    def compile_example_idl(self, idl_f, pkg_param):
        outdir_param = '-C' + self.stubs_dir 
        idl_path_param = '-I' + 'OpenRTM_aist/RTM_IDL'
        p = subprocess.Popen([self.omniidl, '-bpython', idl_path_param,
                              outdir_param, pkg_param, idl_f],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise errors.DistutilsExecError(
                'Failed to compile IDL file {}\nStdout:\n{}\n---\nStderr:\n'
                '{}'.format(idl_f, stdout, stderr))

    def build_example(self):
        log.info('build_example')
        example_dir = "OpenRTM_aist/examples"
        #SimpleService
        current_dir = os.path.join(example_dir, "SimpleService")
        #include_dirs = [self.idl_dir, current_dir]
        idl_files = [os.path.join(current_dir, "MyService.idl")]
        for f in idl_files:
            self.compile_example_idl(f, current_dir)
        # AutoTest
        current_dir = os.path.join(example_dir, "AutoTest")
        #include_dirs = [self.idl_dir, current_dir]
        idl_files = [os.path.join(current_dir, "AutoTestService.idl")]
        for f in idl_files:
            self.compile_example_idl(f, current_dir)

    def run(self):
        self.compile_idl()
        self.move_stubs()
        self.copy_idl()


class InstallIDL(Command):
    description = 'install the Python stubs generated from IDL files'
    user_options = [
        ('install-dir=', 'd', 'directory to install stubs to'),
        ('build-dir=', 'b', 'build directory (where to install from'),
        ('force', 'f', 'force installation (overwrite existing files)'),
        ('skip-build', None, 'skip the build steps'),
        ]
    boolean_options = ['force', 'skip-build']

    def initialize_options(self):
        self.install_dir = None
        self.install_dir = None
        self.build_dir = None
        self.force = None
        self.skip_build = None

    def finalize_options(self):
        self.set_undefined_options('build', ('build_base', 'build_dir'))
        self.set_undefined_options('install', ('install_lib', 'install_dir'),
                                   ('force', 'force'),
                                   ('skip_build', 'skip_build'))

    def run(self):
        if not self.skip_build:
            self.run_command('build_idl')
        # Copy the IDL files to rtctree/data/idl
        self.outfiles = self.copy_tree(
                os.path.join(self.build_dir, 'idl'),
                os.path.join(self.install_dir, 'rtctree', 'data', 'idl'))

    def get_outputs(self):
        return self.outfiles or []


# vim: set expandtab tabstop=8 shiftwidth=4 softtabstop=4 textwidth=79
