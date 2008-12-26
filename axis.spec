# TODO
#  - castor is needed by axis-1.2.1-0.2jpp.1.noarch
#  - package axis2, axis is obsolete. see NOTE below.
# NOTE
#  - it won't compile with java 1.6. see:
#    https://fcp.surfsite.org/modules/newbb/viewtopic.php?topic_id=55862&viewmode=flat&order=ASC&start=20
%define archivever %(echo %{version} | tr . _)
Summary:	A SOAP implementation in Java
Summary(pl.UTF-8):	Implementacja SOAP w Javie
Name:		axis
Version:	1.2.1
Release:	0.3
License:	Apache Software License
Group:		Development/Languages/Java
Source0:	http://ws.apache.org/axis//dist/%{archivever}/%{name}-src-%{archivever}.tar.gz
# Source0-md5:	157ad070accf373565bce80de1204a4d
URL:		http://ws.apache.org/axis/
BuildRequires:	ant >= 1.6
#BuildRequires:	ant-nodeps
BuildRequires:	jdk
# Mandatory requires
BuildRequires:	jaf
BuildRequires:	jakarta-commons-discovery
BuildRequires:	jakarta-commons-httpclient
BuildRequires:	jakarta-commons-logging
BuildRequires:	javamail
BuildRequires:	jaxp_parser_impl
BuildRequires:	jpackage-utils
BuildRequires:	logging-log4j
BuildRequires:	rpmbuild(macros) >= 1.300
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
Requires:	jaf
Requires:	jakarta-commons-discovery
Requires:	jakarta-commons-httpclient
Requires:	jakarta-commons-logging
Requires:	java
Requires:	javamail
Requires:	jaxp_parser_impl
Requires:	logging-log4j
Requires:	jpackage-utils
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

%description -l pl.UTF-8
Apache AXIS to implementacja SOAP ("Simple Object Access Protocol")
przekazanego do W3C.

Z projektu specyfikacji W3C:

SOAP to lekki protokół do wymiany informacji w scentralizowanym,
rozproszonym środowisku. Jest to protokół oparty na XML-u, składający
się z trzech części: koperty definiującej szkielet do opisu zawartości
i sposobu przetwarzania komunikatu, zbioru reguł kodowania do
wyrażania instancji typów danych zdefiniowanych w aplikacji oraz
konwencji reprezentowania zdalnych wywołań procedur i odpowiedzi.

Ten projekt jest następcą projektu Apache SOAP.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%package manual
Summary:	Manual for %{name}
Summary(pl.UTF-8):	Podręcznik do pakietu %{name}
Group:		Development/Languages/Java

%description manual
Documentation for %{name}.

%description manual -l pl.UTF-8
Podręcznik do pakietu %{name}.

%prep
%setup -q -n %{name}-%{archivever}

# Remove provided binaries
find -name '*.jar' | xargs rm -v
find -name '*.zip' | xargs rm -v
find -name '*.class' | xargs rm -v

%build
export JAVA_HOME=%{java_home}

CLASSPATH=$(build-classpath wsdl4j jakarta-commons-discovery jakarta-commons-httpclient jakarta-commons-logging log4j jaf javamail/mailapi servletapi5)
export CLASSPATH=$CLASSPATH:$(build-classpath oro junit jimi xml-security jsse httpunit jms castor 2>/dev/null)

export OPT_JAR_LIST="ant/ant-nodeps"
%ant \
	-Dcompile.ime=true \
	-Dwsdl4j.jar=$(find-jar wsdl4j) \
	-Dcommons-discovery.jar=$(find-jar jakarta-commons-discovery) \
	-Dcommons-logging.jar=$(find-jar jakarta-commons-logging) \
	-Dcommons-httpclient.jar=$(find-jar jakarta-commons-httpclient) \
	-Dlog4j-core.jar=$(find-jar log4j) \
	-Dactivation.jar=$(find-jar jaf) \
	-Dmailapi.jar=$(find-jar javamail/mailapi) \
	-Dxerces.jar=$(find-jar jaxp_parser_impl) \
	-Dservlet.jar=$(find-jar servletapi5) \
	-Dregexp.jar=$(find-jar oro) \
	-Djunit.jar=$(find-jar junit) \
	-Djimi.jar=$(find-jar jimi) \
	-Djsse.jar=$(find-jar jsse/jsse) \
	clean compile javadocs

%install
rm -rf $RPM_BUILD_ROOT
### Jar files
install -d $RPM_BUILD_ROOT%{_javadir}/%{name}

cd build/lib
install axis.jar axis-ant.jar saaj.jar jaxrpc.jar \
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
cp -a build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc LICENSE README release-notes.html changelog.html
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%files manual
%defattr(644,root,root,755)
%doc docs/*
