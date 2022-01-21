Summary: A Filesystem Benchmark Tool
Name: iozone
%define real_version 3_493
Version: 3.493
Release: 1%{?dist}
License: Freeware
Group: Applications/System
URL: http://www.iozone.org/

%define _disable_source_fetch 0
Source0: http://www.iozone.org/src/current/iozone%{real_version}.tgz
Source1: http://www.iozone.org/docs/Iozone_License.txt
BuildRequires: gcc, dos2unix
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
IOzone is a filesystem benchmark tool. The benchmark generates and
measures a variety of file operations. Iozone has been ported to
many machines and runs under many operating systems.

Iozone is useful for performing a broad filesystem analysis of a vendors
computer platform. The benchmark tests file I/O performance for the following
operations: Read, write, re-read, re-write, read backwards, read strided,
fread, fwrite, random read, pread ,mmap, aio_read, aio_write.

%prep
%setup -n %{name}%{real_version}
cp %{SOURCE1} .

%build
%ifarch %{ix86}
  %define mfile linux
%else
  %ifarch x86_64
    %define mfile linux-AMD64
  %else
    %ifarch ppc %{power64}
      %define mfile linux-powerpc64
    %else
      %ifarch %{arm} aarch64
        %define mfile linux-arm
      %else
        echo "No idea how to build for your arch..."
        exit 1
      %endif
    %endif
  %endif
%endif
%{__rm} -f src/current/*.o
export CFLAGS=$RPM_OPT_FLAGS
%{__make} %{?_smp_mflags} -C src/current %{mfile}

sed -i '1s/^/#!\/bin\/bash\n/' src/current/Generate_Graphs
dos2unix src/current/report.pl
dos2unix src/current/iozone_visualizer.pl
sed -i '1s/env perl/perl/' src/current/iozone_visualizer.pl
dos2unix src/current/Gnuplot.txt
dos2unix docs/iozone.1

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0755 src/current/iozone %{buildroot}%{_bindir}/iozone
%{__install} -Dp -m0755 src/current/Generate_Graphs %{buildroot}%{_datadir}/iozone/Generate_Graphs
%{__install} -Dp -m0755 src/current/gengnuplot.sh %{buildroot}%{_datadir}/iozone/gengnuplot.sh
%{__install} -Dp -m0644 src/current/gnu3d.dem %{buildroot}%{_datadir}/iozone/gnu3d.dem
%{__install} -Dp -m0755 src/current/iozone_visualizer.pl %{buildroot}%{_datadir}/iozone/iozone_visualizer.pl
%{__install} -Dp -m0755 src/current/report.pl %{buildroot}%{_datadir}/iozone/report.pl
%{__install} -Dp -m0644 docs/iozone.1 %{buildroot}%{_mandir}/man1/iozone.1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%license Iozone_License.txt
%attr(0644, root, root) %doc src/current/Changes.txt src/current/Gnuplot.txt docs/*
#%attr(0755, root, root) %doc src/current/*.pl src/current/*.sh
%doc %{_mandir}/man1/iozone.1*
%{_bindir}/iozone
%{_datadir}/iozone/

%changelog
* Fri Jan 21 2022 Chen Chen <aflyhorse@fedoraproject.org> - 3.493-1
- Update to release 3.493

* Sun Jan 31 2021 Chen Chen <aflyhorse@fedoraproject.org> - 3.491-1
- Update to release 3.491
- Remove junk obj files left in upstream tarball
- Add rpm default CFLAGS
- Simplify make command

* Thu Sep 10 2020 Chen Chen <aflyhorse@fedoraproject.org> - 3.490-1
- Update to release 3.490
- Fix file permissions of docs
- Fix line breakers

* Sun Mar 8 2020 Chen Chen <aflyhorse@fedoraproject.org> - 3.489-1
- Update to release 3.489
- Add aarch64 support

* Tue Apr 30 2019 Chen Chen <aflyhorse@fedoraproject.org> - 3.487-2
- Add license file for author's sake
- Add gcc BuildRequires for recent Fedora
- Fix ppc

* Tue Apr 30 2019 Chen Chen <aflyhorse@fedoraproject.org> - 3.487-1
- Update to release 3.487

* Wed Nov 8 2017 Niels de Vos <ndevos@redhat.com> - 3.471-1
- Update to release 3.471
- Initial package based on an earlier version from RepoForge.Org
