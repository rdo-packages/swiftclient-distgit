%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-swiftclient
Version:    3.0.0
Release:    1%{?dist}
Summary:    Client Library for OpenStack Object Storage API
License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{name}
Source0:    http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

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
Requires:      python-simplejson
Requires:      python-futures
Requires:      python-requests
Requires:      python-six

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
%setup -q -n %{name}-%{upstream_version}

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

# Remove bundled egg-info
rm -rf python_swiftclient.egg-info

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

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
%{python2_sitelib}/swiftclient
%{python2_sitelib}/*.egg-info
%{_mandir}/man1/swift.1*

%files doc
%doc LICENSE doc/build/html

%changelog
* Wed Mar 23 2016 Haikel Guemar <hguemar@fedoraproject.org> 3.0.0-
- Update to 3.0.0


