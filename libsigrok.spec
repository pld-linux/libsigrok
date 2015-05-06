#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Basic hardware access drivers for logic analyzers
Summary(pl.UTF-8):	Podstawowe sterowniki dostępu do sprzętu dla analizatorów logicznych
Name:		libsigrok
Version:	0.3.0
Release:	2
License:	GPL v3+
Group:		Libraries
Source0:	http://sigrok.org/download/source/libsigrok/%{name}-%{version}.tar.gz
# Source0-md5:	6bc9fa9da9b791b8da961003244adeec
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
BuildRequires:	libserialport-devel >= 0.1.0
BuildRequires:	libtool >= 2:2
BuildRequires:	libusb-devel >= 1.0.16
BuildRequires:	libzip-devel >= 0.10
BuildRequires:	pkgconfig >= 1:0.22
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

%prep
%setup -q

%build
install -d autostuff
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-all-drivers \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

doxygen Doxyfile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib/udev/rules.d,%{_datadir}/sigrok-firmware}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

sed -e 's#plugdev#usb#g' contrib/z60_libsigrok.rules > $RPM_BUILD_ROOT/lib/udev/rules.d/60-libsigrok.rules

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsigrok.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README README.devices
%attr(755,root,root) %{_libdir}/libsigrok.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsigrok.so.2
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
