from conan.tools.files import copy
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.build import can_run, check_min_cppstd
    
class AsioChan(ConanFile):
    name = "asiochan"
    version = "0.4.3"
    description = "C++20 coroutine channels for ASIO"
    homepage = "https://github.com/MiSo1289/asiochan"
    url = "https://github.com/MiSo1289/asiochan"
    license = "MIT"
    settings = ("os", "compiler", "arch", "build_type")
    exports_sources = (
        "examples/*",
        "include/*",
        "tests/*",
        "CMakeLists.txt",
    )
    options = {
        "asio": ["boost", "standalone"]
    }
    default_options = {
        "asio": "boost",
    }
    no_copy_source = True

    def validate(self):
        check_min_cppstd(self, "20")

    def requirements(self):
        self.test_requires("catch2/2.13.7")
        if self.options.asio == "boost":
            self.requires("boost/1.84.0")
        else:
            self.requires("asio/[>=1.18.1 <=1.29.0]")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        if self.options.asio == "standalone" :
            tc.variables["WITH_IGH"] = True
            tc.variables["ASIOCHAN_USE_STANDALONE_ASIO"]=True
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

        if (not self.conf.get("tools.build:skip_test", default=False)) and can_run(self):
            cmake.test()

    def package(self):
        copy(self, "*.hpp", self.source_folder, self.package_folder)

    def package_id(self):
        self.info.clear()

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        if self.options.asio == "standalone":
            self.cpp_info.defines = ["ASIOCHAN_USE_STANDALONE_ASIO"]
