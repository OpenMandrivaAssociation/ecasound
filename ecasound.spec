%define	major		24
%define	libname		%mklibname %{name} %{major}
%define	develname	%mklibname %{name} -d

Summary:	Sound processing, multitrack recording, and mixing tools
Name:		ecasound
Version:	2.9.3
Release:	1
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
BuildRequires:	pkgconfig(python2)
BuildRequires:	readline-devel
BuildRequires:	oil-devel >= 0.3
BuildRequires:	pkgconfig(liblo)
BuildRequires:	pkgconfig(lilv-0)
BuildRequires:	ruby
BuildRequires:	ruby-devel
#BuildRequires:	multiarch-utils >= 1.0.3

%define	python_compile_opt	python2 -O -c "import compileall; compileall.compile_dir('.')"
%define	python_compile		python2 -c "import compileall; compileall.compile_dir('.')"

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
Requires:	python2
%rename		pyecasound

%description -n python-%{name}
Python bindings to Ecasound Control Interface (ECI).

%files -n python-ecasound
%{py2_platsitedir}/*.py
%{py2_platsitedir}/*.pyc
%{py2_platsitedir}/*.pyo

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
ln -s %{_bindir}/python2 python
export PATH=`pwd`:$PATH

%configure \
    --enable-liboil \
    --enable-pyecasound \
    --disable-dependency-tracking \
    --disable-liblilv \
    --enable-sys-readline \
    --with-python-includes=%{_includedir}/python2.7 \
    --with-python-modules=%{_libdir}/python2.7

%make

# (eandry) the tests dies at "pyecasound" on bs submit,
# but build fine with mdvsys build, so disabling for submission
#%%check
#%%make check


%install
install -d %{buildroot}%{py2_platsitedir}
%makeinstall_std ECA_S_RUBY_SITEDIR="%{ruby_sitelibdir}"

pushd pyecasound
%python_compile_opt
%python_compile
install *.pyc *.pyo %{buildroot}%{py2_platsitedir}
popd

sed -i 's:bin/env python:bin/env python2:' \
	"%{buildroot}%{_bindir}/ecamonitor"


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
#mv %{buildroot}/usr/lib/ruby/2.2.0/site_ruby/2.2/ %{buildroot}%{ruby_sitelibdir}


