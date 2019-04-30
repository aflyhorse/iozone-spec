Summary: IOzone Filesystem Benchmark
Name: iozone
%define real_version 3_487
Version: 3.487
Release: 1%{?dist}
License: Freeware
Group: Applications/System
URL: http://www.iozone.org/

Source: http://www.iozone.org/src/current/iozone%{real_version}.tar
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
IOzone is a filesystem benchmark tool. The benchmark generates and
measures a variety of file operations. Iozone has been ported to
many machines and runs under many operating systems.

Iozone is useful for performing a broad filesystem analysis of a vendors
computer platform. The benchmark tests file I/O performance for the following
operations: Read, write, re-read, re-write, read backwards, read strided,
fread, fwrite, random read, pread ,mmap, aio_read, aio_write.

%global debug_package %{nil}

%prep
%setup -n %{name}%{real_version}

%build
%ifarch %{ix86}
  %{__make} %{?_smp_mflags} -C src/current linux
%else
  %ifarch x86_64
     %{__make} %{?_smp_mflags} -C src/current linux-AMD64
  %else
    %ifarch ppc64
      %{__make} %{?_smp_mflags} -C src/current linux-powerpc64
    %else
      %ifarch %(arm)
        %{__make} %{?_smp_mflags} -C src/current linux-arm
      %else
        echo "No idea how to build for your arch..."
        exit 1
      %endif
    %endif
  %endif
%endif

sed -i '1s/^/#!\/bin\/bash\n/' src/current/Generate_Graphs

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0755 src/current/iozone %{buildroot}%{_bindir}/iozone
%{__install} -Dp -m0755 src/current/Generate_Graphs %{buildroot}%{_datadir}/iozone/Generate_Graphs
%{__install} -Dp -m0755 src/current/gengnuplot.sh %{buildroot}%{_datadir}/iozone/gengnuplot.sh
%{__install} -Dp -m0755 src/current/gnu3d.dem %{buildroot}%{_datadir}/iozone/gnu3d.dem
%{__install} -Dp -m0644 docs/iozone.1 %{buildroot}%{_mandir}/man1/iozone.1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc src/current/Changes.txt src/current/Gnuplot.txt
%doc src/current/*.pl src/current/*.sh docs/*
%doc %{_mandir}/man1/iozone.1*
%{_bindir}/iozone
%{_datadir}/iozone/

%changelog
* Tue Apr 30 2019 Chen Chen <aflyhorse@fedoraproject.org> - 3.487-1
- Update to release 3.487

* Wed Nov 8 2017 Niels de Vos <ndevos@redhat.com> - 3.471-1
- Update to release 3.471
- Initial package based on an earlier version from RepoForge.Org
