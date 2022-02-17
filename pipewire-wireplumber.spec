#
# Conditional build:
%bcond_without	apidocs		# API documentation

Summary:	Session / policy manager implementation for PipeWire
Name:		pipewire-wireplumber
Version:	0.4.8
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://gitlab.freedesktop.org/pipewire/wireplumber/-/archive/%{version}/wireplumber-%{version}.tar.bz2
# Source0-md5:	a5a405f0f8e973df9d644a20a8c0620b
Patch0:		va_list.patch
URL:		https://pipewire.org/
# required for both docs and introspection
BuildRequires:	doxygen >= 1.8.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.62
BuildRequires:	gobject-introspection-devel
%{?with_apidocs:BuildRequires:	graphviz}
BuildRequires:	lua-devel >= 5.3.0
BuildRequires:	meson >= 0.56.0
BuildRequires:	ninja
BuildRequires:	pipewire-devel >= 0.3.45
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	python3-lxml
BuildRequires:	python3-modules
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.011
BuildRequires:	systemd-devel
%if %{with apidocs}
BuildRequires:	python3-Sphinx
BuildRequires:	python3-breathe
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg >= 2.1.0
%endif
Requires(post,preun):	systemd-units >= 250.1
Requires:	%{name}-libs = %{version}-%{release}
Requires:	systemd-units >= 250.1
Provides:	pipewire-session-manager
Obsoletes:	pipewire-media-session
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
Requires:	pipewire-libs >= 0.3.45

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

%package apidocs
Summary:	API documentation for PipeWire WirePlumber
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for PipeWire WirePlumber.

%prep
%setup -q -n wireplumber-%{version}
%patch0 -p1

%build
%meson build \
	-Ddoc=%{__enabled_disabled apidocs} \
	-Dintrospection=enabled \
	-Dsystem-lua=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%{?with_apidocs:%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/wireplumber}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_user_post wireplumber.service

%preun
%systemd_user_preun wireplumber.service

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
%{_libdir}/girepository-1.0/Wp-0.4.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwireplumber-0.4.so
%{_includedir}/wireplumber-0.4
%{_pkgconfigdir}/wireplumber-0.4.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libwireplumber-0.4.a
%{_datadir}/gir-1.0/Wp-0.4.gir

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/docs/html
%endif
