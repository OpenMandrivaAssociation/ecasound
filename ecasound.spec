%define	major		24
%define	cmajor	1
%define	kmajor	10
%define	libname	%mklibname %{name} %{major}
%define	libnamec	%mklibname %{name}c %{cmajor}
%define	libkvutils	%mklibname kvutils %{kmajor}
%define	develname	%mklibname %{name} -d

Summary:	Sound processing, multitrack recording, and mixing tools
Name:		ecasound
Version:	2.9.3
Release:	2
License: 	GPLv2+
Group:	Sound
Url: 		https://ecasound.seul.org
# See also: https://github.com/kaivehmanen/ecasound
Source0:	https://ecasound.seul.org/download/%{name}-%{version}.tar.gz
Source1:	ecasound16.png
Source2:	ecasound32.png
Source3:	ecasound48.png
Patch0:		ecasound-2.9.3-shared.patch
Patch1:		ecasound-2.9.3-fix-shebangs.patch
Patch2:		ecasound-2.9.3-linkage-fix.patch
Patch3:		ecasound-2.9.3-kill-rpath-in-config-scripts.patch
Patch4:		ecasound-2.9.3-fix-lv2-check.patch
Patch5:		ecasound-2.9.3-use-SIGTERM-to-avoid-messing-up-the-console.patch
Patch6:		ecasound-2.9.3-do-not-normalize-output-floating-point-data.patch
Patch7:		ecasound-2.9.3-glibc2.36.patch
#BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:	ruby
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(liblo)
BuildRequires:	pkgconfig(liboil-0.3)
BuildRequires:	pkgconfig(lilv-0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(ruby)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
Requires(post,postun): 	desktop-file-utils

#define	python_compile_opt	python2 -O -c "import compileall; compileall.compile_dir('.')"
#define	python_compile		python2 -c "import compileall; compileall.compile_dir('.')"

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
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

#-------------------------------------------------------------------------------

%package -n %{libname}
Summary:	Main shared library for Ecasound
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
%doc COPYING COPYING.GPL COPYING.LGPL
%{_libdir}/libecasound.so.%{major}*

#-------------------------------------------------------------------------------

%package -n %{libnamec}
Summary:	Shared library for Ecasound
Group:		System/Libraries
Conflicts:	%{_lib}ecasound24 < 2.9.0-5

%description -n %{libnamec}
Shared library for Ecasound.

%files -n %{libnamec}
%doc COPYING COPYING.GPL COPYING.LGPL
%{_libdir}/libecasoundc.so.%{cmajor}*

#-------------------------------------------------------------------------------

%package -n %{libkvutils}
Summary:	Shared library for Ecasound
Group:		System/Libraries
Conflicts:	%{_lib}ecasound24 < 2.9.0-5

%description -n %{libkvutils}
Shared library for Ecasound.

%files -n %{libkvutils}
%doc COPYING COPYING.GPL COPYING.LGPL
%{_libdir}/libkvutils.so.%{kmajor}*

#-------------------------------------------------------------------------------

%package -n python-%{name}
Summary:	Python bindings to %{name} control interface
Group:		Sound
Requires:	%{name} = %{version}
Requires:	python
%rename	pyecasound

%description -n python-%{name}
Python bindings to Ecasound Control Interface (ECI).

%files -n python-ecasound
%doc COPYING COPYING.GPL COPYING.LGPL
%{py_platsitedir}/*.py

#-------------------------------------------------------------------------------

%package -n ruby-%{name}
Summary:	Ruby bindings to %{name} control interface
Group:		Sound
Requires:	%{name} = %{version}
%rename		rubyecasound

%description -n ruby-%{name}
Ruby bindings to Ecasound Control Interface (ECI).

%files -n ruby-ecasound
%doc COPYING COPYING.GPL COPYING.LGPL
%{ruby_sitelibdir}/*.rb

#-------------------------------------------------------------------------------

%package -n %{develname}
Summary:	Ecasound - development files
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
%rename	%{_lib}ecasound16-devel

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

#-------------------------------------------------------------------------------

%prep
%autosetup -p1


%build
autoreconf -fiv

# Fix for lib64
perl -pi -e "s|/lib/|/%{_lib}/|g" configure*


# It was "%%{optflags} -fPIC -DPIC",
# but we already have "-fPIC" in %%{optflags}
export CFLAGS="%{optflags} -DPIC"
export CXXFLAGS="%{optflags} -DPIC  -std=c++11"
%configure \
	--enable-jack \
	--enable-liboil \
	--enable-liblilv \
	--enable-pyecasound \
	--disable-arts \
	--disable-static \
	--enable-sys-readline \
	--with-python-modules="%{_libdir}/python%{py3_ver}" \
	--enable-python-force-site-packages

%make_build


%install
%make_install ECA_S_RUBY_SITEDIR="%{ruby_sitelibdir}"

#pushd pyecasound
#python_compile_opt
#python_compile
#install *.pyc *.pyo %%{buildroot}%%{py_platsitedir}
#popd

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
Categories=X-OpenMandriva-Multimedia-Sound;
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
Categories=X-OpenMandriva-Multimedia-Sound;
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
Categories=X-OpenMandriva-Multimedia-Sound;
EOF

