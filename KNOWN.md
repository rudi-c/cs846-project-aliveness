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

# What are the most commmon .md and .txt files?

Script: common-documentation.boa

Results: Seems like only readme.md and readme.txt are there in sufficient numbers.

```
counts = readme.md, 105270.0
counts = proguard-project.txt, 21360.0
counts = readme.txt, 10506.0
counts = license.txt, 7576.0
counts = .metadata/.plugins/org.eclipse.jdt.core/savedindexnames.txt, 1589.0
counts = .metadata/.plugins/org.eclipse.jdt.core/javalikenames.txt, 1510.0
counts = dist/readme.txt, 1350.0
counts = license.md, 1055.0
counts = bin/r.txt, 1043.0
counts = todo.txt, 935.0
counts = notice.txt, 898.0
counts = test.txt, 750.0
counts = changelog.txt, 640.0
counts = public/robots.txt, 479.0
counts = android/proguard-project.txt, 478.0
counts = changes.txt, 455.0
counts = cmakelists.txt, 417.0
counts = licence.txt, 398.0
counts = changelog.md, 376.0
counts = copying.txt, 369.0
counts = notes.txt, 278.0
counts = .metadata/.plugins/org.eclipse.jdt.core/indexnamesmap.txt, 270.0
counts = install.txt, 270.0
counts = gpl.txt, 263.0
counts = copyright.txt, 262.0
counts = docs/readme.txt, 257.0
counts = manifest.txt, 257.0
counts = license-2.0.txt, 252.0
counts = bin/proguard.txt, 238.0
counts = header.txt, 232.0
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
