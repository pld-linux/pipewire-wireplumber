Summary:	Session / policy manager implementation for PipeWire
Name:		pipewire-wireplumber
Version:	0.4.4
Release:	0.1
License:	MIT
Group:		Libraries
Source0:	https://gitlab.freedesktop.org/pipewire/wireplumber/-/archive/%{version}/wireplumber-%{version}.tar.bz2
# Source0-md5:	bc389c723b4368b4e73e06eafce95d40
URL:		https://pipewire.org/
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.62
BuildRequires:	lua-devel >= 5.3.0
BuildRequires:	meson >= 0.56.0
BuildRequires:	ninja
BuildRequires:	pipewire-devel >= 0.3.37
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	systemd-devel
Requires:	%{name}-libs = %{version}-%{release}
Provides:	pipewire-session-manager
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WirePlumber is a modular session / policy manager for PipeWire and a
GObject-based high-level library that wraps PipeWire's API, providing
convenience for writing the daemon's modules as well as external tools
for managing PipeWire.

The WirePlumber daemon implements the session & policy management
service. It follows a modular design, having plugins that implement
the actual management functionality.

%package libs
Summary:	WirePlumber shared library
Group:		Libraries
Requires:	glib2 >= 1:2.62
Requires:	pipewire-libs >= 0.3.37

%description libs
WirePlumber shared library.

%package devel
Summary:	Header files for WirePlumber library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for WirePlumber library.

%package static
Summary:	WirePlumber static library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
WirePlumber static library.

%prep
%setup -q -n wireplumber-%{version}

%build
%meson build \
	-Dsystem-lua=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wireplumber
%attr(755,root,root) %{_bindir}/wpctl
%attr(755,root,root) %{_bindir}/wpexec
%{systemduserunitdir}/wireplumber.service
%{systemduserunitdir}/wireplumber@.service
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-default-nodes-api.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-default-nodes.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-default-profile.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-device-activation.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-file-monitor-api.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-logind.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-lua-scripting.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-metadata.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-mixer-api.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-portal-permissionstore.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-reserve-device.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-route-settings-api.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-si-audio-adapter.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-si-audio-endpoint.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-si-node.so
%attr(755,root,root) %{_libdir}/wireplumber-0.4/libwireplumber-module-si-standard-link.so
%{_datadir}/wireplumber/bluetooth.conf
%{_datadir}/wireplumber/bluetooth.lua.d
%{_datadir}/wireplumber/common
%{_datadir}/wireplumber/main.conf
%{_datadir}/wireplumber/main.lua.d
%{_datadir}/wireplumber/policy.conf
%{_datadir}/wireplumber/policy.lua.d
%{_datadir}/wireplumber/scripts
%{_datadir}/wireplumber/wireplumber.conf

%files libs
%defattr(644,root,root,755)
%doc NEWS.rst README.rst
%attr(755,root,root) %{_libdir}/libwireplumber-0.4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwireplumber-0.4.so.0
%dir %{_libdir}/wireplumber-0.4
%dir %{_datadir}/wireplumber

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwireplumber-0.4.so
%{_includedir}/wireplumber-0.4
%{_pkgconfigdir}/wireplumber-0.4.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libwireplumber-0.4.a