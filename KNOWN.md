# Projects v.s. Code Repositories

Boa projects have an array of repositories. How big is this array? What does it
even mean to have more or less than 1 repository?

Script: coderepository-count.boa

Results (large GitHub): http://boa.cs.iastate.edu/boa/?q=boa/job/33535

```
counts  0   174853
counts  1   380011
```

# Is it always the case that project_url = "https://github.com/" + project.name?

Script: name-url-relation.boa

Results (large GitHub): yes

```
counts    true    7830023
```

# What are the most commmon .md and .txt and no-extension files?

Script: common-documentation.boa

Results: Seems like only readme.md and readme.txt are there in significant numbers.

```
counts = readme.md, 105270.0
counts = readme, 39852.0
counts = proguard-project.txt, 21360.0
counts = license, 14963.0
counts = readme.txt, 10506.0
counts = license.txt, 7576.0
counts = makefile, 3205.0
counts = copying, 3077.0
counts = notice, 2965.0
counts = conf/routes, 2723.0
counts = gradlew, 2437.0
counts = .metadata/.plugins/org.eclipse.jdt.core/savedindexnames.txt, 1589.0
counts = doc/package-list, 1522.0
counts = .metadata/.plugins/org.eclipse.jdt.core/javalikenames.txt, 1510.0
counts = module_license_apache2, 1480.0
counts = todo, 1459.0
counts = conf/messages, 1430.0
counts = dist/readme.txt, 1350.0
counts = changelog, 1260.0
counts = procfile, 1202.0
counts = rakefile, 1064.0
counts = license.md, 1055.0
counts = bin/r.txt, 1043.0
counts = authors, 976.0
counts = todo.txt, 935.0
counts = notice.txt, 898.0
counts = install, 804.0
counts = test.txt, 750.0
counts = gemfile, 740.0
counts = changelog.txt, 640.0
counts = configure, 483.0
counts = public/robots.txt, 479.0
counts = android/proguard-project.txt, 478.0
counts = licence, 462.0
counts = changes.txt, 455.0
counts = cmakelists.txt, 417.0
counts = news, 406.0
counts = doc/readme_for_app, 404.0
counts = licence.txt, 398.0
counts = script/rails, 385.0
counts = changelog.md, 376.0
counts = version, 374.0
counts = copying.txt, 369.0
counts = javadoc/package-list, 368.0
counts = src/makefile, 360.0
counts = debian/control, 354.0
counts = cordova/log, 352.0
counts = debian/changelog, 348.0
counts = debian/rules, 347.0
counts = debian/compat, 338.0
counts = cordova/clean, 333.0
counts = debian/copyright, 310.0
counts = test, 309.0
counts = changes, 307.0
counts = cordova/run, 284.0
counts = manifest, 279.0
counts = notes.txt, 278.0
counts = .metadata/.plugins/org.eclipse.jdt.core/indexnamesmap.txt, 270.0
counts = cordova/build, 270.0
counts = install.txt, 270.0
counts = gpl.txt, 263.0
counts = install-sh, 263.0
counts = copyright.txt, 262.0
counts = docs/readme.txt, 257.0
counts = manifest.txt, 257.0
counts = license-2.0.txt, 252.0
counts = bin/proguard.txt, 238.0
counts = header.txt, 232.0
counts = cordova/cordova, 227.0
counts = src/readme, 224.0
counts = doxyfile, 222.0
counts = todo.md, 218.0
counts = doc/makefile, 217.0
counts = bsd_license_for_wpilib_code.txt, 215.0
counts = copyright, 209.0
counts = lib/readme, 204.0
counts = version.txt, 204.0
counts = src/readme.txt, 203.0
counts = www/res/screen/tizen/readme.md, 203.0
counts = readme~, 201.0
counts = tmp/bytecode/dev/docviewerplugin, 201.0
counts = output.txt, 199.0
counts = missing, 197.0
counts = platforms/android/proguard-project.txt, 194.0
counts = actionbarsherlock/readme.md, 192.0
counts = buildfile, 190.0
counts = log.txt, 189.0
counts = robots.txt, 187.0
counts = run, 184.0
counts = test/proguard-project.txt, 183.0
counts = doc/readme, 181.0
counts = cordova/release, 179.0
counts = lib/readme.txt, 178.0
counts = contributing.md, 170.0
counts = input.txt, 166.0
counts = doc/readme.txt, 165.0
counts = contributors, 162.0
counts = google-play-services_lib/readme.txt, 160.0
counts = depcomp, 159.0
counts = credits, 156.0
counts = proj.android/proguard-project.txt, 154.0
counts = .metadata/.plugins/org.eclipse.wst.jsdt.core/indexes/savedindexnames.txt, 153.0
counts = platforms/android/assets/www/res/screen/tizen/readme.md, 148.0
counts = src/etc/header.txt, 146.0
counts = notes, 145.0
counts = gpl-3.0.txt, 144.0
counts = proguard/seeds.txt, 143.0
counts = config, 142.0
counts = debian/source/format, 142.0
counts = platforms/android/cordova/clean, 142.0
counts = platforms/android/cordova/log, 142.0
counts = proguard/dump.txt, 141.0
counts = myfirstapp/proguard-project.txt, 140.0
counts = platforms/android/cordova/build, 139.0
counts = platforms/android/cordova/run, 139.0
counts = proguard/mapping.txt, 138.0
counts = proguard/usage.txt, 137.0
counts = keywords.txt, 136.0
counts = platforms/android/cordova/lib/install-device, 136.0
counts = platforms/android/cordova/lib/install-emulator, 136.0
counts = platforms/android/cordova/lib/list-devices, 136.0
counts = platforms/android/cordova/lib/list-emulator-images, 136.0
counts = platforms/android/cordova/lib/list-started-emulators, 136.0
counts = platforms/android/cordova/lib/start-emulator, 136.0
counts = mkinstalldirs, 135.0
counts = compile, 134.0
counts = platforms/android/cordova/version, 134.0
counts = maintainers, 133.0
counts = test/makefile, 131.0
counts = project/target/streams/$global/update/$global/out, 130.0
counts = debian/docs, 129.0
counts = dist/javadoc/package-list, 129.0
counts = project/target/streams/compile/compile/$global/out, 128.0
counts = mit-license.txt, 127.0
counts = project/target/streams/compile/$global/$global/data, 127.0
counts = docs/package-list, 126.0
counts = app/proguard-project.txt, 125.0
counts = src/main/webapp/robots.txt, 125.0
counts = build, 124.0
counts = keystore, 123.0
counts = proprietary-files.txt, 120.0
counts = core/makefile, 118.0
counts = helloworld/proguard-project.txt, 118.0
counts = project/target/streams/$global/ivy-sbt/$global/out, 117.0
counts = target/streams/$global/update/$global/out, 117.0
counts = library/proguard-project.txt, 116.0
counts = project/target/streams/$global/compilers/$global/out, 116.0
counts = project/target/streams/$global/ivy-configuration/$global/out, 116.0
counts = project/target/streams/$global/project-descriptors/$global/out, 116.0
counts = project/target/streams/compile/compile-inputs/$global/out, 115.0
counts = src/org/json/readme, 115.0
counts = target/streams/compile/compile/$global/out, 115.0
counts = tests/proguard-project.txt, 115.0
counts = examples/readme, 114.0
counts = project/target/streams/compile/copy-resources/$global/out, 114.0
counts = project/target/streams/compile/defined-sbt-plugins/$global/out, 114.0
counts = src/test/resources/keystore, 113.0
counts = target/streams/compile/$global/$global/data, 112.0
counts = release-notes.txt, 111.0
counts = cordova/lib/list-devices, 108.0
counts = cordova/version, 108.0
counts = tools/releasetools/ota_from_target_files, 108.0
counts = tools/releasetools/sign_target_files_apks, 108.0
counts = cordova/lib/install-device, 107.0
counts = cordova/lib/install-emulator, 107.0
counts = cordova/lib/list-emulator-images, 107.0
counts = cordova/lib/list-started-emulators, 107.0
counts = cordova/lib/start-emulator, 107.0
counts = debian/dirs, 107.0
counts = doc/javadoc/package-list, 107.0
counts = examples/makefile, 107.0
counts = workspace/.metadata/.plugins/org.eclipse.jdt.core/savedindexnames.txt, 107.0
counts = adb/overview.txt, 106.0
counts = adb/protocol.txt, 106.0
counts = adb/services.txt, 106.0
counts = building.txt, 106.0
counts = core/apicheck_msg_current.txt, 106.0
counts = core/apicheck_msg_last.txt, 106.0
counts = core/checktree, 106.0
counts = debuggerd/module_license_apache2, 106.0
counts = debuggerd/notice, 106.0
counts = history.txt, 106.0
counts = init/module_license_apache2, 106.0
counts = init/notice, 106.0
counts = init/readme.txt, 106.0
counts = kernel, 106.0
counts = libctest/notice, 106.0
counts = libcutils/module_license_apache2, 106.0
counts = libcutils/notice, 106.0
counts = liblog/notice, 106.0
counts = libmincrypt/notice, 106.0
counts = libnetutils/notice, 106.0
counts = libpixelflinger/module_license_apache2, 106.0
counts = libpixelflinger/notice, 106.0
counts = libzipfile/module_license_apache2, 106.0
counts = libzipfile/notice, 106.0
counts = logcat/module_license_apache2, 106.0
counts = logcat/notice, 106.0
counts = logwrapper/notice, 106.0
counts = netcfg/module_license_apache2, 106.0
```

