%define	major		24
%define	libname		%mklibname %{name} %{major}
%define	develname	%mklibname %{name} -d

Summary:	Sound processing, multitrack recording, and mixing tools
Name:		ecasound
Version:	2.9.0
Release:	2
License: 	GPLv2+
Group:		Sound
URL: 		http://www.eca.cx/ecasound/
Source0:	http://ecasound.seul.org/download/%{name}-%{version}.tar.gz
Source1:	%{name}16.png
Source2:	%{name}32.png
Source3:	%{name}48.png
Patch0:		%{name}-2.7.0-shared.diff
Patch1:		%{name}-shellbang_fix.patch
Patch2:		%{name}-linkage_fix.diff
Patch3:		%{name}-2.6.0-link-pyecasound.patch
Requires(post,postun): 	desktop-file-utils
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(alsa) >= 0.9.0
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile) >= 1.0.0
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig(python)
BuildRequires:	readline-devel
BuildRequires:	oil-devel >= 0.3
BuildRequires:	pkgconfig(liblo)
BuildRequires:	pkgconfig(lilv-0)
BuildRequires:	ruby
BuildRequires:	ruby-devel
BuildRequires:	multiarch-utils >= 1.0.3

%define	python_compile_opt	python -O -c "import compileall; compileall.compile_dir('.')"
%define	python_compile		python -c "import compileall; compileall.compile_dir('.')"

%description
Ecasound is a software package designed for multitrack audio processing.
It can be used for simple tasks like audio playback, recording and format
conversions, as well as for multitrack effect processing, mixing, recording
and signal recycling. Ecasound supports a wide range of audio inputs, outputs
and effect algorithms. Effects and audio objects can be combined in various
ways, and their parameters can be controlled by operator objects like
oscillators and MIDI-CCs. A versatile console mode user-interface is included
in the package.

