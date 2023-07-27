#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-

from setuptools import Command 
from setuptools._distutils import errors 
from setuptools._distutils import log
from setuptools._distutils import util
from setuptools._distutils import cmd
import os
import os.path
import setuptools
import shutil
import subprocess


class BuildIDL(Command):
    description = 'generate Python stubs from the IDL files'
#    user_options = [
#        ('omniidl=', 'o', 'omniidl compiler executable'),
#        ('stubs-dir=', 's', 'directory to generate stubs in'),
#        ('idl-dir=', 'i', 'directory to place IDL files in'),
#        ]


    def initialize_options(self):
        self.omniidl = None
        self.stubs_dir = None
        self.idl_dir = None
        self.build_lib = None

    def finalize_options(self):
        if not self.omniidl:
            self.omniidl = 'omniidl'
        if not self.stubs_dir:
            self.set_undefined_options('build', ('build_base', 'stubs_dir'))
            self.stubs_dir = os.path.join(self.stubs_dir, 'stubs')
        if not self.idl_dir:
            self.set_undefined_options('build', ('build_base', 'idl_dir'))
            self.idl_dir = os.path.join(self.idl_dir, 'OpenRTM_aist/RTM_IDL')
        self.idl_src_dir = os.path.join(os.getcwd(), 'OpenRTM_aist/RTM_IDL')
        self.examples_dir = os.path.join(os.getcwd(), 'OpenRTM_aist/examples')
        self.set_undefined_options('build', ('build_lib', 'build_lib'))

    def compile_one_idl(self, idl_f):
        outdir_param = '-C' + self.stubs_dir
        pkg_param = '-Wbpackage=OpenRTM_aist.RTM_IDL'
        idl_path_param = '-I' + 'OpenRTM_aist/RTM_IDL'
        if 'Manipulator' in f:
            idl_path_param += ' -I' + 'OpenRTM_aist/RTM_IDL/ext'
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
            log.info('***kawa set_idl_list : {}'.format(f))
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
    
    def copy_examples_idl(self):
        log.info('Copying IDL files of sample RTC')
        example_dest= os.path.join(self.build_lib, 'OpenRTM_aist', 'examples', 'AutoTest')
        target_dir = os.path.join(self.examples_dir, 'AutoTest')
        self.copy_tree(target_dir, example_dest)
        
        example_dest= os.path.join(self.build_lib, 'OpenRTM_aist', 'examples', 'SimpleService')
        target_dir = os.path.join(self.examples_dir, 'SimpleService')
        self.copy_tree(target_dir, example_dest)
       

    def copy_idl(self):
        log.info('Copying IDL files')
        self.mkpath(self.idl_dir)
        idl_files = [os.path.join(self.idl_src_dir, f)
                     for f in os.listdir(self.idl_src_dir)
                     if os.path.splitext(f)[1] == '.idl']
        for f in idl_files:
            shutil.copy(f, self.idl_dir)

    def compile_example_idl(self, idl_f, pkg_param, current_dir):
        outdir_param = '-C' + current_dir 
        idl_path_param = '-IOpenRTM_aist/RTM_IDL ' + idl_f
        p = subprocess.Popen([self.omniidl, '-bpython', idl_path_param,
                              outdir_param, pkg_param, idl_f],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise errors.DistutilsExecError(
                'Failed to compile IDL file {}\nStdout:\n{}\n---\nStderr:\n'
                '{}'.format(idl_f, stdout, stderr))

    def examples_idl(self):
        log.info('Generating Python stubs from examples IDL files')
        #../examples/SimpleService
        self.mkpath(self.examples_dir)
        current_dir = os.path.join(self.examples_dir, 'SimpleService')
        idl_file = os.path.join(current_dir, "MyService.idl")
        pkg_param = '-Wbpackages=OpenRTM_aist.examples.SimpleService'
        self.compile_example_idl(idl_file, pkg_param, current_dir)

        #../examples/AutoTest
        current_dir = os.path.join(self.examples_dir, 'AutoTest')
        idl_file = os.path.join(current_dir, "AutoTestService.idl")
        pkg_param = '-Wbpackages=OpenRTM_aist.examples.AutoTest'
        self.compile_example_idl(idl_file, pkg_param, current_dir)


    def run(self):
        self.compile_idl()
        self.move_stubs()
        self.copy_idl()
        self.examples_idl()
        self.copy_examples_idl()


class BuildDoc(Command):
    description = 'Generate documentation from source code.'
#    user_options = [
#        ('install-dir=', 'd', 'directory to install stubs to'),
#        ('build-dir=', 'b', 'build directory (where to install from'),
#        ('force', 'f', 'force installation (overwrite existing files)'),
#        ('skip-build', None, 'skip the build steps'),
#        ]
#    boolean_options = ['force', 'skip-build']

    def initialize_options(self):
        self.doxygen = None

    def finalize_options(self):
        if not self.doxygen:
            self.doxygen = 'doxygen'
        self.document_path = os.path.join(os.getcwd(), 'OpenRTM_aist/docs')

    def create_doc(self, doxygen_conf, target_dir):
        """
        create_doc
        - doxygen_conf: [string] path to Doxygen's conf file
        - target_dir  : [string] directory to where doxygen generates documentation
    	"""
        def exec_doxygen(cmd):
            # remove target dir
            if os.path.exists(target_dir + "/html/index.html"):
                return
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)

            #cmdline = string.join(cmd)
            cmdline = " ".join(cmd)
            #if os_is() == "win32":
            #    os.system(cmdline)
            #    return
            log.info(cmdline)
            try:
                proc = subprocess.run(
                    cmdline,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
                status = 0
                log.info(proc.stdout.decode("UTF-8"))
            except BaseException:
                status = 1

            if status != 0:
                raise errors.DistutilsExecError("Return status of %s is %d" %
                                            (cmd, status))
            return
        # compile IDL by using dist.util.execute
        docdir = os.path.dirname(doxygen_conf)
        tmp = os.getcwd()
        os.chdir(docdir)
        cmd = ["doxygen", doxygen_conf]
        util.execute(exec_doxygen, [cmd],
                   "Generating documentation")
        os.chdir(tmp)

    def build_doc_common(self, infile, outfile):
        f_input = open(infile, 'r')
        src = f_input.read()
        f_input.close()
        #dst = src.replace("__VERSION__", pkg_version)
        dst = src.replace("__VERSION__", "2.0.2")
        f_output = open(outfile, 'w')
        f_output.write(dst)
        f_output.close()

    def run(self):
        conf_in_file = os.path.normpath(self.document_path + "/Doxyfile_en.in")
        conf_file = os.path.normpath(self.document_path + "/Doxyfile_en")
        self.build_doc_common(conf_in_file, conf_file)
        target_dir = os.path.normpath(self.document_path + "/ClassReference-en")
        self.create_doc(conf_file, target_dir)

        conf_in_file = os.path.normpath(self.document_path + "/Doxyfile_jp.in")
        conf_file = os.path.normpath(self.document_path + "/Doxyfile_jp")
        self.build_doc_common(conf_in_file, conf_file)
        target_dir = os.path.normpath(self.document_path + "/ClassReference-jp")
        self.create_doc(conf_file, target_dir)

# vim: set expandtab tabstop=8 shiftwidth=4 softtabstop=4 textwidth=79
