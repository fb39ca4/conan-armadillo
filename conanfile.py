from conans import ConanFile, CMake, tools
import os
import shutil

class ArmadilloConan(ConanFile):
    name = "armadillo"
    version = "8.400.0"
    license = "Apache License 2.0"
    url = "http://arma.sourceforge.net/"
    description = "Armadillo is a high quality linear algebra library (matrix maths) for the C++ language, aiming towards a good balance between speed and ease of use"
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = ""
    generators = "cmake"
    requires = ("lapack/3.7.1@conan/stable",)# "openblas/0.2.20@conan/stable")
    
    def configure(self):
        if self.settings.compiler == "Visual Studio":
            self.options["lapack"].CMAKE_GNUtoMS = True

    def source(self):
        zip_name = "armadillo-%s.tar.xz" % self.version
        folder_name = "armadillo-%s" % self.version
        tools.download("https://iweb.dl.sourceforge.net/project/arma/" + zip_name, filename=zip_name)
        tools.untargz(zip_name)
        os.unlink(zip_name)
        shutil.move(folder_name, "armadillo")
        shutil.move("armadillo/CMakeLists.txt", "armadillo/CMakeListsOriginal.cmake")
        tools.download("https://raw.githubusercontent.com/fb39ca4/conan-armadillo/master/CMakeLists.txt", filename="CMakeLists.txt")
        shutil.copyfile("CMakeLists.txt", "armadillo/CMakeLists.txt")
        
    def build(self):
        cmake = CMake(self)
        cmake.configure(build_dir="build", source_dir="../armadillo")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("armadillo_bits/*", dst="include", src="armadillo/include")
        self.copy("armadillo", dst="include", src="armadillo/include")
        self.copy("*.lib", dst="lib", src="build", keep_path=False)
        self.copy("*.dll", dst="bin", src="build", keep_path=False)
        self.copy("*.so", dst="lib", src="build", keep_path=False)
        self.copy("*.dylib", dst="lib", src="build", keep_path=False)
        self.copy("*.a", dst="lib", src="build", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["armadillo"]

