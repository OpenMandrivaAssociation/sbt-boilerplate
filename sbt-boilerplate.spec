Name:		sbt-boilerplate
Version:	0.6.1
Release:	1
Summary:	Template expander from sbt-boilerplate
Group:		Development/Java
License:	BSD-2-Clause
URL:		https://github.com/sbt/sbt-boilerplate
Source0:	sbt-boilerplate-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	scala = 2.13.16
BuildRequires:	scala-parser-combinators = 1.1.2
BuildRequires:	java-1.8.0-openjdk-devel
Requires:	java-1.8.0-openjdk
Requires:	mvn(org.scala-lang:scala-library) = 2.13.16
Requires:	mvn(org.scala-lang.modules:scala-parser-combinators_2.13) = 1.1.2

%description
sbt-boilerplate %{version} generator, compiled for Scala 2.13.16. This is
the template engine from tag v0.6.1, not the sbt plugin. The build adds
spray.boilerplate.ExpandMain so sjson-new can expand its templates without
sbt. Nothing is downloaded at build time.

%prep
%autosetup -n sbt-boilerplate-%{version}
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
test -s LICENSE
test -s compile.sh
test -s check.sh
test -s src/main/scala/spray/boilerplate/Generator.scala
test -s src/main/scala/spray/boilerplate/TemplateParser.scala

%build
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./compile.sh

%install
set -eo pipefail
test -s sbt-boilerplate.jar
install -d %{buildroot}%{_javadir}
install -m 644 sbt-boilerplate.jar %{buildroot}%{_javadir}/sbt-boilerplate-%{version}.jar

%check
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./check.sh

%files
%license LICENSE
%{_javadir}/sbt-boilerplate-%{version}.jar
