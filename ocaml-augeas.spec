# TODO: optflags?
#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif
Summary:	Augeas binding for OCaml
Summary(pl.UTF-8):	Wiązania augeasa dla OCamla
Name:		ocaml-augeas
Version:	0.6
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://people.redhat.com/~rjones/augeas/files/%{name}-%{version}.tar.gz
# Source0-md5:	16837f2caf4764e46068a58e5b9d6c9b
Patch0:		%{name}-no-ocamlopt.patch
Patch1:		ocaml-4.09.patch
URL:		http://augeas.net/
BuildRequires:	augeas-devel >= 1.2.0
BuildRequires:	autoconf
BuildRequires:	libxml2-devel
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-findlib
BuildRequires:	pkgconfig
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains files needed to run bytecode executables using
augeas library.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających biblioteki augeas.

%package devel
Summary:	Augeas binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania augeasa dla OCamla - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
augeas library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
biblioteki augeas.

%prep
%setup -q
%{!?with_ocaml_opt:%patch0 -p1}
%patch -P1 -p1

%build
%{__autoconf}
%{__autoheader}
%configure

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{augeas,stublibs}

install augeas.cmi libmlaugeas.a mlaugeas.cma $RPM_BUILD_ROOT%{_libdir}/ocaml/augeas
%if %{with ocaml_opt}
install augeas.cmx mlaugeas.{a,cmxa} $RPM_BUILD_ROOT%{_libdir}/ocaml/augeas
%endif
install dllmlaugeas.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
install -D META $RPM_BUILD_ROOT%{_libdir}/ocaml/augeas/META

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllmlaugeas.so

%files devel
%defattr(644,root,root,755)
%doc augeas.mli
%dir %{_libdir}/ocaml/augeas
%{_libdir}/ocaml/augeas/META
%{_libdir}/ocaml/augeas/augeas.cmi
%{_libdir}/ocaml/augeas/libmlaugeas.a
%{_libdir}/ocaml/augeas/mlaugeas.cma
%if %{with ocaml_opt}
%{_libdir}/ocaml/augeas/augeas.cmx
%{_libdir}/ocaml/augeas/mlaugeas.a
%{_libdir}/ocaml/augeas/mlaugeas.cmxa
%endif
