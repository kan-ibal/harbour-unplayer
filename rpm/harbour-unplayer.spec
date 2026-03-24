Name:       harbour-unplayer
Version:    2.1.2
Release:    1
Summary:    Simple music player for Sailfish OS
Group:      Applications/Music
License:    GPLv3
URL:        https://github.com/kan-ibal/harbour-unplayer/

Source0:    https://github.com/kan-ibal/harbour-unplayer/archive/%{version}.tar.gz

Requires:      sailfishsilica-qt5
BuildRequires: pkgconfig(Qt5Concurrent)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Multimedia)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5Sql)
BuildRequires: pkgconfig(sailfishapp)
BuildRequires: pkgconfig(nemonotifications-qt5)
BuildRequires: cmake
BuildRequires: desktop-file-utils

BuildRequires: pkgconfig(mpris-qt5)
BuildRequires: pkgconfig(taglib)

# TagLib dependencies
BuildRequires: pkgconfig(zlib)
BuildRequires: boost-devel

# >> macros
%define		_binary_payload		w9.gzdio
%define		_source_payload		w9.gzdio


%define __provides_exclude mimehandler

%global debug 0

%global harbour ON
#%%global harbour OFF

%global build_directory %{_builddir}/build-%{_target}-%(version | awk '{print $3}')

%global thirdparty_install_directory %{build_directory}/3rdparty/install

%define patch_if_needed() \
%if 0%(patch -p0 -R --dry-run --force --fuzz=2 --input=%{P:%1} > /dev/null 2>&1; echo $?) != 0 \
%patch%1 \
%endif

%global apply_patches %{lua: \
for i, s in ipairs(patches) do \
    print(rpm.expand("%patch_if_needed "..(i - 1))) \
end \
}
# << macros

%description
%{summary}


%prep
%setup -q
%apply_patches
mkdir %{build_directory}

%build
export PKG_CONFIG_PATH=%{thirdparty_install_directory}/lib/pkgconfig

# Enable -O0 for debug builds
# This also requires disabling _FORTIFY_SOURCE
%if %{debug}
    export CFLAGS="${CFLAGS:-%optflags} -O0 -Wp,-U_FORTIFY_SOURCE"
    export CXXFLAGS="${CXXFLAGS:-%optflags} -O0 -Wp,-U_FORTIFY_SOURCE"
%endif

cd %{build_directory}
%cmake .. \
    -DHARBOUR=%{harbour} \
    -DQTMPRIS_STATIC=ON \
    -DTAGLIB_STATIC=ON
%make_build

%install
cd %{build_directory}
%make_install
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%files
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
