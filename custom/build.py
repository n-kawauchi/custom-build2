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

    #pkg_shortver = attr: OpenRTM_aist.version.openrtm_version
    #log.info('******** pkg_shortver {}'.format(self.pkg_shortver))


    def initialize_options(self):
        #self.pkg_shortver = None
        self.omniidl = None
        self.stubs_dir = None
        self.idl_dir = None
        self.build_lib = None
        #self.examples_dir = None
        #self.idl_path = None

    def finalize_options(self):
        #if not self.idl_path:
        #    self.idl_path = 'OpenRTM_aist/RTM_IDL'
        #if not self.pkg_shortver:
        #    self.pkg_shortver = 2.0
        if not self.omniidl:
            self.omniidl = 'omniidl'
        if not self.stubs_dir:
            self.set_undefined_options('build', ('build_base', 'stubs_dir'))
            self.stubs_dir = os.path.join(self.stubs_dir, 'stubs')
        if not self.idl_dir:
            self.set_undefined_options('build', ('build_base', 'idl_dir'))
            #self.idl_dir = os.path.join(self.idl_dir, self.idl_path)
            self.idl_dir = os.path.join(self.idl_dir, 'OpenRTM_aist/RTM_IDL')
        #if not self.examples_dir:
        #    self.set_undefined_options('build', ('build_base', 'examples_dir'))
        #    self.examples_dir = os.path.join(self.examples_dir, 'OpenRTM_aist/examples')
        #self.idl_src_dir = os.path.join(os.getcwd(), self.idl_path)
        self.idl_src_dir = os.path.join(os.getcwd(), 'OpenRTM_aist/RTM_IDL')
        self.examples_dir = os.path.join(os.getcwd(), 'OpenRTM_aist/examples')
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
            log.info('***kawa set_idl_list : f  {}'.format(f))
            self.compile_one_idl(f)
    

    def compile_idl(self):
        log.info('Generating Python stubs from IDL files')
        self.mkpath(self.stubs_dir)
        self.set_idl_list(self.idl_src_dir)

        # ext/rtmCamera
        idl_target_dir = os.path.join(self.idl_src_dir, 'ext/rtmCamera')
        self.set_idl_list(idl_target_dir)

        # ext/rtmManipulator
        idl_target_dir = os.path.join(self.idl_src_dir, 'ext/rtmManipulator')
        self.set_idl_list(idl_target_dir)

        # ../ext/sdo/observer
        idl_target_dir = os.path.join(self.idl_src_dir, '../ext/sdo/observer')
        self.set_idl_list(idl_target_dir)

        # ../ext/fsm4rtc_observer
        idl_target_dir = os.path.join(self.idl_src_dir, '../ext/fsm4rtc_observer')
        self.set_idl_list(idl_target_dir)

    def move_stubs(self):
        stub_dest = os.path.join(self.build_lib, 'OpenRTM_aist', 'RTM_IDL')
        log.info('Moving stubs to package directory {}'.format(stub_dest))
        self.copy_tree(os.path.join(self.stubs_dir, 'OpenRTM_aist', 'RTM_IDL'),
                       stub_dest)
       
        #example_install_dir = "/user/share/openrtm-" + self.pkg_shortver + "/components/python3"
        #self.mkpath(example_install_dir)
        #stub_dest = os.path.join(self.build_lib, 'OpenRTM_aist', 'examples', 'SimpleService')
        #log.info('Moving stubs to package directory {}'.format(example_install_dir))
        #self.copy_tree(self.examples_dir, example_install_dir)
        

    def copy_idl(self):
        log.info('Copying IDL files')
        self.mkpath(self.idl_dir)
        idl_files = [os.path.join(self.idl_src_dir, f)
                     for f in os.listdir(self.idl_src_dir)
                     if os.path.splitext(f)[1] == '.idl']
        for f in idl_files:
            shutil.copy(f, self.idl_dir)

    #def compile_example_idl(self, idl_f, include_dirs, current_dir, pkg_param):
    def compile_example_idl(self, idl_f, pkg_param):
        #outdir_param = '-C' + current_dir 
        outdir_param = '-C' + self.stubs_dir 
        log.info('***kawa compile_example_idl : idl_f {}'.format(idl_f))
        idl_path_param = '-IOpenRTM_aist/RTM_IDL ' + idl_f
        #idl_path_param = '-I' + self.idl_src_dir + ' ' + idl_f
        log.info('***kawa compile_example_idl : idl_path_param {}'.format(idl_path_param))
        p = subprocess.Popen([self.omniidl, '-bpython', idl_path_param,
                              outdir_param, pkg_param, idl_f],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise errors.DistutilsExecError(
                'Failed to compile IDL file {}\nStdout:\n{}\n---\nStderr:\n'
                '{}'.format(idl_f, stdout, stderr))

    def compile_example_idl(self):
        log.info('Generating Python stubs from examples IDL files')
        #../examples/SimpleService
        self.mkpath(self.examples_dir)
        current_dir = os.path.join(self.examples_dir, 'SimpleService')
        idl_file = os.path.join(current_dir, "MyService.idl")
        pkg_param = '-Wbpackages=OpenRTM_aist.examples.SimpleService'
        self.compile_example_idl(idl_file, pkg_param)

        #../examples/AutoTest
        current_dir = os.path.join(self.examples_dir, 'AutoTest')
        idl_file = os.path.join(current_dir, "AutoTestService.idl")
        pkg_param = '-Wbpackages=OpenRTM_aist.examples.AutoTest'
        self.compile_example_idl(idl_file, pkg_param)


    def run(self):
        self.compile_idl()
        self.move_stubs()
        self.copy_idl()
        self.compile_example_idl()


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
