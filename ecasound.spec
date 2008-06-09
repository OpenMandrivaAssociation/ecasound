%define major 16
%define libname %mklibname %{name} %{major}

%define	Summary	Sound processing, multitrack recording, and mixing tools

Summary:	%{Summary}
Name:		ecasound
Version: 	2.4.6.1
Release: 	%mkrel 1
License: 	GPL
Group: 		Sound
URL: 		http://www.eca.cx/ecasound/
Source0: 	http://ecasound.seul.org/download/%{name}-%{version}.tar.bz2
Source1:        %{name}16.png
Source2:        %{name}32.png
Source3:        %{name}48.png
Patch0:		ecasound-2.4.6.1-shared.diff
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
BuildRequires:  autoconf
BuildRequires:	arts-devel
BuildRequires:	jackit-devel
BuildRequires:	libalsa-devel
BuildRequires:	libaudiofile-devel
BuildRequires:	libsndfile-devel
BuildRequires:	ncurses-devel
BuildRequires:	python-devel
BuildRequires:	ruby
BuildRequires:	ruby-devel
BuildRequires:	readline-devel
BuildRequires:	multiarch-utils >= 1.0.3
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot

%define python_compile_opt python -O -c "import compileall; compileall.compile_dir('.')"
%define python_compile     python -c "import compileall; compileall.compile_dir('.')"

%description
Ecasound is a software package designed for multitrack
audio processing. It can be used for simple tasks like
audio playback, recording and format conversions, as
well as for multitrack effect processing, mixing,
recording and signal recycling. Ecasound supports a
wide range of audio inputs, outputs and effect
algorithms. Effects and audio objects can be combined
in various ways, and their parameters can be
controlled by operator objects like oscillators and
MIDI-CCs. A versatile console mode user-interface is
included in the package.

%package -n	%{libname}
Summary: 	Shared libraries for Ecasound
Group: 		System/Libraries

%description -n	%{libname}
Ecasound is a software package designed for multitrack
audio processing. It can be used for simple tasks like
audio playback, recording and format conversions, as
well as for multitrack effect processing, mixing,
recording and signal recycling. Ecasound supports a
wide range of audio inputs, outputs and effect
algorithms. Effects and audio objects can be combined
in various ways, and their parameters can be
controlled by operator objects like oscillators and
MIDI-CCs. A versatile console mode user-interface is
included in the package.

This package contains the shared Ecasound libraries.

%package -n	python-ecasound
Summary: 	Python bindings to ecasound control interface
Group: 		Sound
Requires: 	ecasound
Obsoletes:      pyecasound
Provides:       pyecasound

%description -n	python-ecasound
Python bindings to Ecasound Control Interface (ECI).

%package -n	ruby-ecasound
Summary:        Ruby bindings to ecasound control interface
Group:          Sound
Requires:       ecasound
Obsoletes:      rubyecasound
Provides:       rubyecasound

%description -n	ruby-ecasound
Ruby bindings to Ecasound Control Interface (ECI).

%package -n	%{libname}-devel
Summary: 	Ecasound - development files
Group: 		Development/Other
Provides:	lib%{name}-devel %{name}-devel
Requires:	%{libname} = %{version}
Obsoletes:	libecasound-devel

%description -n	%{libname}-devel
The ecasound-devel package contains the header files and static
libraries necessary for building apps like ecawave and
ecamegapedal that directly link against ecasound libraries.

%prep

%setup -q
%patch0 -p1

# lib64 fix
perl -pi -e "s|/lib/|/%{_lib}/|g" configure*

%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force && aclocal && autoconf && automake --foreign --add-missing

export CFLAGS="%{optflags} -fPIC -DPIC"
export CXXFLAGS="%{optflags} -fPIC -DPIC"

%configure2_5x \
    --enable-shared \
    --with-largefile \
    --enable-sys-readline

%make

# (oe) the tests dies at "ECA_TEST_REPOSITORY" on cooker as 
# of Fri Apr 01 2005 but works on 10.1 x86_64
#%check
#make check

%install
rm -fr %{buildroot}

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
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{Summary}
Exec=%{name} -c
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Sound;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-ecamonitor.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{Summary}
Exec=ecamonitor
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Sound;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-ecasignalview.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{Summary}
Exec=ecasignalview
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Multimedia-Sound;
EOF


%multiarch_binaries %{buildroot}%{_bindir}/libecasound-config
%multiarch_binaries %{buildroot}%{_bindir}/libecasoundc-config

%post
%update_menus
%update_desktop_database

%postun
%clean_menus
%clean_desktop_database

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/*.so.*

%files
%defattr(-,root,root)
%doc NEWS COPYING COPYING.GPL COPYING.LGPL README BUGS TODO examples
%doc Documentation/*.html Documentation/*.txt
%{_bindir}/eca*
#%config(noreplace) %{_sysconfdir}/ecasound/*
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop

%files -n python-ecasound
%defattr(-,root,root)
%{py_platsitedir}/*.so
%{py_platsitedir}/*.py
%{py_platsitedir}/*.pyc
%{py_platsitedir}/*.pyo

%files -n ruby-ecasound
%defattr(-,root,root)
/usr/lib/ruby/site_ruby/1.8/*.rb

%files -n %{libname}-devel
%defattr(-, root, root)
%multiarch %{multiarch_bindir}/libecasound-config
%multiarch %{multiarch_bindir}/libecasoundc-config
%{_bindir}/libecasound-config
%{_bindir}/libecasoundc-config
%{_includedir}/kvutils/*.h
%{_includedir}/libecasound/*.h
%{_includedir}/libecasoundc/*.h
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/*.a


