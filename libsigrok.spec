%define	snap	a618599
#
Summary:	Basic hardware access drivers for logic analyzers
Name:		libsigrok
Version:	0.2.0
Release:	0.%{snap}.1
License:	GPL v3+
Group:		Libraries
URL:		http://www.sigrok.org/
#Source0:	http://downloads.sourceforge.net/sigrok/%{name}-%{version}.tar.gz
#Source0:	http://sigrok.org/gitweb/?p=libsigrok.git;a=snapshot;h=%{snap};sf=tgz;/%{name}-%{snap}.tar.gz
Source0:	%{name}-%{snap}.tar.gz
# Source0-md5:	0605e573435ba6334cb8e1270a4b060a
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
%setup -q -n %{name}-%{snap}

grep AM_PROG_CC_C_O configure.ac && exit 1
echo AM_PROG_CC_C_O >> configure.ac

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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README NEWS
%attr(755,root,root) %{_libdir}/libsigrok.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsigrok.so.2

%files devel
%defattr(644,root,root,755)
%doc doxy/html-api/*
%{_includedir}/libsigrok
%attr(755,root,root) %{_libdir}/*.so
%{_pkgconfigdir}/libsigrok.pc
