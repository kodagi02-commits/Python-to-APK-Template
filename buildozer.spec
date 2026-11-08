[app]
title = Hitster Reader
package.name = hitsterreader
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
version = 0.1

# Itt pontosan beállítottuk a stabil verziókat
requirements = python3, kivy==2.3.1, kivymd==1.2.0, pandas, openpyxl, qrcode, pillow, opencv-python

entrypoint = main.py
icon.filename = %(source.dir)s/kivymd/images/logo/kivymd-icon-512.png

# Android konfigurációk a KivyMD 1.2.0-hoz
android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 21

# Kamera és Internet engedélyek tisztán megadva
android.permissions = INTERNET, CAMERA

# Háttérrendszerek a fagyásmentes felhős fordításhoz
android.gradle_download = https://gradle.org
android.gradle_plugin = 7.4.2
android.sdk = 33
p4a.gradle_dependencies = gradle:7.6.4
p4a.bootstrap = sdl2
p4a.gradle_options = -Dorg.gradle.java.home=/usr/lib/jvm/java-17-openjdk-amd64
exclude_patterns = **/test/*, **/tests/*

[buildozer]
log_level = 2
warn_on_root = 1
