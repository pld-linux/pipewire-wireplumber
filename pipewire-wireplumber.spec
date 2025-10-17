#
# Conditional build:
%bcond_without	apidocs		# API documentation and wpctl man page
%bcond_with	elogind		# elogind instead of systemd
%bcond_without	static_libs	# static_library

Summary:	Session / policy manager implementation for PipeWire
Summary(pl.UTF-8):	Implementacja zarządcy sesji / polityk dla PipeWire
Name:		pipewire-wireplumber
Version:	0.5.12
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://gitlab.freedesktop.org/pipewire/wireplumber/-/tags
Source0:	https://gitlab.freedesktop.org/pipewire/wireplumber/-/archive/%{version}/wireplumber-%{version}.tar.bz2
# Source0-md5:	42f9b6cbd8d1aa27c80598348463f874
URL:		https://pipewire.org/
# required for both docs and introspection
BuildRequires:	doxygen >= 1.8.0
%{?with_elogind:BuildRequires:	elogind-devel}
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.68
BuildRequires:	gobject-introspection-devel
%{?with_apidocs:BuildRequires:	graphviz}
BuildRequires:	lua-devel >= 5.3.0
BuildRequires:	meson >= 0.59.0
BuildRequires:	ninja
BuildRequires:	pipewire-devel >= 1.0.2
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	python3-lxml
BuildRequires:	python3-modules
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
%{!?with_elogind:BuildRequires:	systemd-devel}
%if %{with apidocs}
BuildRequires:	python3-Sphinx
BuildRequires:	python3-breathe
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg >= 2.1.0
%endif
Requires(post,preun):	systemd-units >= 1:250.1
Requires:	%{name}-libs = %{version}-%{release}
Requires:	systemd-units >= 1:250.1
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

%description -l pl.UTF-8
WirePlumber to modularny zarządca sesji / polityk dla PipeWire oraz
oparta na GObject biblioteka wysokiego poziomu obudowująca API
PipeWire, pozwalająca na wygodne tworzenie modułów demona oraz
zewnętrznych narzędzi do zarządzania PipeWire.

%package libs
Summary:	WirePlumber shared library
Summary(pl.UTF-8):	Biblioteka współdzielona WirePlumber
Group:		Libraries
Requires:	glib2 >= 1:2.68
Requires:	pipewire-libs >= 1.0.2

%description libs
WirePlumber shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona WirePlumber.

%package devel
Summary:	Header files for WirePlumber library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki WirePlumber
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for WirePlumber library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki WirePlumber.

%package static
Summary:	WirePlumber static library
Summary(pl.UTF-8):	Biblioteka statyczna WirePlumber
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
WirePlumber static library.

%description static -l pl.UTF-8
Biblioteka statyczna WirePlumber.

%package apidocs
Summary:	API documentation for PipeWire WirePlumber
Summary(pl.UTF-8):	Dokumentacja API PipeWire WirePlumber
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for PipeWire WirePlumber.

%description apidocs -l pl.UTF-8
Dokumentacja API PipeWire WirePlumber.

%prep
%setup -q -n wireplumber-%{version}

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	-Ddoc=%{__enabled_disabled apidocs} \
	-Delogind=%{__enabled_disabled elogind} \
	-Dintrospection=enabled \
	-Dsystem-lua=true \
	-Dsystemd=%{__enabled_disabled_not elogind}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%{?with_apidocs:%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/wireplumber}

%find_lang wireplumber

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_user_post wireplumber.service

%preun
%systemd_user_preun wireplumber.service

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f wireplumber.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wireplumber
%attr(755,root,root) %{_bindir}/wpctl
%attr(755,root,root) %{_bindir}/wpexec
%{systemduserunitdir}/wireplumber.service
%{systemduserunitdir}/wireplumber@.service
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-dbus-connection.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-default-nodes-api.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-file-monitor-api.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-log-settings.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-logind.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-lua-scripting.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-mixer-api.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-modem-manager.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-mpris.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-notifications-api.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-portal-permissionstore.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-reserve-device.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-settings.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-si-audio-adapter.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-si-node.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-si-standard-link.so
%attr(755,root,root) %{_libdir}/wireplumber-0.5/libwireplumber-module-standard-event-source.so
%dir %{_datadir}/wireplumber/wireplumber.conf.d
%{_datadir}/wireplumber/wireplumber.conf.d/alsa-vm.conf
%{_datadir}/wireplumber/scripts
%{_datadir}/wireplumber/wireplumber.conf
%if %{with apidocs}
%{_mandir}/man1/wpctl.1*
%endif
%{zsh_compdir}/_wpctl

%files libs
%defattr(644,root,root,755)
%doc NEWS.rst README.rst
%attr(755,root,root) %{_libdir}/libwireplumber-0.5.so.*.*.*
%ghost %{_libdir}/libwireplumber-0.5.so.0
%dir %{_libdir}/wireplumber-0.5
%dir %{_datadir}/wireplumber
%{_libdir}/girepository-1.0/Wp-0.5.typelib

%files devel
%defattr(644,root,root,755)
%{_libdir}/libwireplumber-0.5.so
%{_includedir}/wireplumber-0.5
%{_pkgconfigdir}/wireplumber-0.5.pc
%{_datadir}/gir-1.0/Wp-0.5.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libwireplumber-0.5.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/docs/html/{_images,_static,daemon,design,library,policies,resources,scripting,*.html,*.js}
%endif
