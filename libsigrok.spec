# TODO:
# - bindings (ruby, java)
#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define	module	sigrok

Summary:	Basic hardware access drivers for logic analyzers
Summary(pl.UTF-8):	Podstawowe sterowniki dostępu do sprzętu dla analizatorów logicznych
Name:		libsigrok
Version:	0.4.0
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	http://sigrok.org/download/source/libsigrok/%{name}-%{version}.tar.gz
# Source0-md5:	6cd64b94be0b8ce7224de8c823f735aa
URL:		http://www.sigrok.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
#BuildRequires:	check >= 0.9.4
BuildRequires:	doxygen
BuildRequires:	gcc >= 6:4.0
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	graphviz
BuildRequires:	libftdi-devel >= 0.16
BuildRequires:	librevisa-devel >= 0.0.20130812
BuildRequires:	libserialport-devel >= 0.1.1
BuildRequires:	libtool >= 2:2
BuildRequires:	libusb-devel >= 1.0.16
BuildRequires:	libzip-devel >= 0.10
BuildRequires:	pkgconfig >= 1:0.22
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-numpy-devel
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-numpy-devel
BuildRequires:	python3-setuptools
%endif
Requires:	glib2 >= 1:2.32.0
Requires:	libftdi >= 0.16
Requires:	librevisa >= 0.0.20130812
Requires:	libserialport >= 0.1.0
Requires:	libusb >= 1.0.16
Requires:	libzip >= 0.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libsigrok is a shared library written in C which provides the basic
API for talking to logic analyzer hardware and reading/writing the
acquired data into various input/output file formats.

%description -l pl.UTF-8
libsigrok to napisana w C biblioteka współdzielona udostępniająca
podstawowe API do komunikacji ze sprzętowymi analizatorami logicznymi
oraz odczytu/zapisu uzyskanych danych z/do różnych formatów plików
wejściowych/wyjściowych.

%package devel
Summary:	Development files for libsigrok
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libsigrok
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32.0
Requires:	libftdi-devel >= 0.16
Requires:	librevisa-devel >= 0.0.20130812
Requires:	libusb-devel >= 1.0.16
Requires:	libzip-devel >= 0.10

%description devel
This package contains the header files for developing applications
that use libsigrok.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libsigrok.

%package static
Summary:	Static libsigrok library
Summary(pl.UTF-8):	Statyczna biblioteka libsigrok
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libsigrok library.

%description static -l pl.UTF-8
Statyczna biblioteka libsigrok.

%package c++
Summary:	C++ libsigrok library
Summary(pl.UTF-8):	Biblioteka C++ libsigrok
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
C++ libsigrok library.

%description c++ -l pl.UTF-8
Biblioteka C++ libsigrok.

%package c++-devel
Summary:	Header files for develop C++ libsigrok based application
Summary(pl.UTF-8):	Pliki nagłówkowe do biblioteki C++ libsigrok
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}

%description c++-devel
This package includes the header files and libraries necessary to
develop applications that use C++ libsigrok.

%description c++-devel -l pl.UTF-8
Pakiet ten zawiera pliki nagłówkowe niezbędne do kompilacji programów
z wykorzystaniem biblioteki c++-libsigrok.

%package c++-static
Summary:	Static libraries for C++ libsigrok
Summary(pl.UTF-8):	Biblioteki statyczne C++ libsigrok
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
This package includes the static libraries necessary to develop
applications that use C++ libsigrok.

%description c++-static -l pl.UTF-8
Pakiet ten zawiera biblioteki statyczne C++ libsigrok.

%package -n python-%{module}
Summary:	libsigrok python bindings
Group:		Libraries/Python
Requires:	python-modules

%description -n python-%{module}
libsigrok python bindings.

%package -n python3-%{module}
Summary:	libsigrok python bindings
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
libsigrok python bindings.

%prep
%setup -q

%build
install -d autostuff
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

%if %{with python3}
install -d .py3-bindings
cp -a * .py3-bindings

cd .py3-bindings
%configure \
	PYTHON="%{__python3}" \
	--disable-all-drivers \
	--disable-silent-rules \
	--disable-ruby \
	--disable-java \
	--disable-static \
	--enable-python
%{__make} python-build
cd ..
%endif

%configure \
	PYTHON="%{__python}" \
	--enable-all-drivers \
	--disable-silent-rules \
	--disable-ruby \
	--disable-java \
	--%{?with_python2:en}%{!?with_python2:dis}able-python \
	%{!?with_static_libs:--disable-static}

%{__make}

doxygen Doxyfile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib/udev/rules.d,%{_datadir}/sigrok-firmware}

%if %{with python3}
%{__make} -C .py3-bindings python-install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

sed -e 's#plugdev#usb#g' contrib/z60_libsigrok.rules > $RPM_BUILD_ROOT/lib/udev/rules.d/60-libsigrok.rules

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsigrok{,cxx}.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	c++ -p /sbin/ldconfig
%postun	c++ -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README README.devices
%attr(755,root,root) %{_libdir}/libsigrok.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsigrok.so.3
/lib/udev/rules.d/60-libsigrok.rules
%{_datadir}/sigrok-firmware

%files devel
%defattr(644,root,root,755)
%doc doxy/html-api/*
%attr(755,root,root) %{_libdir}/libsigrok.so
%{_includedir}/libsigrok
%{_pkgconfigdir}/libsigrok.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsigrok.a
%endif

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsigrokcxx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsigrokcxx.so.3

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsigrokcxx.so
%{_includedir}/libsigrokcxx
%{_pkgconfigdir}/libsigrokcxx.pc

%if %{with static_libs}
%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libsigrokcxx.a
%endif

%if %{with python2}
%files -n python-%{module}
%defattr(644,root,root,755)
%{py_sitedir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitedir}/*%{module}-%{version}-py*.egg-info
%{py_sitedir}/*%{module}-%{version}-py*.pth
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%{py3_sitedir}/%{module}
%{py3_sitedir}/*%{module}-%{version}-py*.egg-info
%{py3_sitedir}/*%{module}-%{version}-py*.pth
%endif
