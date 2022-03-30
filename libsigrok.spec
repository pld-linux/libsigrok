# TODO: where to package?
#%{_datadir}/mime/packages/vnd.sigrok.session.xml
#%{_iconsdir}/hicolor/48x48/mimetypes/libsigrok.png
#%{_iconsdir}/hicolor/scalable/mimetypes/libsigrok.svg
#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	gpib		# GPIB interface support
%bcond_with	java		# Java bindings
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module
%bcond_with	ruby		# Ruby module

Summary:	Basic hardware access drivers for logic analyzers
Summary(pl.UTF-8):	Podstawowe sterowniki dostępu do sprzętu dla analizatorów logicznych
Name:		libsigrok
Version:	0.5.2
Release:	5
License:	GPL v3+
Group:		Libraries
Source0:	http://sigrok.org/download/source/libsigrok/%{name}-%{version}.tar.gz
# Source0-md5:	e258d471b6d5eaa58daf927a0dc3ba67
Patch0:		%{name}-python.patch

Patch2:		%{name}-ruby.patch
Patch3:		%{name}-java.patch
URL:		https://sigrok.org/wiki/Libsigrok
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	bluez-libs-devel >= 4.0
#BuildRequires:	check >= 0.9.4
BuildRequires:	doxygen
BuildRequires:	gcc >= 6:4.0
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	glibmm-devel >= 2.32.0
BuildRequires:	graphviz
BuildRequires:	hidapi-devel >= 0.8.0
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libftdi1-devel >= 1.0
BuildRequires:	libieee1284-devel
BuildRequires:	librevisa-devel >= 0.0.20130812
BuildRequires:	libserialport-devel >= 0.1.1
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2
BuildRequires:	libusb-devel >= 1.0.16
BuildRequires:	libzip-devel >= 0.10
%{?with_gpib:BuildRequires:	linux-gpib-devel}
BuildRequires:	pkgconfig >= 1:0.22
# required also for C++ binding
BuildRequires:	python >= 1:2.7
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-numpy-devel
BuildRequires:	python-pygobject3-devel >= 3.8.0
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-numpy-devel
BuildRequires:	python3-pygobject3-devel >= 3.8.0
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
%{?with_ruby:BuildRequires:	ruby-devel}
%{?with_java:BuildRequires:	swig}
%if %{with python2} || %{with python3}
BuildRequires:	swig-python
%endif
%{?with_ruby:BuildRequires:	swig-ruby >= 3.0.8}
Requires:	glib2 >= 1:2.32.0
Requires:	libftdi1 >= 1.0
Requires:	librevisa >= 0.0.20130812
Requires:	libserialport >= 0.1.1
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
Requires:	libftdi1-devel >= 1.0
Requires:	libieee1284-devel
Requires:	librevisa-devel >= 0.0.20130812
Requires:	libserialport-devel >= 0.1.1
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
Summary:	C++ bindings for libsigrok library
Summary(pl.UTF-8):	Wiązania C++ do biblioteki libsigrok
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glibmm >= 2.32.0

%description c++
C++ bindings for libsigrok library.

%description c++ -l pl.UTF-8
Wiązania C++ do biblioteki libsigrok.

%package c++-devel
Summary:	Header files for libsigrokcxx based applications
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsigrokcxx
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	glibmm-devel >= 2.32.0
Requires:	libstdc++-devel

%description c++-devel
This package includes the header files necessary to develop
applications that use libsigrokcxx library.

%description c++-devel -l pl.UTF-8
Pakiet ten zawiera pliki nagłówkowe niezbędne do kompilacji programów
z wykorzystaniem biblioteki libsigrokcxx.

%package c++-static
Summary:	Static libsigrokcxx library
Summary(pl.UTF-8):	Biblioteka statyczna libsigrokcxx
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
Static libsigrokcxx library.

%description c++-static -l pl.UTF-8
Biblioteka statyczna libsigrokcxx.