# What is the distribution of lifespan of projects?

Script: activity-span.boa + parse into nicer format

Results:

```
Project lifespans in days
Invalid (no commits?): 97317
[0, 0]:         87069
[1, 2]:         23284
[3, 6]:         19377
[7, 14]:        20942
[15, 30]:       21248
[31, 62]:       21583
[63, 126]:      20229
[127, 254]:     16513
[255, 510]:     13514
[511, 1022]:    8528
[1023, 2046]:   4408
[2047, 4094]:   1365
[4095, 8190]:   201
[8191, 16382]:  62
[32767, 65534]: 1
```

Alternate result from analysis.py
```
[0, 0]:         86444
[1, 2]:         16008
[3, 6]:         16777
[7, 14]:        18131
[15, 30]:       19188
[31, 62]:       19030
[63, 126]:      17349
[127, 254]:     13773
[255, 510]:     11436
[511, 1022]:    7060
[1023, 2046]:   3802
[2047, 4094]:   1165
[4095, 8190]:   177
[8191, 16382]:  55
```

# How many duplicate/forked projects are there?

Use heuristic of looking at the hash of the first commit.
Script: fork.py

Results
```
There are 2014 projects with 2 copies.
There are 252 projects with 3 copies.
There are 105 projects with 4 copies.
There are 65 projects with 5 copies.
There are 31 projects with 6 copies.
There are 29 projects with 7 copies.
There are 17 projects with 8 copies.
There are 13 projects with 9 copies.
There are 13 projects with 10 copies.
There are 9 projects with 11 copies.
There are 8 projects with 12 copies.
There are 4 projects with 13 copies.
There are 2 projects with 14 copies.
There are 3 projects with 15 copies.
There are 1 projects with 16 copies.
There are 3 projects with 17 copies.
There are 2 projects with 18 copies.
There are 1 projects with 19 copies.
There are 4 projects with 20 copies.
There are 4 projects with 21 copies.
There are 1 projects with 23 copies.
There are 2 projects with 24 copies.
There are 1 projects with 25 copies.
There are 1 projects with 26 copies.
There are 1 projects with 27 copies.
There are 1 projects with 28 copies.
There are 1 projects with 30 copies.
There are 1 projects with 32 copies.
There are 1 projects with 34 copies.
There are 1 projects with 36 copies.
There are 1 projects with 38 copies.
There are 1 projects with 41 copies.
There are 2 projects with 43 copies.
There are 2 projects with 45 copies.
There are 1 projects with 52 copies.
There are 1 projects with 54 copies.
There are 1 projects with 58 copies.
There are 1 projects with 65 copies.
There are 1 projects with 66 copies.
There are 1 projects with 76 copies.
There are 1 projects with 81 copies.
There are 1 projects with 99 copies.
A total of 5046/355641 projects have been marked as duplicates.
```
