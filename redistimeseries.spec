# Experimental redis-timeseris rpm package
#
# Based on work by Remi Collet

%global redis_modules_dir %{_libdir}/redis/modules
%global redis_modules_cfg %{_sysconfdir}/redis/modules
%global cfgname          timeseries.conf
%global libname          redistimeseries.so
# Github forge
%global gh_vend          RedisTimeSeries
%global gh_proj          RedisTimeSeries
%global forgeurl         https://github.com/%{gh_vend}/%{gh_proj}
#global commit           e7f73647352fa754b1885d34330879c10e681c9f
%global tag              v%{version}
# for EL-8 to avoid TAG usage
%global archivename      %{gh_proj}-%{version}

Name:              redistimeseries
Version:           8.6.0
Release:           4%{?dist}
Summary:           Time series as native data type
# Starting with Redis 8, RedisTimeSeries is licensed under your choice of:
# (i) Redis Source Available License 2.0 (RSALv2);
# (ii) the Server Side Public License v1 (SSPLv1); or
# (iii) the GNU Affero General Public License version 3 (AGPLv3).
# LibMR is AGPL-3.0-only
# hiredis is BSD-3-Clause
# libevent is BSD-3-Clause
# RedisModulesSDK is MIT
# readies is BSD-3-Clause
# cpu_features is Apache-2.0
# dragonbox is Apache-2.0
# fast_double_parser is Apache-2.0
# minunit is MIT
License:           AGPL-3.0-only AND MIT AND BSD-3-Clause AND Apache-2.0
URL:               %{forgeurl}
Source0:           https://github.com/Peter-Sh/redistimeseries-rpm/releases/download/v8.6.0/redistimeseries-8.6.0.tar.gz
Source1:           timeseries.conf

BuildRequires:     make
BuildRequires:     cmake
BuildRequires:     automake
BuildRequires:     autoconf
BuildRequires:     libtool
BuildRequires:     gcc
BuildRequires:     gcc-c++
BuildRequires:     python3
BuildRequires:     python3-pip
BuildRequires:     openssl-devel
BuildRequires:     jq

Provides:          bundled(LibMR)
Provides:          bundled(hiredis)
Provides:          bundled(libevent)
Provides:          bundled(RedisModulesSDK)
Provides:          bundled(cpu_features)
Provides:          bundled(fast_double_parser)
Provides:          bundled(readies)
Provides:          bundled(dragonbox)
Provides:          bundled(minunit)

Requires:          redis = %{version}
Supplements:       redis


%description
RedisTimeSeries can hold multiple time series. Each time series is accessible
via a single Redis key (similar to any other Redis data structure).


%prep
%setup -q -n %{gh_proj}-%{version}

: Configuration file
{ printf '# %{gh_proj}\nloadmodule %{redis_modules_dir}/%{libname}\n\n'; cat %{SOURCE1}; } > %{cfgname}

cp -p deps/LibMR/LICENSE.txt           LICENSE.LibMR              # AGPLv3
cp -p deps/RedisModulesSDK/LICENSE     LICENSE.RedisModulesSDK    # MIT
cp -p deps/cpu_features/LICENSE        LICENSE.cpu_features       # Apache-2.0
cp -p deps/readies/LICENSE             LICENSE.readies            # BSD-3-Clause
cp -p deps/fast_double_parser/LICENSE  LICENSE.fast_double_parser # Apache-2.0
cp -p deps/LibMR/deps/hiredis/COPYING  LICENSE.hiredis            # BSD-3-Clause
cp -p deps/LibMR/deps/libevent/LICENSE LICENSE.libevent           # BSD-3-Clause
chmod 0644 LICENSE.*


%build
%global make_flags  DEBUG="" VERBOSE=1 LDFLAGS="%{?__global_ldflags}" CFLAGS+="%{optflags} -fPIC"
make %{?_smp_mflags} %{make_flags} build


%check
test -f bin/linux-*-release/%{libname}


%install
install -Dpm755 bin/linux-*-release/%{libname} %{buildroot}%{redis_modules_dir}/%{libname}
install -Dpm644 %{cfgname}                     %{buildroot}%{redis_modules_cfg}/%{cfgname}


%files
%license LICENSE.*
%license licenses/AGPLv3.txt
%doc *.md
%attr(0644, root, root) %config(noreplace) %{redis_modules_cfg}/%{cfgname}
%{redis_modules_dir}/%{libname}


%changelog
* Tue Mar 31 2026 Petar Shtuchkin <petar.shtuchkin@redis.com> - 8.6.0-4
- initial experimental 8.6.0