%package -n java-sigrok
Summary:	Java bindings for libsigrok library
Summary(pl.UTF-8):	Wiązania Javy do biblioteki libsigrok
Group:		Libraries/Java
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	jre

%description -n java-sigrok
Java bindings for libsigrok library.

%description -n java-sigrok -l pl.UTF-8
Wiązania Javy do biblioteki libsigrok.

%package -n python-sigrok
Summary:	Python 2 bindings for libsigrok library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki libsigrok
Group:		Libraries/Python
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	python-modules >= 1:2.7
Requires:	python-pygobject3 >= 3.8.0

%description -n python-sigrok
Python 2 bindings for libsigrok library.

%description -n python-sigrok -l pl.UTF-8
Wiązania Pythona 2 do biblioteki libsigrok.

%package -n python3-sigrok
Summary:	Python 3 bindings for libsigrok library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki libsigrok
Group:		Libraries/Python
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	python3-modules >= 1:3.2
Requires:	python3-pygobject3 >= 3.8.0

%description -n python3-sigrok
Python 3 bindings for libsigrok library.

%description -n python3-sigrok -l pl.UTF-8
Wiązania Pythona 3 do biblioteki libsigrok.

%package -n ruby-sigrok
Summary:	Ruby bindings for libsigrok library
Summary(pl.UTF-8):	Wiązania języka Ruby do biblioteki libsigrok
Group:		Libraries/Java
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	ruby

%description -n ruby-sigrok
Ruby bindings for libsigrok library.

%description -n ruby-sigrok -l pl.UTF-8
Wiązania języka Ruby do biblioteki libsigrok.

%prep
%setup -q
%patch0 -p1

%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

%if %{with python3}
install -d build-py3
cd build-py3

../%configure \
	PYTHON="%{__python3}" \
	--disable-all-drivers \
	--disable-java \
	--disable-ruby \
	--disable-silent-rules \
	--disable-static \
	--enable-python
%{__make} python-build
cd ..
%endif

%configure \
	PYTHON="%{__python}" \
	--enable-all-drivers=yes \
	--enable-java%{!?with_java:=no} \
	--enable-python%{!?with_python2:=no} \
	--enable-ruby%{!?with_ruby:=no} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-libgpib%{!?with_gpib:=no}

%{__make}

doxygen Doxyfile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib/udev/rules.d,%{_datadir}/sigrok-firmware}

%if %{with python3}
%{__make} -C build-py3 python-install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsigrok{,cxx}.la

%if %{with python2}
%py_postclean
%endif

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
%attr(755,root,root) %ghost %{_libdir}/libsigrok.so.4
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
%attr(755,root,root) %ghost %{_libdir}/libsigrokcxx.so.4

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

%if %{with java}
%files -n java-sigrok
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsigrok_java_core_classes.so
%{_javadir}/sigrok-core.jar
%endif

%if %{with python2}
%files -n python-sigrok
%defattr(644,root,root,755)
%dir %{py_sitedir}/sigrok
%dir %{py_sitedir}/sigrok/core
%attr(755,root,root) %{py_sitedir}/sigrok/core/_classes.so
%{py_sitedir}/sigrok/core/*.py[co]
%{py_sitedir}/libsigrok-%{version}-py*.egg-info
%{py_sitedir}/libsigrok-%{version}-py*.pth
%endif

%if %{with python3}
%files -n python3-sigrok
%defattr(644,root,root,755)
%dir %{py3_sitedir}/sigrok
%dir %{py3_sitedir}/sigrok/core
%attr(755,root,root) %{py3_sitedir}/sigrok/core/_classes.cpython-*.so
%{py3_sitedir}/sigrok/core/*.py
%{py3_sitedir}/sigrok/core/__pycache__
%{py3_sitedir}/libsigrok-%{version}-py*.egg-info
%{py3_sitedir}/libsigrok-%{version}-py*.pth
%endif

%if %{with ruby}
%files -n ruby-sigrok
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_vendorarchdir}/sigrok.so
%endif
