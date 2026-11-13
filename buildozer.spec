[app]

# (str) Title of your application
title = Щоденник спостережень

# (str) Package name
package.name = observationdiary

# (str) Package domain (needed for android packaging)
package.domain = org.observation

# (str) Source files where the let's go (relative to directory of spec)
source.include_exts = py,png,jpg,kv,atlas

# (str) Directory where the source files are located
source.dir = .

# (string) Version of the application
version = 1.0

# (list) Application requirements
requirements = python3,kivy,setuptools,plyer

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECORD_AUDIO

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (bool) Enable AndroidX support
android.androidx = True

# (list) The android api to target that you want for the application
android.api = 33

# (list) Minimum API your APK / AAB will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (str) The Android arch to build for, options: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = armeabi-v7a

# (bool) Use --private data storage (True) or public storage (False)
android.private_storage = True

[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_root = 1
