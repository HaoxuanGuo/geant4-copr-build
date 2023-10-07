%if 0%{?fedora}<33||0%{?rhel} >= 8
%undefine __cmake_in_source_build
%endif

%global         optflags %(echo %{optflags} | sed 's/-O[0-3]/-O3 -DNDEBUG -fno-trapping-math -ftree-vectorize -fno-math-errno/')

Name:           geant4
Version:        11.1.2
Release:        1%{?dist}
Summary:        Toolkit for the simulation of the passage of particles through matter

License:        BSD
URL:            http://geant4.cern.ch/
Source:         https://geant4-data.web.cern.ch/releases/%{name}-v%{version}.tar.gz

BuildRequires:  motif-devel
BuildRequires:  libXi-devel
BuildRequires:  xerces-c-devel
BuildRequires:  expat-devel
BuildRequires:  zlib-devel
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  qt5-qtbase-devel

Recommends:     %{name}-data = %{version}-%{release}
Recommends:     %{name}-examples = %{version}-%{release}

%description
Geant4 is a toolkit for the simulation of the passage of particles through matter.
Its areas of application include high energy, nuclear and accelerator physics, as
well as studies in medical and space science.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

Recommends:     xerces-c-devel
Recommends:     expat-devel
Recommends:     zlib-devel
Recommends:     qt5-devel
Recommends:     cmake
Recommends:     make

%description    devel
Development files for %{name}.

%package examples
Summary:        Examples files for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    examples
Examples files for %{name}.

%package data
Summary:        Geant4 datasets
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    data
Geant4 datasets.

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
%cmake   -GNinja \
         -DGEANT4_BUILD_MULTITHREADED=ON \
         -DGEANT4_INSTALL_DATA=ON \
         -DGEANT4_USE_GDML=ON \
         -DGEANT4_USE_G3TOG4=OFF \
         -DGEANT4_USE_QT=ON \
         -DGEANT4_USE_XM=OFF \
         -DGEANT4_USE_INVENTOR=OFF \
         -DGEANT4_USE_RAYTRACER_X11=OFF \
         -DGEANT4_USE_SYSTEM_CLHEP=OFF \
         -DGEANT4_USE_SYSTEM_EXPAT=ON \
         -DGEANT4_USE_SYSTEM_ZLIB=ON \
         -DGEANT4_BUILD_TLS_MODEL=auto
%cmake_build

%install
%cmake_install

mkdir -p %{buildroot}%{_sysconfdir}/profile.d

cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}-data.sh <<EOF
pushd %{_bindir}/ >/dev/null; . ./geant4.sh; popd >/dev/null
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}-data.csh <<EOF
pushd %{_bindir}/ >/dev/null; . ./geant4.csh; popd >/dev/null
EOF

chmod -x %{buildroot}%{_datadir}/Geant4/geant4make/geant4make.csh

%ldconfig_scriptlets

%files
%defattr(-,root,root,-)
%doc LICENSE ReleaseNotes
%dir %{_datadir}/Geant4
%{_libdir}/libG*.so.*

%files devel
%{_libdir}/libG*.so
%{_bindir}/geant4-config
%{_includedir}/Geant4
%{_libdir}/Geant4-%{version}
%{_datadir}/Geant4
%{_libdir}/cmake/Geant4/*
%{_libdir}/pkgconfig/G4ptl.pc
%exclude %{_datadir}/Geant4/data
%exclude %{_datadir}/Geant4/examples

%files examples
%{_datadir}/Geant4/examples

%files data
%{_datadir}/Geant4/data
%{_bindir}/geant4.sh
%{_bindir}/geant4.csh
%{_sysconfdir}/profile.d/%{name}-data.sh
%{_sysconfdir}/profile.d/%{name}-data.csh

%changelog
* Sun Jan 29 23:12:00 CST 2023 Haoxuan Guo <kuohaoxuan@outlook.com> - 11.1.0-1
- update to 11.1 release and download data on compile time

* Wed Dec 30 00:28:23 CST 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.07-2
- add missing config flag

* Mon Dec 28 21:53:05 CST 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.07-1
- Update to 10.7 upstream release

* Wed Sep  2 10:43:42 CST 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.06.p02-6
- rebuilt

* Sun Aug 09 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.06.p02-5
- rebuilt

* Mon Jul 20 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.06.p02-4
- Out-of-Source Build

* Mon Jul 20 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.06.p02-3
- Cleanup builds for old fedora/epel release (they no longer build)

* Sun Jul 19 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.06.p02-2
- Use motif on RHEL > 8 release due to suggestion in issue #1

* Mon Jun 15 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.06.p02-1
- update to 10.06.p02 upstream

* Thu Apr 23 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.06.p01-4
- Use O3 build

* Fri Apr 10 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.06.p01-3
- rebuilt

* Sun Mar 29 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.06.p01-2
- rebuilt

* Sat Mar 14 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.06-4
- rebuilt

* Wed Mar 04 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.06-3
- rebuilt

* Mon Jan 27 2020 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.06-2
- rebuilt

* Thu Oct 17 2019 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.05.p01-3
- Fix Dep

* Thu Oct 17 2019 Qiyu Yan <yanqiyu@fedoraproject.org> - 10.05.p01
- geant4.10.05.p01

* Wed Jan  6 2016 Alexey Kurov <nucleo@fedoraproject.org> - 10.01.p02-1
- geant4.10.01.p02

* Wed Jan  6 2016 Alexey Kurov <nucleo@fedoraproject.org> - 10.01-1
- Initial RPM release
