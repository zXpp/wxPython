#!/usr/bin/env python
#----------------------------------------------------------------------
# Name:        setup.py
# Purpose:     Distutils script for building wxPython
#
# Author:      Robin Dunn
#
# Created:     12-Oct-2000
# RCS-ID:      $Id$
# Copyright:   (c) 2000 by Total Control Software
# Licence:     wxWindows license
#----------------------------------------------------------------------

import sys, os


# The full contents of the wx.build.config module used to be located
# here in setup.py.  They were split into a separate module so it will
# be installed with wxPython and can then be used by the build scripts
# of other extension modules that wish to be wxPython compatible.
# The split is still fairly new and hasn't been tested by building
# third-party extensions yet, so expect some things to still shift
# back and forth, and also more stuff in config.py will get converted
# to functions, etc.

# This script imports it as just "config" because if wxPython doesn't
# exist yet, then it can't be imported from wx.build.config (since
# wx._core doesn't exist yet.)  So instead we keep the main copy of
# config .py in the same place as setup.py, and then copy it to
# wx/build as needed below.

# To fully support external builds, we need to have a build options
# file that is created whenever a new wxPython build is performed.
# We happen to be doing that here in this script, so make sure to
# remove the build_options.py file, so that config.py will recreate it.

for bo_name in ["build_options.py", "build_options.pyc"]:
    if os.path.exists(bo_name):
        os.remove(bo_name)

sys.setup_is_main =  __name__ == "__main__"  # an icky hack!
from config import *


#----------------------------------------------------------------------
# Update the packaged config file.
#----------------------------------------------------------------------

copy_file('config.py', 'wx/build', update=1, verbose=1)
copy_file('cfg_version.py', 'wx/build', update=1, verbose=1)
copy_file('build_options.py', 'wx/build', update=1, verbose=1)
CLEANUP.append('wx/build/config.py')
CLEANUP.append('wx/build/cfg_version.py')
CLEANUP.append('wx/build/build_options.py')

#----------------------------------------------------------------------
# Update the version file
#----------------------------------------------------------------------

# The version file is unconditionally updated every time setup.py is
# run since the version string can change based on the UNICODE flag

open('wx/__version__.py', 'w').write("""\
# This file was generated by setup.py...

VERSION_STRING  = '%(VERSION)s'
MAJOR_VERSION   = %(VER_MAJOR)s
MINOR_VERSION   = %(VER_MINOR)s
RELEASE_VERSION = %(VER_RELEASE)s
SUBREL_VERSION  = %(VER_SUBREL)s

VERSION = (MAJOR_VERSION, MINOR_VERSION, RELEASE_VERSION,
           SUBREL_VERSION, '%(VER_FLAGS)s')
""" % globals())


open('demo/version.py', 'w').write("""\
# This file was generated by setup.py...

VERSION_STRING  = '%(VERSION)s'
""" % globals())


CLEANUP.append('wx/__version__.py')
CLEANUP.append('demo/version.py')

#----------------------------------------------------------------------
# Write the SWIG version to a header file
#----------------------------------------------------------------------

if USE_SWIG:
    try:
        SVER = swig_version()
        open('include/wx/wxPython/swigver.h', 'w').write('''\
// This file was generated by setup.py

#define wxPy_SWIG_VERSION "SWIG-%s"
''' % SVER)
        msg('Using SWIG-' + SVER)
    except:
        msg('\nUnable to get SWIG version number\n')



#----------------------------------------------------------------------
# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
#----------------------------------------------------------------------

if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
    depends = {}
else:
    depends = {'depends' : depends}


#----------------------------------------------------------------------
# Define the CORE extension module
#----------------------------------------------------------------------

