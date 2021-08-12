del dist\*.* /s /q
del build\*.* /s /q
del PygameHelper.egg-info\*.* /s /q
py -3.8 setup.py sdist bdist_wheel