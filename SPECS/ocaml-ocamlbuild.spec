%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Name:          ocaml-ocamlbuild
Version:       0.12.0
Release:       1%{?dist}

Summary:       Build tool for OCaml libraries and programs

License:       LGPLv2+ with exceptions

URL:           https://github.com/ocaml/ocamlbuild

Source0: https://repo.citrite.net:443/ctx-local-contrib/xs-opam/ocamlbuild-0.12.0.tar.gz




BuildRequires: ocaml >= 4.04.0


%description
OCamlbuild is a build tool for building OCaml libraries and programs.


%package devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}


%description devel
This package contains development files for %{name}.


%package doc
Summary:       Documentation for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}


%description doc
This package contains the manual for %{name}.


%prep
%setup -q -n ocamlbuild-%{version}


%build
make configure \
  OCAMLBUILD_PREFIX=%{_prefix} \
  OCAMLBUILD_BINDIR=%{_bindir} \
  OCAMLBUILD_LIBDIR=%{_libdir}/ocaml \
%ifarch %{ocaml_native_compiler}
  OCAML_NATIVE=true
%else
  OCAML_NATIVE=false
%endif

make %{?_smp_mflags}


%install
make install \
     DESTDIR=$RPM_BUILD_ROOT \
     CHECK_IF_PREINSTALLED=false

# Install the man page, which for some reason is not copied
# in by the make install rule above.
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
install -p -m 0644 man/ocamlbuild.1 $RPM_BUILD_ROOT%{_mandir}/man1/

# Remove the META file.  It will be replaced by ocaml-ocamlfind (findlib).
rm $RPM_BUILD_ROOT%{_libdir}/ocaml/ocamlbuild/META


%files
%doc Changes Readme.md VERSION
%license LICENSE
%{_bindir}/ocamlbuild
%{_bindir}/ocamlbuild.byte
%ifarch %{ocaml_native_compiler}
%{_bindir}/ocamlbuild.native
%endif
%{_mandir}/man1/ocamlbuild.1*
%{_libdir}/ocaml/ocamlbuild
%ifarch %{ocaml_native_compiler}
%exclude %{_libdir}/ocaml/ocamlbuild/*.a
%exclude %{_libdir}/ocaml/ocamlbuild/*.o
%exclude %{_libdir}/ocaml/ocamlbuild/*.cmx
%exclude %{_libdir}/ocaml/ocamlbuild/*.cmxa
%endif
%exclude %{_libdir}/ocaml/ocamlbuild/*.mli


%files devel
%license LICENSE
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/ocamlbuild/*.a
%{_libdir}/ocaml/ocamlbuild/*.o
%{_libdir}/ocaml/ocamlbuild/*.cmx
%{_libdir}/ocaml/ocamlbuild/*.cmxa
%endif
%{_libdir}/ocaml/ocamlbuild/*.mli


%files doc
%license LICENSE
%doc manual/*


%changelog
* Fri Jul 06 2018 Christian Lindig <christian.lindig@citrix.com> - 0.12.0-1
- Update to version 0.12.0 (same as in xs-opam-{src,repo}.spec)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 0.9.3-5
- New package, ocamlbuild used to be part of ocaml.
