%define		fversion	%(echo %{version} |tr . -)
Summary:	WebServices - Axis
Summary(pl):	WebServices - Axis
Name:		axis
Version:	1.2
Release:	0.1
License:	Apache Software License
Group:		Development/Libraries
Source0:	http://www.apache.org/dist/ws/axis-c/source/linux/%{name}-c-src-%{fversion}-linux.tar.gz
# Source0-md5:	9c68ba2f2d8029aed0694881bc2f491b
URL:		http://ws.apache.org/%{name}/
BuildRequires:	expat-devel
BuildRequires:	xerces-c-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache Axis is an implementation of the SOAP ("Simple Object Access
Protocol") submission to W3C.

%description -l pl
Apache Axis jest implementacj± SOAP ("Simple Object Access Protocol")
przekazan± do W3C.

%prep
%setup -q -n axis-c-src-%{fversion}-linux
rm -rf include/expat
ln -sf %{_includedir} include/expat

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CFLAGS="%{rpmcflags} -I`pwd`/include"
CXXFLAGS="%{rpmcflags} -I`pwd`/include"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
