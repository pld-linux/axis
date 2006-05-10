# TODO
#  - servletapi5 is needed by axis-1.2.1-0.2jpp.1.noarch
#  - castor is needed by axis-1.2.1-0.2jpp.1.noarch
%define archivever %(echo %{version} | tr . _)
Summary:	A SOAP implementation in Java
Name:		axis
Version:	1.2.1
Release:	0.2jpp.1
License:	Apache Software License
Group:		Development/Languages/Java
URL:		http://ws.apache.org/axis/
Source0:	%{url}/dist/%{archivever}/%{name}-src-%{archivever}.tar.gz
# Source0-md5:	157ad070accf373565bce80de1204a4d
#BuildRequires:	ant-nodeps
BuildRequires:	jakarta-ant >= 1.6
BuildRequires:	jdk
# Mandatory requires
BuildRequires:	jaf
BuildRequires:	jakarta-commons-discovery
BuildRequires:	jakarta-commons-httpclient3
BuildRequires:	jakarta-commons-logging
BuildRequires:	jakarta-log4j
BuildRequires:	javamail
BuildRequires:	jaxp_parser_impl
BuildRequires:	servletapi5
BuildRequires:	wsdl4j
# optional requires
BuildRequires:	castor
BuildRequires:	httpunit
BuildRequires:	jakarta-oro
BuildRequires:	jimi
BuildRequires:	jms
BuildRequires:	jsse
BuildRequires:	junit
#BuildRequires: xml-security
Requires:	jaf
Requires:	jakarta-commons-discovery
Requires:	jakarta-commons-httpclient3
Requires:	jakarta-commons-logging
Requires:	java
Requires:	javamail
Requires:	jaxp_parser_impl
#Requires:	jpackage-utils >= 0:1.5
Requires:	log4j
Requires:	wsdl4j
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache AXIS is an implementation of the SOAP ("Simple Object Access
Protocol") submission to W3C.

From the draft W3C specification:

SOAP is a lightweight protocol for exchange of information in a
decentralized, distributed environment. It is an XML based protocol
that consists of three parts: an envelope that defines a framework for
describing what is in a message and how to process it, a set of
encoding rules for expressing instances of application-defined
datatypes, and a convention for representing remote procedure calls
and responses.

This project is a follow-on to the Apache SOAP project.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Languages/Java

%description javadoc
Javadoc for %{name}.

%package manual
Summary:	Manual for %{name}
Group:		Development/Languages/Java

%description manual
Documentation for %{name}.

%prep
%setup -q -n %{name}-%{archivever}

# Remove provided binaries
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.zip" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;

%build

[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java

CLASSPATH=$(build-classpath wsdl4j jakarta-commons-discovery jakarta-commons-httpclient3 jakarta-commons-logging log4j jaf javamail/mailapi servletapi5)
export CLASSPATH=$CLASSPATH:$(build-classpath oro junit jimi xml-security jsse httpunit jms castor 2>/dev/null)

export OPT_JAR_LIST="ant/ant-nodeps"
ant -Dcompile.ime=true \
	-Dwsdl4j.jar=$(build-classpath wsdl4j) \
	-Dcommons-discovery.jar=$(build-classpath jakarta-commons-discovery) \
	-Dcommons-logging.jar=$(build-classpath jakarta-commons-logging) \
	-Dcommons-httpclient.jar=$(build-classpath jakarta-commons-httpclient3) \
	-Dlog4j-core.jar=$(build-classpath log4j) \
	-Dactivation.jar=$(build-classpath jaf) \
	-Dmailapi.jar=$(build-classpath javamail/mailapi) \
	-Dxerces.jar=$(build-classpath jaxp_parser_impl) \
	-Dservlet.jar=$(build-classpath servletapi5) \
	-Dregexp.jar=$(build-classpath oro 2>/dev/null) \
	-Djunit.jar=$(build-classpath junit 2>/dev/null) \
	-Djimi.jar=$(build-classpath jimi 2>/dev/null) \
	-Djsse.jar=$(build-classpath jsse/jsse 2>/dev/null) \
	clean compile javadocs

%install

rm -rf $RPM_BUILD_ROOT
### Jar files

install -d $RPM_BUILD_ROOT%{_javadir}/%{name}

cd build/lib
   install -m 644 axis.jar axis-ant.jar saaj.jar jaxrpc.jar \
           $RPM_BUILD_ROOT%{_javadir}/%{name}
cd -

cd $RPM_BUILD_ROOT%{_javadir}/%{name}
	for jar in *.jar ; do
		vjar=$(echo $jar | sed s+.jar+-%{version}.jar+g)
		mv $jar $vjar
		ln -fs $vjar $jar
	done
cd -

### Javadoc

install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

cd docs
   rm -fr apiDocs
   ln -fs %{_javadocdir}/%{name} apiDocs
cd -

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc LICENSE README release-notes.html changelog.html
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar

%files javadoc
%defattr(644,root,root,755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*

%files manual
%defattr(644,root,root,755)
%doc docs/*