msg('Preparing CORE...')
swig_sources = run_swig(['core.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps +
                        [ 'src/_accel.i',
                          'src/_app.i',
                          'src/_app_ex.py',
                          'src/_constraints.i',
                          'src/_core_api.i',
                          'src/_core_ex.py',
                          'src/__core_rename.i',
                          'src/__core_reverse.txt',
                          'src/_defs.i',
                          'src/_event.i',
                          'src/_event_ex.py',
                          'src/_evtloop.i',
                          'src/_evthandler.i',
                          'src/_filesys.i',
                          'src/_gdicmn.i',
                          'src/_image.i',
                          'src/_menu.i',
                          'src/_obj.i',
                          'src/_sizers.i',
                          'src/_gbsizer.i',
                          'src/_streams.i',
                          'src/_validator.i',
                          'src/_window.i',
                          'src/_control.i',
                          'src/_swigtype.i',
                          'src/_headercol.i',
                          ],
                        True)

copy_file('src/__init__.py', PKGDIR, update=1, verbose=0)
CLEANUP.append(opj(PKGDIR, '__init__.py'))


# update the license files
mkpath('licence')
for file in ['preamble.txt', 'licence.txt', 'licendoc.txt', 'lgpl.txt']:
    copy_file(opj(WXDIR, 'docs', file), opj('licence',file), update=1, verbose=0)
    CLEANUP.append(opj('licence',file))
CLEANUP.append('licence')


if sys.platform in ['win32', 'darwin']:
    build_locale_dir(opj(PKGDIR, 'locale'))
    DATA_FILES += build_locale_list(opj(PKGDIR, 'locale'))


if os.name == 'nt':
    rc_file = ['src/wxc.rc']
else:
    rc_file = []


ext = Extension('_core_', ['src/helpers.cpp',
                           ] + rc_file + swig_sources,

                include_dirs = includes,
                define_macros = defines,

                library_dirs = libdirs,
                libraries = libs,

                extra_compile_args = cflags,
                extra_link_args = lflags,

                **depends
                )
wxpExtensions.append(ext)





# Extension for the GDI module
swig_sources = run_swig(['gdi.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps +
                        ['src/_bitmap.i',
                         'src/_colour.i',
                         'src/_dc.i',
                         'src/_graphics.i',
                         'src/_overlay.i',
                         'src/_gdiobj.i',
                         'src/_imaglist.i',
                         'src/_region.i',
                         'src/_stockobjs.i',
                         'src/_effects.i',
                         'src/_intl.i',
                         'src/_intl_ex.py',
                         'src/_brush.i',
                         'src/_cursor.i',
                         'src/_font.i',
                         'src/_icon.i',
                         'src/_pen.i',
                         'src/_palette.i',
                         'src/_renderer.i',
                         'src/_pseudodc.i',
                         ],
                        True)
ext = Extension('_gdi_', ['src/drawlist.cpp',
                          'src/pseudodc.cpp'
                          ] + swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)






# Extension for the windows module
swig_sources = run_swig(['windows.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps +
                        ['src/_panel.i',
                         'src/_toplvl.i',
                         'src/_statusbar.i',
                         'src/_splitter.i',
                         'src/_sashwin.i',
                         'src/_popupwin.i',
                         'src/_tipwin.i',
                         'src/_vscroll.i',
                         'src/_taskbar.i',
                         'src/_cmndlgs.i',
                         'src/_mdi.i',
                         'src/_pywindows.i',
                         'src/_printfw.i',
                         ],
                        True)
ext = Extension('_windows_', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)




# Extension for the controls module
swig_sources = run_swig(['controls.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps +
                        [ 'src/_toolbar.i',
                          'src/_button.i',
                          'src/_checkbox.i',
                          'src/_choice.i',
                          'src/_combobox.i',
                          'src/_gauge.i',
                          'src/_statctrls.i',
                          'src/_listbox.i',
                          'src/_textctrl.i',
                          'src/_scrolbar.i',
                          'src/_spin.i',
                          'src/_radio.i',
                          'src/_slider.i',
                          'src/_tglbtn.i',
                          'src/_notebook.i',
                          'src/_listctrl.i',
                          'src/_treectrl.i',
                          'src/_dirctrl.i',
                          'src/_pycontrol.i',
                          'src/_cshelp.i',
                          'src/_dragimg.i',
                          'src/_datectrl.i',
                          'src/_hyperlink.i',
                          'src/_picker.i',
                          'src/_collpane.i',
                          'src/_srchctrl.i',
                          'src/_axbase.i',
                          'src/_filectrl.i',
                          ],
                        True)
ext = Extension('_controls_', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)




# Extension for the misc module
swig_sources = run_swig(['misc.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps +
                        [ 'src/_settings.i',
                          'src/_functions.i',
                          'src/_misc.i',
                          'src/_tipdlg.i',
                          'src/_timer.i',
                          'src/_log.i',
                          'src/_process.i',
                          'src/_joystick.i',
                          'src/_sound.i',
                          'src/_mimetype.i',
                          'src/_artprov.i',
                          'src/_config.i',
                          'src/_datetime.i',
                          'src/_dataobj.i',
                          'src/_dnd.i',
                          'src/_display.i',
                          'src/_clipbrd.i',
                          'src/_stdpaths.i',
                          'src/_power.i',
                          'src/_about.i',
                          ],
                        True)
ext = Extension('_misc_', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)



##
## Core modules that are not in the "core" namespace start here
##

swig_sources = run_swig(['calendar.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps)
ext = Extension('_calendar', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)


swig_sources = run_swig(['combo.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps)
ext = Extension('_combo', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)


swig_sources = run_swig(['grid.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps)
ext = Extension('_grid', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)



swig_sources = run_swig(['html.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps)
ext = Extension('_html', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)


mediaLibs = libs[:]
if not MONOLITHIC and findLib('media', libdirs):
    mediaLibs += makeLibName('media')
swig_sources = run_swig(['media.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps)
ext = Extension('_media', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = mediaLibs,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)


swig_sources = run_swig(['webkit.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps)
ext = Extension('_webkit', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)



swig_sources = run_swig(['wizard.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps)
ext = Extension('_wizard', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)


swig_sources = run_swig(['dataview.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps)
ext = Extension('_dataview', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)


swig_sources = run_swig(['xrc.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args, swig_deps +
                        [ 'src/_xrc_ex.py',
                          'src/_xmlres.i',
                          'src/_xmlsub.i',
                          'src/_xml.i',
                          'src/_xmlhandler.i',
                          ])

if not MONOLITHIC and findLib('xrc', libdirs):
    xrcLib = makeLibName('xrc')
else:
    xrcLib = []
ext = Extension('_xrc',
                swig_sources,

                include_dirs =  includes + CONTRIBS_INC,
                define_macros = defines,

                library_dirs = libdirs,
                libraries = libs + xrcLib,

                extra_compile_args = cflags,
                extra_link_args = lflags,
                )
wxpExtensions.append(ext)



swig_sources = run_swig(['richtext.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force, swig_args,
                        swig_deps + [ 'src/_richtextbuffer.i',
                                      'src/_richtextctrl.i',
                                      'src/_richtexthtml.i',
                                      'src/_richtextxml.i',
                                      ])
if not MONOLITHIC and findLib('richtext', libdirs):
    richLib = makeLibName('richtext')
else:
    richLib = []
ext = Extension('_richtext', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs + richLib,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)



swig_sources = run_swig(['aui.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force,
                        swig_args + ['-I'+opj(WXDIR, 'include/wx/aui')],
                        swig_deps + ['src/_aui_docstrings.i',
                                     opj(WXDIR, 'include/wx/aui/framemanager.h'),
                                     opj(WXDIR, 'include/wx/aui/floatpane.h'),
                                     opj(WXDIR, 'include/wx/aui/dockart.h'),
                                     opj(WXDIR, 'include/wx/aui/auibook.h'),
                                     opj(WXDIR, 'include/wx/aui/tabmdi.h'),
                                     ])
if not MONOLITHIC and findLib('aui', libdirs):
    auiLib = makeLibName('aui')
else:
    auiLib = []
ext = Extension('_aui', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs + auiLib,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)


swig_sources = run_swig(['animate.i'], 'src', GENDIR, PKGDIR,
                            USE_SWIG, swig_force, swig_args, swig_deps)
ext = Extension('_animate',
                swig_sources,

                include_dirs =  includes + CONTRIBS_INC,
                define_macros = defines,

                library_dirs = libdirs,
                libraries = libs,

                extra_compile_args = cflags,
                extra_link_args = lflags,
                )

wxpExtensions.append(ext)


swig_sources = run_swig(['propgrid.i'], 'src', GENDIR, PKGDIR,
                        USE_SWIG, swig_force,
                        swig_args + ['-I'+opj(WXDIR, 'include/wx/propgrid')],
                        swig_deps + [#'src/_propgrid_docstrings.i',
                                     opj(WXDIR, 'include/wx/propgrid/advprops.h'),
                                     opj(WXDIR, 'include/wx/propgrid/editors.h'),
                                     opj(WXDIR, 'include/wx/propgrid/manager.h'),
                                     opj(WXDIR, 'include/wx/propgrid/property.h'),
                                     opj(WXDIR, 'include/wx/propgrid/propgrid.h'),
                                     opj(WXDIR, 'include/wx/propgrid/propgriddefs.h'),
                                     opj(WXDIR, 'include/wx/propgrid/propgridiface.h'),
                                     opj(WXDIR, 'include/wx/propgrid/propgridpagestate.h'),
                                     opj(WXDIR, 'include/wx/propgrid/props.h'),
                                     ])
if not MONOLITHIC and findLib('propgrid', libdirs):
    propgridLib = makeLibName('propgrid')
else:
    propgridLib = []
ext = Extension('_propgrid', swig_sources,
                include_dirs =  includes,
                define_macros = defines,
                library_dirs = libdirs,
                libraries = libs + propgridLib,
                extra_compile_args = cflags,
                extra_link_args = lflags,
                **depends
                )
wxpExtensions.append(ext)


if BUILD_STC:
    msg('Preparing STC...')
    STC_H = opj(WXDIR, 'include/wx/stc')

    swig_sources = run_swig(['stc.i'], 'src', GENDIR, PKGDIR,
                            USE_SWIG, swig_force, swig_args + ['-I'+STC_H],
                            [opj(STC_H, 'stc.h'),
                             opj("src/_stc_utf8_methods.py"),
                             opj("src/_stc_docstrings.i"),
                             opj("src/_stc_gendocs.i"),
                             ] + swig_deps)

    stcLibs = libs[:]
    if not MONOLITHIC and findLib('stc', libdirs):
        stcLibs += makeLibName('stc')

    ext = Extension('_stc',
                    swig_sources,
                    include_dirs = includes + CONTRIBS_INC,
                    define_macros = defines,
                    library_dirs = libdirs,
                    libraries = stcLibs,
                    extra_compile_args = cflags,
                    extra_link_args = lflags,
                    )

    wxpExtensions.append(ext)


if BUILD_GLCANVAS:
    msg('Preparing GLCANVAS...')
    swig_sources = run_swig(['glcanvas.i'], 'src', GENDIR, PKGDIR,
                            USE_SWIG, swig_force, swig_args, swig_deps)
    gl_libs = []
    gl_libdirs = libdirs[:]
    if os.name == 'posix':
        gl_config = os.popen(WX_CONFIG + ' --libs', 'r').read()[:-1] + \
                    os.popen(WX_CONFIG + ' --libs gl', 'r').read()[:-1]
        gl_lflags = gl_config.split()
        gl_lflags = adjustLFLAGS(gl_lflags, gl_libdirs, gl_libs)
    else:
        gl_libs = libs + ['opengl32', 'glu32'] + makeLibName('gl')
        gl_lflags = lflags

    if sys.platform[:6] == "darwin" and WXPORT == 'osx_carbon':
        if not ARCH == "":
            gl_lflags.append("-arch")
            gl_lflags.append(ARCH)

    ext = Extension('_glcanvas',
                    swig_sources,
                    include_dirs = includes + CONTRIBS_INC,
                    define_macros = defines,
                    library_dirs = gl_libdirs,
                    libraries = gl_libs,
                    extra_compile_args = cflags,
                    extra_link_args = gl_lflags,
                    )

    wxpExtensions.append(ext)



#----------------------------------------------------------------------
# Define the ACTIVEX extension module (experimental)
#----------------------------------------------------------------------

if BUILD_ACTIVEX:
    msg('Preparing ACTIVEX...')
    location = 'contrib/activex'
    axloc = opj(location, "wxie")

    swig_files = ['activex.i', ]

    swig_sources = run_swig(swig_files, location, '', PKGDIR,
                            USE_SWIG, swig_force, swig_args, swig_deps +
                            [ '%s/_activex_ex.py' % location])


    ext = Extension('_activex', ['%s/IEHtmlWin.cpp' % axloc,
                                 '%s/wxactivex.cpp' % axloc,
                                 ] + swig_sources,

                    include_dirs =  includes + [ axloc ],
                    define_macros = defines,

                    library_dirs = libdirs,
                    libraries = libs,

                    extra_compile_args = cflags,
                    extra_link_args = lflags,
                    )

    wxpExtensions.append(ext)


#----------------------------------------------------------------------
# Define the GIZMOS  extension module
#----------------------------------------------------------------------

if BUILD_GIZMOS:
    msg('Preparing GIZMOS...')
    location = 'contrib/gizmos'

    swig_sources = run_swig(['gizmos.i'], location, GENDIR, PKGDIR,
                            USE_SWIG, swig_force, swig_args, swig_deps +
                            [ '%s/_treelist.i' % location])

    ext = Extension('_gizmos',
                    [ '%s/treelistctrl.cpp'        % opj(location, 'wxCode/src'),
                      '%s/gizmos/dynamicsash.cpp'  % opj(location, 'wxCode/src'),
                      #'%s/gizmos/editlbox.cpp'     % opj(location, 'wxCode/src'),
                      '%s/gizmos/ledctrl.cpp'      % opj(location, 'wxCode/src'),
                      '%s/gizmos/splittree.cpp'    % opj(location, 'wxCode/src'),
                      '%s/gizmos/statpict.cpp'     % opj(location, 'wxCode/src'),
                      ] + swig_sources,

                    include_dirs =  includes + [ location, opj(location, 'wxCode/include') ] + CONTRIBS_INC,
                    define_macros = defines,

                    library_dirs = libdirs,
                    libraries = libs,

                    extra_compile_args = cflags,
                    extra_link_args = lflags,
                    )

    wxpExtensions.append(ext)


#----------------------------------------------------------------------
# Define the DLLWIDGET  extension module
#----------------------------------------------------------------------

if BUILD_DLLWIDGET:
    msg('Preparing DLLWIDGET...')
    location = 'contrib/dllwidget'
    swig_files = ['dllwidget_.i']

    swig_sources = run_swig(swig_files, location, '', PKGDIR,
                            USE_SWIG, swig_force, swig_args, swig_deps)

    # copy a contrib project specific py module to the main package dir
    copy_file(opj(location, 'dllwidget.py'), PKGDIR, update=1, verbose=0)
    CLEANUP.append(opj(PKGDIR, 'dllwidget.py'))

    ext = Extension('dllwidget_c', [
                                '%s/dllwidget.cpp' % location,
                             ] + swig_sources,

                    include_dirs =  includes + CONTRIBS_INC,
                    define_macros = defines,

                    library_dirs = libdirs,
                    libraries = libs,

                    extra_compile_args = cflags,
                    extra_link_args = lflags,
                    )

    wxpExtensions.append(ext)



#----------------------------------------------------------------------

if EGGing:
    # Replace the make_zipfile function used by the bdist_egg command
    # so we can do some postprocessing of what will become the content
    # of the egg file before it is made.
    
    import setuptools.command.bdist_egg
    old_make_zipfile = setuptools.command.bdist_egg.make_zipfile

    def my_make_zipfile(zip_filename, base_dir, *args, **kw):
        if sys.platform == 'darwin':
            # copy wx dylibs into the egg, and set the @loader_path in
            # the wxPython .so's to find our copies.
                   
            # find all wx dylibs used by the wxPython .so files, use a
            # set to collapse the duplicates.
            dylibs = set()
            soFiles = glob.glob(opj(base_dir, 'wx', '*.so'))
            for f in soFiles:
                info = os.popen('otool -L %s | grep libwx | grep -v loader_path' % f).read().strip()
                for line in info.split('\n'):
                    if not line: continue
                    so = line.split()[0]
                    dylibs.add(so)
                    cmd = ['install_name_tool',
                           '-change',
                           so,
                           '@loader_path/../Library/%s' % os.path.basename(so),
                           f ]
                    spawn(cmd)

            # Copy the shared library files into the egg, and fix up
            # dependency paths where needed.
            dest = opj(base_dir, 'Library')
            if not os.path.exists(dest):
                os.mkdir(dest)
            for f in dylibs:
                copy_file(f, dest)
                info = os.popen('otool -L %s | grep libwx | grep -v ":$" | grep -v loader_path' % f).read().strip()
                for line in info.split('\n'):
                    if not line: continue

                    so = line.split()[0]
                    cmd = ['install_name_tool',
                           '-change',
                           so,
                           '@loader_path/../Library/%s' % os.path.basename(so),
                           '%s/%s' % (dest, os.path.basename(f)) ]
                    spawn(cmd)
                
        
        if os.name == 'nt':
            # copy the wx DLLs and others into the wx package dir
            # inside the egg.
            dllFiles = glob.glob(opj(WXDIR, 'lib', 'vc_dll',
                                     'wxmsw%s%s_*.dll' % (WXDLLVER, libFlag()))) + \
                       glob.glob(opj(WXDIR, 'lib', 'vc_dll',
                                     'wxbase%s%s_*.dll' % (WXDLLVER, libFlag()))) + \
                       [ 'distrib/msw/gdiplus.dll',
                         'distrib/msw/msvcp71.dll' ]
            for f in dllFiles:
                copy_file(f, opj(base_dir, 'wx'))
                        
        return old_make_zipfile(zip_filename, base_dir, *args, **kw)

    setuptools.command.bdist_egg.make_zipfile = my_make_zipfile


#----------------------------------------------------------------------
# Tools, scripts, data files, etc.
#----------------------------------------------------------------------


WX_PKGLIST =      [ 'wx',
                    'wx.build',
                    'wx.lib',
                    'wx.lib.agw',
                    'wx.lib.agw.aui',
                    'wx.lib.agw.ribbon',
                    'wx.lib.analogclock',
                    'wx.lib.analogclock.lib_setup',
                    'wx.lib.art',
                    'wx.lib.colourchooser',
                    'wx.lib.editor',
                    'wx.lib.floatcanvas',
                    'wx.lib.floatcanvas.Utilities',
                    'wx.lib.masked',
                    'wx.lib.mixins',
                    'wx.lib.ogl',
                    'wx.py',
                    'wx.tools',
                    'wx.tools.XRCed',
                    'wx.tools.XRCed.plugins',
                    'wx.tools.Editra',
                    'wx.tools.Editra.src',
                    'wx.tools.Editra.src.autocomp',
                    'wx.tools.Editra.src.eclib',
                    'wx.tools.Editra.src.ebmlib',
                    'wx.tools.Editra.src.extern',
                    'wx.tools.Editra.src.syntax',
                    ]


if NO_SCRIPTS or EGGing:
    SCRIPTS = None
else:
    SCRIPTS = [opj('scripts/helpviewer'),
               opj('scripts/img2png'),
               opj('scripts/img2py'),
               opj('scripts/img2xpm'),
               opj('scripts/pyalacarte'),
               opj('scripts/pyalamode'),
               opj('scripts/pycrust'),
               opj('scripts/pyshell'),
               opj('scripts/pywrap'),
               opj('scripts/pywxrc'),
               opj('scripts/xrced'),
               opj('scripts/editra'),
               ]
    if os.name == 'nt':
        SCRIPTS.append( opj('scripts/genaxmodule') ) 



DATA_FILES += find_data_files('wx/lib/editor', '*.txt')
DATA_FILES += find_data_files('wx/py', '*.txt', '*.ico', '*.css', '*.html')

DATA_FILES += find_data_files('wx/tools/XRCed', '*.txt', '*.xrc', '*.htb')
DATA_FILES += find_data_files('wx/tools/XRCed/plugins', '*.crx')
DATA_FILES += find_data_files('wx/tools/XRCed/plugins/bitmaps', '*.png')

DATA_FILES += find_data_files('wx/tools/Editra/docs', '*.txt')
DATA_FILES += find_data_files('wx/tools/Editra/locale', '*.mo')
DATA_FILES += find_data_files('wx/tools/Editra/pixmaps',
                              '*.png', '*.icns', '*.ico', 'README', 'AUTHORS', 'COPYING')
DATA_FILES += find_data_files('wx/tools/Editra/plugins', '*.egg')
DATA_FILES += find_data_files('wx/tools/Editra/src', 'README')
DATA_FILES += find_data_files('wx/tools/Editra/styles', '*.ess')
DATA_FILES += find_data_files('wx/tools/Editra/tests/syntax', '*')
DATA_FILES += find_data_files('wx/tools/Editra', '[A-Z]*', recursive=False)


## import pprint
## pprint.pprint(DATA_FILES)
## sys.exit()


if NO_HEADERS or EGGing:
    HEADERS = None
else:
    h_files = glob.glob(opj("include/wx/wxPython/*.h"))
    i_files = glob.glob(opj("src/*.i"))   + \
              glob.glob(opj("src/_*.py")) + \
              glob.glob(opj("src/*.swg"))
    if BUILD_GLCANVAS:
        i_files += glob.glob(opj("contrib/glcanvas/*.i"))

    HEADERS = zip(h_files, ["/wxPython"]*len(h_files)) + \
              zip(i_files, ["/wxPython/i_files"]*len(i_files))


if INSTALL_MULTIVERSION:
    EXTRA_PATH = getExtraPath(addOpts=EP_ADD_OPTS, shortVer=not EP_FULL_VER)
    open("src/wx.pth", "w").write(EXTRA_PATH + "\n")
    CLEANUP.append("src/wx.pth")
else:
    EXTRA_PATH = None


BUILD_OPTIONS = { 'build_base' : BUILD_BASE }
if WXPORT == 'msw':
    BUILD_OPTIONS[ 'compiler' ] = COMPILER


other_kw = {}
if EGGing:
    # These args are only used with setuptools, which for now is only
    # when we are building an egg.
    other_kw = dict(
        zip_safe = False,
        entry_points = {
            'console_scripts' : [ 'img2png = wx.tools.img2png:main',
                                  'img2xpm = wx.tools.img2xpm:main',
                                  'img2py = wx.tools.img2py:main',
                                  'pywxrc = wx.tools.pywxrc:main',
                                  ], 
            'gui_scripts'     : [ 'pycrust = wx.py.PyCrust:main',
                                  'pyshell = wx.py.PyShell:main',
                                  'pywrap = wx.py.PyWrap:main',
                                  'helpviewer = wx.tools.helpviewer:main',
                                  'editra = wx.tools.Editra.launcher:main',
                                  'xrced = wx.tools.XRCed.xrced:main',
                                  ], 
            },
        )
    
    if os.name == 'nt':
        other_kw['entry_points']['console_scripts'].append(
            'genaxmodule = wx.tools.genaxmodule:main')

#----------------------------------------------------------------------
# Do the Setup/Build/Install/Whatever
#----------------------------------------------------------------------

if __name__ == "__main__":
    if not PREP_ONLY:

        if not EGGing:
            if INSTALL_MULTIVERSION:
                setup(name             = 'wxPython-common',
                      version          = VERSION,
                      description      = DESCRIPTION,
                      long_description = LONG_DESCRIPTION,
                      author           = AUTHOR,
                      author_email     = AUTHOR_EMAIL,
                      url              = URL,
                      download_url     = DOWNLOAD_URL,
                      license          = LICENSE,
                      platforms        = PLATFORMS,
                      classifiers      = filter(None, CLASSIFIERS.split("\n")),
                      keywords         = KEYWORDS,

                      package_dir = { '': 'wxversion' },
                      py_modules = ['wxversion'],

                      data_files = [('', ['src/wx.pth'])],

                      options = { 'build' : BUILD_OPTIONS,
                                  },

                      cmdclass = { 'install_data':    wx_smart_install_data,
                                   },
                      )

        setup(name             = 'wxPython',
              version          = VERSION,
              description      = DESCRIPTION,
              long_description = LONG_DESCRIPTION,
              author           = AUTHOR,
              author_email     = AUTHOR_EMAIL,
              url              = URL,
              download_url     = DOWNLOAD_URL,
              license          = LICENSE,
              platforms        = PLATFORMS,
              classifiers      = filter(None, CLASSIFIERS.split("\n")),
              keywords         = KEYWORDS,

              packages         = WX_PKGLIST,
              extra_path       = EXTRA_PATH,
              ext_package      = PKGDIR,
              ext_modules      = wxpExtensions,
              

              options          = { 'build' : BUILD_OPTIONS,  },

              scripts          = SCRIPTS,
              data_files       = DATA_FILES,
              headers          = HEADERS,

              # Override some of the default distutils command classes with my own
              cmdclass = { 'install' :        wx_install,
                           'install_data':    wx_smart_install_data,
                           'install_headers': wx_install_headers,
                           'clean':           wx_extra_clean,
                           },

              **other_kw
              )



#----------------------------------------------------------------------
#----------------------------------------------------------------------