%files
%doc NEWS COPYING COPYING.GPL COPYING.LGPL README BUGS TODO examples
%doc Documentation/*.html
%{_bindir}/eca*
#%%config(noreplace) %%{_sysconfdir}/ecasound/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop

#-------------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared libraries for Ecasound
Group:		System/Libraries

%description -n %{libname}
Ecasound is a software package designed for multitrack audio processing.
It can be used for simple tasks like audio playback, recording and format
conversions, as well as for multitrack effect processing, mixing, recording
and signal recycling. Ecasound supports a wide range of audio inputs, outputs
and effect algorithms. Effects and audio objects can be combined in various
ways, and their parameters can be controlled by operator objects like
oscillators and MIDI-CCs. A versatile console mode user-interface is included
in the package. This package contains the shared Ecasound libraries.

%files -n %{libname}
%{_libdir}/libecasound.so.%{major}*
%{_libdir}/libecasoundc.so.*
%{_libdir}/libkvutils.so.*

#-------------------------------------------------------------------------------

%package -n python-%{name}
Summary:	Python bindings to %{name} control interface
Group:		Sound
Requires:	%{name} = %{version}
%rename		pyecasound

%description -n python-%{name}
Python bindings to Ecasound Control Interface (ECI).

%files -n python-ecasound
#{py_platsitedir}/*.so
%{py_platsitedir}/*.py
%{py_platsitedir}/*.pyc
%{py_platsitedir}/*.pyo

#-------------------------------------------------------------------------------

%package -n ruby-%{name}
Summary:	Ruby bindings to %{name} control interface
Group:		Sound
Requires:	%{name} = %{version}
%rename		rubyecasound

%description -n ruby-%{name}
Ruby bindings to Ecasound Control Interface (ECI).

%files -n ruby-ecasound
%{ruby_sitelibdir}/*.rb

#-------------------------------------------------------------------------------

%package -n %{develname}
Summary:	Ecasound - development files
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
%rename		%{_lib}ecasound16-devel

%description -n	%{develname}
The %{name}-devel package contains the files necessary for building apps like
ecawave and ecamegapedal that directly link against %{name} libraries.

%files -n %{develname}
%{_bindir}/libecasound-config
%{_bindir}/libecasoundc-config
%{_includedir}/kvutils/*.h
%{_includedir}/libecasound/*.h
%{_includedir}/libecasoundc/*.h
%{_libdir}/*.so
%{_libdir}/*.a

#-------------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p0
%patch3 -p1

# lib64 fix
perl -pi -e "s|/lib/|/%{_lib}/|g" configure*


%build
autoreconf -fiv
# It was "%%{optflags} -fPIC -DPIC",
# but we already have "-fPIC" in %%{optflags}
export CFLAGS="%{optflags} -DPIC"
export CXXFLAGS="%{optflags} -DPIC"

%configure2_5x \
    --enable-liboil \
    --enable-pyecasound \
    --disable-dependency-tracking \
    --disable-liblilv \
    --enable-sys-readline

%make

# (eandry) the tests dies at "pyecasound" on bs submit,
# but build fine with mdvsys build, so disabling for submission
#%%check
#%%make check


%install
install -d %{buildroot}%{py_platsitedir}
%makeinstall_std

pushd pyecasound
%python_compile_opt
%python_compile
install *.pyc *.pyo %{buildroot}%{py_platsitedir}
popd

# Icons
install -m644 %{SOURCE1} -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 %{SOURCE2} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE3} -D %{buildroot}%{_liconsdir}/%{name}.png

# Menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Name[ru]=%{name}
Comment=%{Summary}
Comment[ru]=Ð˜Ð½ÑÑ‚Ñ€ÑƒÐ¼ÐµÐ½Ñ‚Ñ‹ Ð¾Ð±Ñ€Ð°Ð±Ð¾Ñ‚ÐºÐ¸ Ð·Ð²ÑƒÐºÐ°, Ð¼Ð¸ÐºÑˆÐ¸Ñ€Ð¾Ð²Ð°Ð½Ð¸Ñ Ð¸ Ð·Ð°Ð¿Ð¸ÑÐ¸
Exec=%{name} -c
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Sound;
EOF

cat > %{buildroot}%{_datadir}/applications/ecamonitor.desktop << EOF
[Desktop Entry]
Name=%{name}
Name[ru]=%{name}
Comment=%{Summary}
Comment[ru]=Ð˜Ð½ÑÑ‚Ñ€ÑƒÐ¼ÐµÐ½Ñ‚Ñ‹ Ð¾Ð±Ñ€Ð°Ð±Ð¾Ñ‚ÐºÐ¸ Ð·Ð²ÑƒÐºÐ°, Ð¼Ð¸ÐºÑˆÐ¸Ñ€Ð¾Ð²Ð°Ð½Ð¸Ñ Ð¸ Ð·Ð°Ð¿Ð¸ÑÐ¸
Exec=ecamonitor
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Sound;
EOF

cat > %{buildroot}%{_datadir}/applications/ecasignalview.desktop << EOF
[Desktop Entry]
Name=%{name}
Name[ru]=%{name}
Comment=%{Summary}
Comment[ru]=Ð˜Ð½ÑÑ‚Ñ€ÑƒÐ¼ÐµÐ½Ñ‚Ñ‹ Ð¾Ð±Ñ€Ð°Ð±Ð¾Ñ‚ÐºÐ¸ Ð·Ð²ÑƒÐºÐ°, Ð¼Ð¸ÐºÑˆÐ¸Ñ€Ð¾Ð²Ð°Ð½Ð¸Ñ Ð¸ Ð·Ð°Ð¿Ð¸ÑÐ¸
Exec=ecasignalview
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Sound;
EOF

# Installer wrongly put the ecasound.rb file in /usr/lib/ruby/1.9.1/site_ruby/1.9/
# the right one is %%{ruby_sitelibdir}= /usr/lib/ruby/1.9.1/site_ruby/1.9.1/:
# rename it accordingly
mv %{buildroot}/usr/lib/ruby/1.9.1/site_ruby/1.9/ %{buildroot}%{ruby_sitelibdir}


%changelog
* Sat May 04 2013 Giovanni Mariani <mc2374@mclink.it> 2.9.0-1
- New release 2.9.0
- Rediffed P1
- Added BReq for lilv-devel
- Dropped support for aRTs (we have it no more) and for liblilv
  (to avoid build failure with our library)

* Fri Nov 02 2012 Giovanni Mariani <mc2374@mclink.it> 2.7.2-3
- Dropped BuildRoot, useless %%defines, %%mkrel, %%defattr and
  %%clean section
- Fixed BReq for libsndfile and liboil devel package
- Removed .la files
- Removed deprecated %%multiarch macros
- Fixed wrong placement for ruby files
- Fixed file lists

* Fri Nov 19 2010 Funda Wang <fwang@mandriva.org> 2.7.2-2mdv2011.0
+ Revision: 598991
- rebuild for py2.7

* Wed Sep 01 2010 Emmanuel Andry <eandry@mandriva.org> 2.7.2-1mdv2011.0
+ Revision: 575120
- New version 2.7.2

* Mon Mar 01 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.7.1-2mdv2010.1
+ Revision: 512889
- rebuild for new libjack

* Mon Feb 22 2010 Frederik Himpe <fhimpe@mandriva.org> 2.7.1-1mdv2010.1
+ Revision: 509625
- update to new version 2.7.1

* Wed Jan 27 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.7.0-2mdv2010.1
+ Revision: 497124
- rebuild

* Thu Dec 31 2009 Emmanuel Andry <eandry@mandriva.org> 2.7.0-1mdv2010.1
+ Revision: 484471
- disable make check, OK on cluster but fails when submitted
- fix pyecasound build
- rediff p0
- BR liboil-devel and liblo-devel
- fix configure options
- New version 2.6.0
- fix license
- use autoreconf
- disable arts support
- update file list

  + JÃ©rÃ´me Brenier <incubusss@mandriva.org>
    - update to new version 2.7.0
    - rediff P0

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - rebuild for latest readline

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Frederik Himpe <fhimpe@mandriva.org>
    - Fix underlinkingin pyecasound

* Sat Jan 03 2009 Funda Wang <fwang@mandriva.org> 2.5.2-2mdv2009.1
+ Revision: 323631
- rebuild

* Sun Aug 24 2008 Oden Eriksson <oeriksson@mandriva.com> 2.5.2-1mdv2009.0
+ Revision: 275506
- 2.5.2

* Thu Aug 21 2008 Oden Eriksson <oeriksson@mandriva.com> 2.5.1-1mdv2009.0
+ Revision: 274661
- 2.5.1
- new major again (20)

* Sun Aug 17 2008 Oden Eriksson <oeriksson@mandriva.com> 2.5.0-1mdv2009.0
+ Revision: 272891
- 2.5.0
- drop the gcc43 patch, it's fixed with this version
- fix shellbang

* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 2.4.6.1-2mdv2009.0
+ Revision: 232974
- added gcc43 and linkage fixes
- fix devel package naming

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Sep 02 2007 Emmanuel Andry <eandry@mandriva.org> 2.4.6.1-1mdv2008.0
+ Revision: 78215
- drop old menu
- drop old distro conditionnal
- New version
- rediff patch0
- fix icons


* Sun Feb 18 2007 Emmanuel Andry <eandry@mandriva.org> 2.4.5-1mdv2007.0
+ Revision: 122210
- New version 2.4.5
- disable check (python tests fail)

  + Oden Eriksson <oeriksson@mandriva.com>
    - drop ruby macros, the bs can't cope with that
    - rebuild

  + Lenny Cartier <lenny@mandriva.com>
    - Rebuild for dependencies

  + Nicolas LÃ©cureuil <neoclust@mandriva.org>
    - Rebuild against new python
    - Import ecasound

* Fri Aug 04 2006 Oden Eriksson <oeriksson@mandriva.com> 2.4.4-4mdv2007.0
- fix deps

* Mon Jul 31 2006 Oden Eriksson <oeriksson@mandriva.com> 2.4.4-3mdv2007.0
- fix #19020
- fix xdg menu

* Sun Mar 05 2006 Michael Scherer <misc@mandriva.org> 2.4.4-2mdk
- use new python macro
- provides/obsoletes ruby package, fix #19021 
- uncomment make check

* Sat Jan 28 2006 Austin Acton <austin@mandriva.org> 2.4.4-1mdk
- New release 2.4.4
- major 16

* Thu Nov 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.4.2-2mdk
- fixed the ruby lib dir after peeking at the eruby spec 
  file... should fix x86_64 build..., duh!

* Thu Aug 18 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.4.2-1mdk
- New release 2.4.2

* Sun Jun 19 2005 Oden Eriksson <oeriksson@mandriva.com> 2.4.1-1mdk
- 2.4.1
- fix deps
- drop obsolete patches

* Sat Apr 02 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.4.0-1mdk
- 2.4.0
- added missing code (P0)
- make it compile on amd64
- make shared libraries
- use the %%mkrel macro
- fix python-naming-policy-not-applied rpmlint error
- fix possible future ruby-naming-policy-not-applied rpmlint error

* Mon Jan 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.3.5-2mdk
- fix deps and conditional %%multiarch

* Thu Nov 11 2004 Austin Acton <austin@mandrake.org> 2.3.5-1mdk
- 2.3.5

* Sat Oct 30 2004 Austin Acton <austin@mandrake.org> 2.3.4-1mdk
- 2.3.4
- source URL

* Wed Jun 09 2004 Austin Acton <austin@mandrake.org> 2.3.3-2mdk
- buildrequires ruby

* Wed May 05 2004 Austin Acton <austin@mandrake.org> 2.3.3-1mdk
- 2.3.3
- delib buildrequires
- configure 2.5

