# This package was forked from fedora-release into redhat-release-server into
# redhat-release-atomic-host, then into redhat-release-coreos.
# Be sure to look at changes upstream!

%define debug_package %{nil}
# Fake this out; we also use 8 here, matching the maipo's use of 7.
%define os_version 8.99
%define dist .el%{version}

Name:           redhat-release-coreos-ootpa
Version:        48
Release:        0%{?dist}
Summary:        %{product_family}%{?variant_titlecase: %{variant_titlecase}} release file
Group:          System Environment/Base
License:        GPLv2
Provides:       redhat-release = %{os_version}-%{release}
Provides:       system-release = %{os_version}-%{release}
# We need to use Server, since there's no RPM content set for anything else
Provides:       system-release(releasever) = %{base_release_version}Server
# This doesn't exist today, I committed the data to git
Source0:        redhat-release-%{variant_lowercase}-%{base_release_version}-4.tar.gz

%description
%{summary}

%prep
%setup -q -n redhat-release-%{base_release_version}

%build
make fs-ootpa

%install
rm -rf %{buildroot}
cp -a --reflink=auto fs-ootpa %{buildroot}

(cd %{buildroot} && find . -maxdepth 1 -type d | sed -e 's,^.,/,') > files.list

%files -f files.list
