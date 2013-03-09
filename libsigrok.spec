#
%bcond_with	alsa
%bcond_with	mso19
#
Summary:	Basic hardware access drivers for logic analyzers
Name:		libsigrok
Version:	0.1.1
Release:	1
License:	GPL v3+
Group:		Libraries
URL:		http://www.sigrok.org/
Source0:	http://downloads.sourceforge.net/sigrok/%{name}-%{version}.tar.gz
# Source0-md5:	285c0b69aa3d36a431bf752c4f70c755
%{?with_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	doxygen
BuildRequires:	glib2-devel
BuildRequires:	graphviz
BuildRequires:	libftdi-devel
BuildRequires:	libusb-devel
BuildRequires:	libzip-devel
BuildRequires:	udev-devel
BuildRequires:	zlib-devel

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
%configure \
	--disable-static \
	--disable-silent-rules \
	--%{?with_alsa:en}%{!?with_alsa:dis}able-alsa \
	--enable-asix-sigma \
	--enable-chronovu-la8 \
	--enable-fx2lafw \
	--enable-demo \
	--%{?with_mso19:en}%{!?with_mso19:dis}able-link-mso19 \
	--enable-ols \
	--enable-zeroplus-logic-cube

%{__make}

doxygen Doxyfile

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README NEWS COPYING ChangeLog
%attr(755,root,root) %{_libdir}/libsigrok.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsigrok.so.0

%files devel
%defattr(644,root,root,755)
%doc doxy/html/*
%{_includedir}/sigrok*.h
%attr(755,root,root) %{_libdir}/*.so
%{_pkgconfigdir}/*.pc
