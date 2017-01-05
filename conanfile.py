from __future__ import print_function

from conans import ConanFile, CMake, tools
import os
import platform
import subprocess


class thrift(ConanFile):
    name = 'thrift'
    version = '0.9.3'
    license = 'MIT'
    url = 'https://github.com/sztomi/thrift-conan'
    repo_url = 'https://git-wip-us.apache.org/repos/asf/thrift.git'
    description = 'Apache Thrift'
    settings = 'os', 'compiler', 'build_type', 'arch'
    requires = (
        'libevent/2.0.22@theirix/stable',
        'OpenSSL/1.0.2g@lasote/stable',
        'zlib/1.2.8@lasote/stable',
        'Boost/1.60.0@lasote/stable',
        'm4/latest@sztomi/testing',
        'libtool/2.4.6@sztomi/testing',
        'autoconf/2.69@sztomi/testing',
        'automake/1.15@sztomi/testing',
        'pkg-config/0.29.1@sztomi/testing',
        'bison/3.0.4@sztomi/testing',
        'flex/2.6.3@sztomi/testing'
    )
    options = {
        'build_qt4_lib': [True, False],
        'build_qt5_lib': [True, False],
        'build_c_glib_lib': [True, False],
        'build_csharp_lib': [True, False],
        'build_java_lib': [True, False],
        'build_erlang_lib': [True, False],
        'build_nodejs_lib': [True, False],
        'build_lua_lib': [True, False],
        'build_python_lib': [True, False],
        'build_perl_lib': [True, False],
        'build_php_lib': [True, False],
        'build_php_extension_lib': [True, False],
        'build_ruby_lib': [True, False],
        'build_haskell_lib': [True, False],
        'build_go_lib': [True, False],
        'build_d_lib': [True, False],
        'build_tests': [True, False],
    }
    default_options = (
        'build_qt4_lib=False',
        'build_qt5_lib=False',
        'build_c_glib_lib=False',
        'build_csharp_lib=False',
        'build_java_lib=False',
        'build_erlang_lib=False',
        'build_nodejs_lib=False',
        'build_lua_lib=False',
        'build_python_lib=False',
        'build_perl_lib=False',
        'build_php_lib=False',
        'build_php_extension_lib=False',
        'build_ruby_lib=False',
        'build_haskell_lib=False',
        'build_go_lib=False',
        'build_d_lib=False',
        'build_tests=False',
    )
    generators = 'cmake', 'virtualenv'
    src_dir = 'thrift'

    def source(self):
        self.run(
            'git clone --branch {} --depth 1 {} {}'.format(
                                self.version,
                                self.repo_url,
                                self.src_dir))

    def build(self):
        def option_to_flag(opt, value):
            flag_name = opt.split('_')[1]
            return '--with-{}={}'.format(flag_name,
                    'yes' if value else 'no')
        def up_one(folder):
            return os.path.abspath(os.path.join(folder, '..'))

        with_flags = []
        for attr, _ in self.options.iteritems():
            value = getattr(self.options, attr)
            with_flags.append(option_to_flag(attr, value))

        integration_flags = [
            '--with-boost={}'.format(up_one(self.deps_cpp_info['Boost'].include_paths[0])),
            '--with-boost-libdir={}'.format(self.deps_cpp_info['Boost'].lib_paths[0]),
            '--with-openssl={}'.format(up_one(self.deps_cpp_info['OpenSSL'].include_paths[0])),
            '--with-zlib={}'.format(up_one(self.deps_cpp_info['zlib'].include_paths[0])),
            '--with-libevent={}'.format(up_one(self.deps_cpp_info['libevent'].include_paths[0])),
        ]

        other_flags = [
            '--disable-tests',
            '--disable-tutorial',
            '--disable-coverage',
            '--disable-shared',
        ]
        
        env_vars = dict(
            PKG_PROG_PKG_CONFIG = os.path.join(self.deps_env_info['pkg-config'].path[0], 'pkg-config'),
            LIBS = '-ldl',
            LDFLAGS = '-L{}'.format(self.deps_cpp_info['OpenSSL'].lib_paths[0]),
            ACLOCAL_PATH = '$ACLOCAL_PATH:{}'.format(self.deps_env_info['pkg-config'].path[1])
        )
        
        env_str = ''
        
        for key, value in env_vars.items():
            env_str += '{}="{}" '.format(key, value)
            
        print(env_str)

        def patch_files():
            filename = 'lib/cpp/src/thrift/transport/TSSLSocket.cpp'
            old_string = 'SSLv3_method'
            new_string = 'SSLv23_method'
            with open(filename) as f:
                contents = f.read()
                if old_string not in contents:
                    print('"{old_string}" not found in {filename}.'.format(**locals()))
                    return

            with open(filename, 'w') as f:
                print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
                contents = contents.replace(old_string, new_string)
                f.write(contents)
                
        os.chdir(self.src_dir)
        patch_files()
        
        def run_in_env(cmd):
            activate = '. ../activate.sh && '
            self.run(activate + cmd)
            
        run_in_env('{} ./bootstrap.sh'.format(env_str))

        conf = '{} bash -c "./configure {} {} {}"'.format(
                                env_str,
                                ' '.join(integration_flags),
                                ' '.join(with_flags),
                                ' '.join(other_flags))
        run_in_env(conf)
        run_in_env('make')

    def package(self):
        self.copy('*.h', src='thrift/lib/cpp/src', dst='include')
        self.copy('*.tcc', src='thrift/lib/cpp/src', dst='include')
        self.copy('*.so', dst='lib', keep_path=False)
        self.copy('*.dll', dst='lib', keep_path=False)
        self.copy('*.lib', dst='lib', keep_path=False)
        self.copy('*.a', dst='lib', keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['thrift']
