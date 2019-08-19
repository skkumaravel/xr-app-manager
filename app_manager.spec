Name: xr-app-manager 
Version: 0.1.0
Release: XR_6.3.1+
License: Copyright (c) 2019 Cisco Systems Inc. All rights reserved.
Packager: cisco
SOURCE0 : %{name}-%{version}.tar.gz
Group: 3rd party application
Summary: XR App Manager compiled for WLR7 for IOS-XR 6.3.1+

%description
This is the set of python and sysvinit scripts for xr-app-manager for WRL7: XR 6.3.1+

%prep

%setup -q -n %{name}-%{version}

%install
mkdir -p %{buildroot}%{_sbindir}
install -m755 core/app_manager.py %{buildroot}%{_sbindir}
install -m755 ha_setup/standby_install.py %{buildroot}%{_sbindir}


mkdir -p %{buildroot}/etc/app_manager/
install -m644 config.json %{buildroot}/etc/app_manager

mkdir -p %{buildroot}/etc/rc.d/init.d
install -m755 sysvinit/app_manager.sh %{buildroot}/etc/rc.d/init.d/app_manager 

%files

%defattr(-,root,root)
%{_sbindir}/app_manager.py
%{_sbindir}/standby_install.py
/etc/app_manager/config.json
/etc/rc.d/init.d/app_manager

%post
chkconfig --add app_manager
# Mutiple files can be specified for scp to standby
%{_sbindir}/standby_install.py --file /etc/rc.d/init.d/app_manager --file %{_sbindir}/app_manager.py

# standby_install.py can be used to run bash commands on standby. Use this to create directories before trying to copy them over scp.
# Remember, bash commands are always executed at the end by standby_install.py. So decouple bash commands that are a prerequisite for any scp operation

%{_sbindir}/standby_install.py --cmd "chkconfig --add app_manager"

# standby_install.py can be used to run bash commands on standby. Use this to create directories before trying to copy them over scp
%{_sbindir}/standby_install.py --cmd "mkdir -p /etc/app_manager"
%{_sbindir}/standby_install.py --directory /etc/app_manager/

# Finally start the app_manager on active RP and on Standby RP (if present)
service app_manager restart
%{_sbindir}/standby_install.py --cmd "service app_manager restart"

%clean
rm -rf %{buildroot}
