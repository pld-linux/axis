# TODO
#  - castor is needed by axis-1.2.1-0.2jpp.1.noarch
#  - package axis2, axis is obsolete. see NOTE below.
#  - build samples
#  - package war app
# NOTE
#  - it won't compile with java 1.6. see:
#    https://fcp.surfsite.org/modules/newbb/viewtopic.php?topic_id=55862&viewmode=flat&order=ASC&start=20

%bcond_with	java_sun
%define archivever %(echo %{version} | tr . _)
Summary:	A SOAP implementation in Java
Summary(pl.UTF-8):	Implementacja SOAP w Javie
Name:		axis
Version:	1.4
Release:	0.1
License:	Apache
Group:		Development/Languages/Java
Source0:	http://ws.apache.org/axis/dist/%{archivever}/%{name}-src-%{archivever}.tar.gz
# Source0-md5:	3dcce3cbd37f52d70ebeb858f90608dc
Source1:	%{name}-build.xml
Patch0:		%{name}-classpath.patch
Patch1:		%{name}-missing_xsd.patch
URL:		http://ws.apache.org/axis/
BuildRequires:	ant >= 1.6
BuildRequires:	ant-nodeps
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun <= 1.5}
# BuildRequires:	jimi
# BuildRequires:	jms
BuildRequires:	httpunit
BuildRequires:	jaf
BuildRequires:	java-commons-discovery
BuildRequires:	java-commons-httpclient
BuildRequires:	java-commons-logging
BuildRequires:	java-commons-net
BuildRequires:	java-oro
BuildRequires:	java-xalan
BuildRequires:	java-xerces
BuildRequires:	java-xml-commons
BuildRequires:	java-xmlbeans
BuildRequires:	javamail
BuildRequires:	jpackage-utils
BuildRequires:	jsse
BuildRequires:	junit
BuildRequires:	logging-log4j
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	servletapi5
BuildRequires:	wsdl4j
Requires:	httpunit
Requires:	jaf
Requires:	java-commons-discovery
Requires:	java-commons-httpclient
Requires:	java-commons-logging
Requires:	java-commons-net
Requires:	java-oro
Requires:	java-xalan
Requires:	java-xerces
Requires:	java-xml-commons
Requires:	java-xmlbeans
Requires:	javamail
Requires:	jpackage-utils
Requires:	jsse
Requires:	logging-log4j
Requires:	servletapi5
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
find -name '*.class' | xargs rm -v

%patch0 -p1
%patch1 -p1

cp %{SOURCE1} build.xml

%build
export JAVA_HOME=%{java_home}
echo $JAVA_HOME

activation_jar=$(find-jar activation)
commons_logging_jar=$(find-jar commons-logging)
commons_discovery_jar=$(find-jar commons-discovery)
commons_httpclient_jar=$(find-jar commons-httpclient)
commons_net_jar=$(find-jar commons-net)
log4j_core_jar=$(find-jar log4j)
jsse_jar=$(find-jar jsse)
junit_jar=$(find-jar junit)
mailapi_jar=$(find-jar mail)
regexp_jar=$(find-jar oro)
servlet_jar=$(find-jar servletapi5)
tools_jar=$(find-jar tools)
wsdl4j_jar=$(find-jar wsdl4j)
xalan_jar=$(find-jar xalan)
xerces_jar=$(find-jar xerces-j2)
xercesImpl_jar=$(find-jar xercesImpl)
xml_apis_jar=$(find-jar xml-commons-apis)
xmlParsersAPIs_jar=$(find-jar xerces-j2)
xmlbeans_jar=$(find-jar xmlbeans)
%{!?with_java_sun:libgcj_jar=$(find-jar libgcj)}

#httpunit_jar=$(find-jar httpunit)
#xmlunit_jar=$(find-jar xmlunit)
#jimi_jar=$(find-jar jimi)

CLASSPATH=$wsdl4j_jar:$commons_logging_jar:$commons_discovery_jar
%{!?with_java_sun:CLASSPATH=$CLASSPATH:$(build-classpath ecj tools)}
export CLASSPATH

%ant dist \
	-Dactivation.jar=$activation_jar \
	-Dcommons-logging.jar=$commons_logging_jar \
	-Dcommons-discovery.jar=$commons_discovery_jar \
	-Dcommons-httpclient.jar=$commons_httpclient_jar \
	-Dcommons-net.jar=$commons_net_jar \
	-Dlog4j-core.jar=$log4j_core_jar \
	-Djsse.jar=$jsse_jar \
	-Djunit.jar=$junit_jar \
	-Dmailapi.jar=$mailapi_jar \
	-Dregexp.jar=$regexp_jar \
	-Dservlet.jar=$servlet_jar \
	-Dtools.jar=$tools_jar \
	-Dwsdl4j.jar=$wsdl4j_jar \
	-Dxalan.jar=$xalan_jar \
	-Dxerces.jar=$xerces_jar \
	-DxercesImpl.jar=$xercesImpl_jar \
	-Dxml-apis.jar=$xml_apis_jar \
	-DxmlParsersAPIs.jar=$xmlParsersAPIs_jar \
	-Dxmlbeans.jar=$xmlbeans_jar \
	%{!?with_java_sun:-Dsun.boot.class.path="$libgcj_jar:[-org.w3c.dom/*]"}

%install
rm -rf $RPM_BUILD_ROOT

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
