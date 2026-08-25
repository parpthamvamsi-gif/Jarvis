[app]
title = Jarvis
package.name = jarvis
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.1,pyjnius
requirements = python3,kivy==2.2.1,pyjnius,android

orientation = portrait
osx.kivy_version = 2.2.1

fullscreen = 0
android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.build_tools_version = 33.0.2
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
