Name:           glpi
Version:        9.5.5
Release:        1%{?dist}
Summary:        Free IT asset management software
License:        AGPLv3+
Group:          Networking/WWW
URL:            https://github.com/glpi-project/glpi/
Source0:        https://github.com/glpi-project/glpi/releases/download/%{version}/%{name}-%{version}.tgz 
Source1: glpi-httpd.conf
Source2: glpi-logrotate
Source3: glpi-downstream.php
Source4: glpi-local_define.php
Source5: glpi-cron
Requires:       httpd
Requires:	    php
Requires:       %{_sysconfdir}/logrotate.d
Requires:       crontabs

BuildArch:      noarch

%description
GLPI is the Information Resource-Manager with an additional Administration-
Interface. You can use it to build up a database with an inventory for your 
company (computer, software, printers...). It has enhanced functions to make
the daily life for the administrators easier, like a job-tracking-system with
mail-notification and methods to build a database with basic information 
about your network-topology.

%prep
mkdir %{name}-%{version}
cd %{name}-%{version}
tar xzvf %{SOURCE0}

%build
# Nothing to do!!

%install

# set specific settings
mkdir -p %{buildroot}/etc/%{name}
cp  %SOURCE4 %{buildroot}%{_sysconfdir}/%{name}/local_define.php

# configuration file path
mkdir -p %{buildroot}/usr/share/%{name}/inc
cp  %SOURCE3 %{buildroot}/usr/share/glpi/inc/downstream.php

# === cron ====
mkdir -p %{buildroot}/%{_sysconfdir}/cron.d
cp  %SOURCE5 %{buildroot}/%{_sysconfdir}/cron.d/%{name}


# ===== files =====
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}
mv %{name}-%{version}/%{name}/files %{buildroot}/%{_localstatedir}/lib/%{name}/files

# ===== log =====
mkdir -p %{buildroot}%{_localstatedir}/log
mv %{buildroot}/%{_localstatedir}/lib/%{name}/files/_log %{buildroot}%{_localstatedir}/log/%{name}

# move all files to /usr/share/glpi
install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -r %{name}-%{version}/%{name}/* %{buildroot}%{_datadir}/%{name}

# Apache with mod_php or php-fpm
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Log rotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cp -pr %SOURCE2 %{buildroot}%{_sysconfdir}/logrotate.d/glpi


# clean up
find %{buildroot} -name remove.txt -exec rm -f {} \; -print

%files
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/glpi
%attr(0750,root,root) %{_sysconfdir}/%{name}/local_define.php
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/config
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/marketplace
%ghost %config(noreplace,missingok) %{_sysconfdir}/%{name}/config_db.php
%ghost %config(noreplace,missingok) %{_sysconfdir}/%{name}/local_define.php
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
# This folder can contain private information (sessions, docs, ...)
%dir %_localstatedir/lib/%{name}/files
%attr(2770,root,apache) %{_localstatedir}/lib/%{name}/files
%attr(2770,root,apache) %dir %{_localstatedir}/log/%{name}

%post

%postun

%clean

%changelog

* Mon Aug 16 2021 stephane de labrusse <stephdl@de-labrusse.fr> 9.5.5
- first release
