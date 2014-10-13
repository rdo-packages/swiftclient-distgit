Name:       python-swiftclient
Version:    2.3.1
Release:    1%{?dist}
Summary:    Client Library for OpenStack Object Storage API
License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{name}
Source0:    http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

Patch0001: 0001-Remove-builtin-requirements-handling.patch
Patch0002: 0002-Patch-docs-to-use-oslo.sphinx.patch

BuildArch:  noarch
Requires:   python-keystoneclient
Requires:   python-requests
# /usr/bin/swift collision with older swift-im rhbz#857900
Conflicts:  swift < 2.0-0.3

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-d2to1
BuildRequires: python-pbr
BuildRequires: python-requests
BuildRequires: python-six

%description
Client library and command line utility for interacting with Openstack
Object Storage API.

%package doc
Summary:    Documentation for OpenStack Object Storage API Client
Group:      Documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description doc
Documentation for the client library for interacting with Openstack
Object Storage API.

%prep
%setup -q

%patch0001 -p1
%patch0002 -p1

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

# Remove bundled egg-info
rm -rf python_swiftclient.egg-info

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make html
popd

install -p -D -m 644 doc/manpages/swift.1 %{buildroot}%{_mandir}/man1/swift.1

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%files
%doc LICENSE README.rst
%{_bindir}/swift
%{python_sitelib}/swiftclient
%{python_sitelib}/*.egg-info
%{_mandir}/man1/swift.1*

%files doc
%doc LICENSE doc/build/html

%changelog
* Mon Oct 13 2014 Jakub Ruzicka <jruzicka@redhat.com> 2.3.1-1
- Update to upstream 2.3.1

* Thu Sep 18 2014 Pete Zaitcev <zaitcev@redhat.com> 2.3.0-1
- Update to upstream 2.3.0 (Juno RC)
- Upstream update includes fix for bz#1126942
- Upstream update includes support for Keystone v3
- New build dependency: python-oslo-sphinx

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Jakub Ruzicka <jruzicka@redhat.com> 2.1.0-1
- Update to upstream 2.1.0
- New dependency: python-six

* Thu Feb 27 2014 Jakub Ruzicka <jruzicka@redhat.com> 2.0.2-1
- Update to upstream 2.0.2
- Switch from pyOpenSSL to python-requests - update dependencies
- Remove unneeded dependency: python-simplejson

* Tue Feb 11 2014 Pete Zaitcev <zaitcev@redhat.com> 1.8.0-2
- Fix the fix for CVE-2013-6395: EBADF, wildcards

* Tue Dec 10 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.8.0-1
- Update to upstream 1.8.0
- Add SSL certificate verification by default (CVE-2013-6396)
- New runtime and build dependency: pyOpenSSL
- New runtime dependency: python-keystoneclient
- python-pbr has been removed from runtime by upstream

* Tue Oct 08 2013 Jakub Ruzicka <jruzicka@redhat.com> - 1.7.0-1
- Update to upstream 1.7.0.

* Mon Sep 02 2013 Jakub Ruzicka <jruzicka@redhat.com> - 1.6.0-1
- Update to upstream 1.6.0.
- Include man page.
- Remove all pbr deps in the patch instead of this spec file.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.5.0-1
- Update to upstream 1.5.0 release.
- Add new build requires: python-pbr, python-d2to1.
- Remove runtime dependency on python-pbr.

* Mon May 13 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.4.0-1
- Update to upstream 1.4.0 release.

* Sat Mar 09 2013 Alan Pevec <apevec@redhat.com> 1.3.0-1
- Update to 1.3.0 release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Alan Pevec <apevec@redhat.com> 1.2.0-2
- conflict with swift-im bz#857900

* Thu Sep 13 2012 Alan Pevec <apevec@redhat.com> 1.2.0-1
- Update to 1.2.0 release.

* Tue Jul 31 2012 Alan Pevec <apevec@redhat.com> 1.1.1-1
- Initial release.
