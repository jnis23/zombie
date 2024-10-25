from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

def build(setup_kwargs):
    ext_modules = [
        Pybind11Extension(
            "firmware",
            sorted(glob("src/cpp/*.cpp")) + ['src/binding/binder.cpp'],
            include_dirs=["src/cpp/"],
            extra_compile_args=['-std=c++11'],
        ),
    ]

    setup_kwargs.update(
        name='zombie',
        version='1.0',
        description='Software for controlling the Zombie',
        author='Jan Nissen',
        packages=['zombie'],
        package_dir={'zombie': 'src'},
        ext_package='zombie',
        ext_modules=ext_modules,
        cmdclass={"build_ext": build_ext},
    )
