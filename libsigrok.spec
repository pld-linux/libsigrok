Summary:	Basic hardware access drivers for logic analyzers
Name:		libsigrok
Version:	0.2.0
Release:	1
License:	GPL v3+
Group:		Libraries
URL:		http://www.sigrok.org/
Source0:	http://sigrok.org/download/source/libsigrok/%{name}-%{version}.tar.gz
# Source0-md5:	4683b44d99924def7f552dfc17537541
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	glib2-devel
BuildRequires:	graphviz
BuildRequires:	libftdi-devel
BuildRequires:	libtool
BuildRequires:	libusb-devel
BuildRequires:	libzip-devel
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	udev-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
%{name} is a shared library written in C which provides the basic API
for talking to logic analyzer hardware and reading/writing the
acquired data into various input/output file formats.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
install -d autostuff
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-static \
	--disable-silent-rules \
	--enable-all-drivers \

%{__make}

doxygen Doxyfile

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README NEWS
%attr(755,root,root) %{_libdir}/libsigrok.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsigrok.so.1

%files devel
%defattr(644,root,root,755)
%doc doxy/html-api/*
%{_includedir}/libsigrok
%attr(755,root,root) %{_libdir}/libsigrok.so
%{_pkgconfigdir}/libsigrok.pc