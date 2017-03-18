#glfw
from conans import ConanFile, tools, AutoToolsBuildEnvironment
import zipfile
import os

class GlfwConan(ConanFile):
	name = "GLFW"
	version = "3.2.1"
	license = "zlib/libpng license"
	settings = "os", "compiler", "build_type", "arch"
	url = "https://github.com/Brunni/conan-GLFW"
	options = {
		"shared": [True, False]
	}
	default_options = "shared=False"

	def source(self):
		if self.settings.compiler != "Visual Studio":
			# TODO: Restrict settings
			raise ConanException("Not valid compiler")
		windowsBit = "32" if self.settings.arch == "x86" else "64";
		glfwurl = "https://github.com/glfw/glfw/releases/download/{0}/glfw-{0}.bin.WIN{1}.zip".format(self.version, windowsBit)
		tools.download(glfwurl, "glfw.zip")
		zip_ref = zipfile.ZipFile("glfw.zip", 'r')
		zip_ref.extractall()
		zip_ref.close()
		zipfoldername = "glfw-{0}.bin.WIN{1}".format(self.version, windowsBit)
		os.rename(zipfoldername, "glfwbin")

	def package(self):
		self.copy("*.h", dst="include", src="glfwbin/include")
		compilerSubfolder = "glfwbin/lib-vc20%s" % str(int(self.settings.compiler.version.value)+1)
		print("Searching in subfolder %s" % compilerSubfolder)
		if self.options.shared:
			self.copy("glfw3dll.lib", dst="lib", src=compilerSubfolder, keep_path=False)
			self.copy("*.dll", dst="bin", src=compilerSubfolder, keep_path=False)
		else:
			self.copy("glfw3.lib", dst="lib", src=compilerSubfolder, keep_path=False)

		
	def package_info(self):
		if self.options.shared:
			self.cpp_info.libs = ["glfw3dll"]
		else:
			self.cpp_info.libs = ["glfw3"]
