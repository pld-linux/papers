Summary:	Document viewer for multiple document formats
Summary(pl):	Przeglądarka dokumentów w wielu formatach
Name:		evince
Version:	0.3.4
Release:	0.2
License:	GPL v2
Group:		X11/Applications/Graphics
Source0:	http://ftp.gnome.org/pub/gnome/sources/evince/0.3/%{name}-%{version}.tar.bz2
# Source0-md5:	2c3177f60e6d8ed0b73168ebf9f726a5
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-gs8.patch
Patch2:		%{name}-disable_dbus.patch
URL:		http://www.gnome.org/projects/evince/
BuildRequires:	GConf2-devel >= 2.10.0
BuildRequires:	autoconf
BuildRequires:	automake
#BuildRequires:	dbus-glib-devel >= 0.33
BuildRequires:	djvulibre-devel >= 3.5.15
BuildRequires:	ghostscript
BuildRequires:	gnome-doc-utils >= 0.3.2
BuildRequires:	gnome-vfs2-devel >= 2.10.0-2
BuildRequires:	gtk+2-devel >= 2:2.6.4
BuildRequires:	intltool
BuildRequires:	kpathsea-devel
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libgnomeprintui-devel >= 2.10.0
BuildRequires:	libgnomeui-devel >= 2.10.0-2
BuildRequires:	libstdc++-devel
BuildRequires:	nautilus-devel
BuildRequires:	pkgconfig
BuildRequires:	poppler-glib-devel >= 0.4.0
BuildRequires:	rpmbuild(macros) >= 1.197
Requires(post,preun):	GConf2
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Evince is a document viewer for multiple document formats like pdf,
postscript, and many others. The goal of evince is to replace the
multiple document viewers that exist on the GNOME Desktop, like ggv,
gpdf, and xpdf with a single simple application.

%description -l pl
Evince jest przeglądarką dokumentów w wielu formatach takich jak pdf,
postscript i wielu innych. W zamierzeniach program ma zastąpić
przeglądarki dokumentów dla środowiska GNOME, takie jak ggv, gpdf i
xpdf jedną prostą aplikacją.

%package -n nautilus-extension-evince
Summary:	Evince extension for Nautilus
Summary(pl):	Rozszerzenie Evince dla Nautilusa
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus

%description -n nautilus-extension-evince
Evince extension for Nautilus.

%description -n nautilus-extension-evince -l pl
Rozszerzenie Evince dla Nautilusa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
gnome-doc-prepare --copy --force
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	--disable-schemas-install \
	--enable-djvu \
	--enable-dvi \
	--enable-nautilus \
	--enable-pixbuf \
	--enable-t1lib \
	--enable-tiff
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no
rm -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-1.0/*.la

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install evince-thumbnailer-djvu.schemas
%gconf_schema_install evince-thumbnailer-dvi.schemas
%gconf_schema_install evince-thumbnailer.schemas
%gconf_schema_install evince.schemas
%update_desktop_database_post
%scrollkeeper_update_post

%preun
%gconf_schema_uninstall evince-thumbnailer-djvu.schemas
%gconf_schema_uninstall evince-thumbnailer-dvi.schemas
%gconf_schema_uninstall evince-thumbnailer.schemas
%gconf_schema_uninstall evince.schemas

%postun
%update_desktop_database_postun
%scrollkeeper_update_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/evince-thumbnailer-djvu.schemas
%{_sysconfdir}/gconf/schemas/evince-thumbnailer-dvi.schemas
%{_sysconfdir}/gconf/schemas/evince-thumbnailer.schemas
%{_sysconfdir}/gconf/schemas/evince.schemas
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_omf_dest_dir}/evince

%files -n nautilus-extension-evince
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-1.0/*.so*
