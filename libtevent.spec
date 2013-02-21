%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
%{!?python_version: %global python_version %(%{__python} -c "from distutils.sysconfig import get_python_version; print(get_python_version())")}

Name: libtevent
Version: 0.9.17
Release: 1%{?dist}
Group: System Environment/Daemons
Summary: The tevent library
License: LGPLv3+
URL: http://tevent.samba.org/
Source: http://samba.org/ftp/tevent/tevent-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: libtalloc-devel >= 2.0.7
BuildRequires: python-devel
BuildRequires: pytalloc-devel >= 2.0.7
BuildRequires: doxygen
BuildRequires: docbook-style-xsl
BuildRequires: libxslt


%description
Tevent is an event system based on the talloc memory management library.
Tevent has support for many event types, including timers, signals, and
the classic file descriptor events.
Tevent also provide helpers to deal with asynchronous code providing the
tevent_req (Tevent Request) functions.

%package devel
Group: Development/Libraries
Summary: Developer tools for the Tevent library
Requires: libtevent = %{version}-%{release}
Requires: libtalloc-devel >= 2.0.7
Requires: pkgconfig

%description devel
Header files needed to develop programs that link against the Tevent library.

%package -n python-tevent
Group: Development/Libraries
Summary: Python bindings for the Tevent library
Requires: libtevent = %{version}-%{release}

%description -n python-tevent
Python bindings for libtevent

%prep
%setup -q -n tevent-%{version}

%build
%configure --disable-rpath \
           --bundled-libraries=NONE \
           --builtin-libraries=replace

make %{?_smp_mflags} V=1

doxygen doxy.config

%check
make %{?_smp_mflags} check

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libtevent.a

# Install API docs
rm -f doc/man/man3/todo*
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
cp -a doc/man/* $RPM_BUILD_ROOT/%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libtevent.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/tevent.h
%{_libdir}/libtevent.so
%{_libdir}/pkgconfig/tevent.pc
%{_mandir}/man3/tevent*.gz

%files -n python-tevent
%defattr(-,root,root,-)
%{python_sitearch}/tevent.py*
%{python_sitearch}/_tevent.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Mon Aug 20 2010 Jakub Hrozek <jhrozek@redhat.com> - 0.9.17-1
- Rebase to 0.9.17 to provide the version Samba4 needs
- Drop EXCLUDE_PATTERNS workaround in specfile
- Resolves: rhbz#766336

* Fri Aug 03 2010 Jakub Hrozek <jhrozek@redhat.com> - 0.9.16-4
- Fix EXCLUDE_PATTERNS in doxyfile

- Related: rhbz#766336

* Fri Aug 03 2010 Jakub Hrozek <jhrozek@redhat.com> - 0.9.16-3
- Update doxygen file before building documentation

- Related: rhbz#766336

* Thu Aug 02 2010 Jakub Hrozek <jhrozek@redhat.com> - 0.9.16-2
- Add BuildRequires on libxslt and docbook-style-xsl to enable
  building manual pages

- Related: rhbz#766336

* Thu Aug 02 2010 Jakub Hrozek <jhrozek@redhat.com> - 0.9.16-1
- Rebase to 0.9.16 to provide the version Samba4 needs
- Resolves: rhbz#766336
- Drop ABI compatibility patch (no longer needed)

* Fri May 21 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.9.8-8
- Run make check during RPM build
- Fix abi_check patch to guarantee script executability

* Wed Feb 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.9.8-7.1
- Remove all references to ABI compatibility patch

* Wed Feb 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 0.9.8-7
- Drop ABI compatibility patch (no longer needed)

* Wed Sep 23 2009 Simo Sorce <ssorce@redhat.com> - 0.9.8-5
- Add patch to fix a segfault case

* Wed Sep 16 2009 Simo Sorce <ssorce@redhat.com> - 0.9.8-2
- Fix abi compatibility with 0.9.3

* Sat Sep 8 2009 Simo Sorce <ssorce@redhat.com> - 0.9.8-1
- First independent release for tevent 0.9.8
