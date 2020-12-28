%if 0%{?fedora}<33||0%{?rhel} >= 8
%undefine __cmake_in_source_build
%endif

%define         libversion 10.7.0

%define         G4NDL_version 4.6
%define         G4EMLOW_version 7.13
%define         G4PhotonEvaporation_version 5.7
%define         G4RadioactiveDecay_version 5.6
%define         G4PARTICLEXS_version 3.1
%define         G4PII_version 1.3
%define         G4RealSurface_version 2.2
%define         G4SAIDDATA_version 2.0
%define         G4ABLA_version 3.1
%define         G4INCL_version 1.0
%define         G4ENSDFSTATE_version 2.3

%global         optflags %(echo %{optflags} | sed 's/-O[0-3]/-O3 -flto -fno-fat-lto-objects -DNDEBUG -fno-trapping-math -ftree-vectorize -fno-math-errno/')

Name:           geant4
Version:        10.07
Release:        1%{?dist}
Summary:        Toolkit for the simulation of the passage of particles through matter

License:        BSD
URL:            http://geant4.cern.ch/
Source0:        https://geant4-data.web.cern.ch/geant4-data/releases/%{name}.%{version}.tar.gz
Source1:        https://cern.ch/geant4-data/datasets/G4NDL.%{G4NDL_version}.tar.gz
Source2:        https://cern.ch/geant4-data/datasets/G4EMLOW.%{G4EMLOW_version}.tar.gz
Source3:        https://cern.ch/geant4-data/datasets/G4PhotonEvaporation.%{G4PhotonEvaporation_version}.tar.gz
Source4:        https://cern.ch/geant4-data/datasets/G4RadioactiveDecay.%{G4RadioactiveDecay_version}.tar.gz
Source5:        https://cern.ch/geant4-data/datasets/G4PARTICLEXS.%{G4PARTICLEXS_version}.tar.gz
Source6:        https://cern.ch/geant4-data/datasets/G4PII.%{G4PII_version}.tar.gz
Source7:        https://cern.ch/geant4-data/datasets/G4RealSurface.%{G4RealSurface_version}.tar.gz
Source8:        https://cern.ch/geant4-data/datasets/G4SAIDDATA.%{G4SAIDDATA_version}.tar.gz
Source9:        https://cern.ch/geant4-data/datasets/G4ABLA.%{G4ABLA_version}.tar.gz
Source10:       https://cern.ch/geant4-data/datasets/G4INCL.%{G4INCL_version}.tar.gz
Source11:       https://cern.ch/geant4-data/datasets/G4ENSDFSTATE.%{G4ENSDFSTATE_version}.tar.gz
Patch0:         0001-fix-soversion.patch


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
%setup -q -n %{name}.%{version}
%patch0 -p1

%build
%cmake   -GNinja \
         -DGEANT4_BUILD_MULTITHREADED=ON \
         -DGEANT4_INSTALL_DATA=OFF \
         -DGEANT4_USE_GDML=ON \
         -DGEANT4_USE_G3TOG4=OFF \
         -DGEANT4_USE_QT=ON \
         -DGEANT4_USE_XM=OFF \
         -DGEANT4_USE_INVENTOR=OFF \
         -DGEANT4_USE_RAYTRACER_X11=OFF \
         -DGEANT4_USE_SYSTEM_CLHEP=OFF \
         -DGEANT4_USE_SYSTEM_EXPAT=ON \
         -DGEANT4_USE_SYSTEM_ZLIB=ON \
         -DGEANT4_BUILD_CXXSTD=14
%cmake_build

%install
%cmake_install

rm -rf %{buildroot}%{_bindir}/geant4.sh %{buildroot}%{_bindir}/geant4.csh

mkdir -p %{buildroot}%{_sysconfdir}/profile.d

cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}-data.sh <<EOF
export G4NEUTRONHPDATA="%{_datadir}/Geant4-%{libversion}/data/G4NDL%{G4NDL_version}"
export G4LEDATA="%{_datadir}/Geant4-%{libversion}/data/G4EMLOW%{G4EMLOW_version}"
export G4LEVELGAMMADATA="%{_datadir}/Geant4-%{libversion}/data/PhotonEvaporation%{G4PhotonEvaporation_version}"
export G4RADIOACTIVEDATA="%{_datadir}/Geant4-%{libversion}/data/RadioactiveDecay%{G4RadioactiveDecay_version}"
export G4PARTICLEXSDATA="%{_datadir}/Geant4-%{libversion}/data/G4PARTICLEXS%{G4PARTICLEXS_version}"
export G4PIIDATA="%{_datadir}/Geant4-%{libversion}/data/G4PII%{G4PII_version}"
export G4REALSURFACEDATA="%{_datadir}/Geant4-%{libversion}/data/RealSurface%{G4RealSurface_version}"
export G4SAIDXSDATA="%{_datadir}/Geant4-%{libversion}/data/G4SAIDDATA%{G4SAIDDATA_version}"
export G4ABLADATA="%{_datadir}/Geant4-%{libversion}/data/G4ABLA%{G4ABLA_version}"
export G4INCLDATA="%{_datadir}/Geant4-%{libversion}/data/G4INCL%{G4INCL_version}"
export G4ENSDFSTATEDATA="%{_datadir}/Geant4-%{libversion}/data/G4ENSDFSTATE%{G4ENSDFSTATE_version}"
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}-data.csh <<EOF
setenv G4NEUTRONHPDATA "%{_datadir}/Geant4-%{libversion}/data/G4NDL%{G4NDL_version}"
setenv G4LEDATA "%{_datadir}/Geant4-%{libversion}/data/G4EMLOW%{G4EMLOW_version}"
setenv G4LEVELGAMMADATA "%{_datadir}/Geant4-%{libversion}/data/PhotonEvaporation%{G4PhotonEvaporation_version}"
setenv G4RADIOACTIVEDATA "%{_datadir}/Geant4-%{libversion}/data/RadioactiveDecay%{G4RadioactiveDecay_version}"
setenv G4PARTICLEXSDATA "%{_datadir}/Geant4-%{libversion}/data/G4PARTICLEXS%{G4PARTICLEXS_version}"
setenv G4PIIDATA "%{_datadir}/Geant4-%{libversion}/data/G4PII%{G4PII_version}"
setenv G4REALSURFACEDATA "%{_datadir}/Geant4-%{libversion}/data/RealSurface%{G4RealSurface_version}"
setenv G4SAIDXSDATA "%{_datadir}/Geant4-%{libversion}/data/G4SAIDDATA%{G4SAIDDATA_version}"
setenv G4ABLADATA "%{_datadir}/Geant4-%{libversion}/data/G4ABLA%{G4ABLA_version}"
setenv G4INCLDATA "%{_datadir}/Geant4-%{libversion}/data/G4INCL%{G4INCL_version}"
setenv G4ENSDFSTATEDATA "%{_datadir}/Geant4-%{libversion}/data/G4ENSDFSTATE%{G4ENSDFSTATE_version}"
EOF
mkdir -p %{buildroot}%{_datadir}/Geant4-%{libversion}/data
tar -zxf %{S:1} --directory %{buildroot}%{_datadir}/Geant4-%{libversion}/data
tar -zxf %{S:2} --directory %{buildroot}%{_datadir}/Geant4-%{libversion}/data
tar -zxf %{S:3} --directory %{buildroot}%{_datadir}/Geant4-%{libversion}/data
tar -zxf %{S:4} --directory %{buildroot}%{_datadir}/Geant4-%{libversion}/data
tar -zxf %{S:5} --directory %{buildroot}%{_datadir}/Geant4-%{libversion}/data
tar -zxf %{S:6} --directory %{buildroot}%{_datadir}/Geant4-%{libversion}/data
tar -zxf %{S:7} --directory %{buildroot}%{_datadir}/Geant4-%{libversion}/data
tar -zxf %{S:8} --directory %{buildroot}%{_datadir}/Geant4-%{libversion}/data
tar -zxf %{S:9} --directory %{buildroot}%{_datadir}/Geant4-%{libversion}/data
tar -zxf %{S:10} --directory %{buildroot}%{_datadir}/Geant4-%{libversion}/data
tar -zxf %{S:11} --directory %{buildroot}%{_datadir}/Geant4-%{libversion}/data

%ldconfig_scriptlets

%files
%defattr(-,root,root,-)
%doc LICENSE ReleaseNotes
%dir %{_datadir}/Geant4-%{libversion}
%{_libdir}/libG*.so.*

%files devel
%{_libdir}/libG*.so
%{_bindir}/geant4-config
%{_includedir}/Geant4
%{_includedir}/PTL
%{_libdir}/Geant4-%{libversion}
%{_libdir}/PTL
%{_datadir}/Geant4-%{libversion}
%exclude %{_datadir}/Geant4-%{libversion}/data
%exclude %{_datadir}/Geant4-%{libversion}/examples

%files examples
%{_datadir}/Geant4-%{libversion}/examples

%files data
%{_datadir}/Geant4-%{libversion}/data
%{_sysconfdir}/profile.d/%{name}-data.csh
%{_sysconfdir}/profile.d/%{name}-data.sh

%changelog
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
