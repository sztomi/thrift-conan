from __future__ import print_function

from conans import ConanFile, CMake, tools
import os
import platform


class thrift(ConanFile):
    name = 'thrift'
    version = '0.9.3'
    license = 'MIT'
    repo_url = 'https://git-wip-us.apache.org/repos/asf/thrift.git'
    description = 'Apache Thrift'
    settings = 'os', 'compiler', 'build_type', 'arch'
    requires = (
            'libevent/2.0.22@theirix/stable',
            'OpenSSL/1.0.2g@lasote/stable',
            'zlib/1.2.8@lasote/stable',
            'Boost/1.60.0@lasote/stable',
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
    generators = 'cmake'
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

        with_flags = []
        for attr, _ in self.options.iteritems():
            value = getattr(self.options, attr)
            with_flags.append(option_to_flag(attr, value))

        integration_flags = [
            '--with-boost={}'.format(self.deps_cpp_info['Boost'].include_paths[0]),
            '--with-boost-libdir={}'.format(self.deps_cpp_info['Boost'].lib_paths[0]),
            '--with-openssl={}'.format(self.deps_cpp_info['OpenSSL'].include_paths[0]),
            '--with-zlib={}'.format(self.deps_cpp_info['zlib'].include_paths[0]),
            '--with-libevent={}'.format(self.deps_cpp_info['libevent'].include_paths[0]),
        ]

        other_flags = [
            '--disable-tests',
            '--disable-tutorial',
            '--disable-coverage'
        ]

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
        self.run('./bootstrap.sh')
        self.run('./configure {} {} {} --prefix={}'
                        .format(' '.join(integration_flags),
                                ' '.join(with_flags),
                                ' '.join(other_flags),
                                self.package_folder))
        self.run('make')
        self.run('make install')

    def package_info(self):
        self.cpp_info.libs = ['thrift']
        # if platform.system() == 'Linux':
            # self.cpp_info.libs.append('pthread')
