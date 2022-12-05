# include limits header
%global commit0 0bbf78789b3a52677453128755f9c1ab3051c250
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20221121

%bcond_with check
%bcond_with pocl

Summary:        An automatic OpenCL & CUDA kernel tuner
Name:           CLTune
License:        Apache-2.0
Version:        2.7.0
Release:        1.%{?date0}git%{?shortcommit0}%{?dist}

URL:            https://cnugteren.github.io/cltune/cltune.html
Source0:        https://github.com/CNugteren/CLTune/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Patch0:         0001-Version-the-shared-library.patch
Patch1:         0002-Silence-OpenCL-version-warning.patch
Patch2:         0003-Improve-install-location-handling.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  ocl-icd-devel
%if %{with pocl}
BuildRequires:  pocl
%endif

%description
CLTune is a C++ library which can be used to automatically tune your
OpenCL and CUDA kernels. The only thing you'll need to provide is a
tuneable kernel and a list of allowed parameters and values.

For example, if you would perform loop unrolling or local memory tiling
through a pre-processor define, just remove the define from your kernel
code, pass the kernel to CLTune and tell it what the name of your
parameter(s) are and what values you want to try. CLTune will take care
of the rest: it will iterate over all possible permutations, test them,
and report the best combination.

%package devel
Summary:        Headers and libraries for CLTune
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocl-icd-devel%{?_isa}

%description devel
CLTune is a C++ library which can be used to automatically tune your
OpenCL and CUDA kernels. The only thing you'll need to provide is a
tuneable kernel and a list of allowed parameters and values.

For example, if you would perform loop unrolling or local memory tiling
through a pre-processor define, just remove the define from your kernel
code, pass the kernel to CLTune and tell it what the name of your
parameter(s) are and what values you want to try. CLTune will take care
of the rest: it will iterate over all possible permutations, test them,
and report the best combination.

%prep
%autosetup -p1 -n %{name}-%{commit0}

%build
%cmake \
       -DSAMPLES=OFF \
%if %{with check}
       -DTESTS=ON
%endif
%cmake_build

%install
%cmake_install

mkdir -p %{buildroot}%{_datadir}/%{name}/samples
cp -pr samples/* %{buildroot}%{_datadir}/%{name}/samples
cp -p LICENSE %{buildroot}%{_datadir}/%{name}
cp -p README.md %{buildroot}%{_datadir}/%{name}

%if %{with check}
%check
%ctest
%endif

%files
%dir %{_datadir}/%{name}
%license %{_datadir}/%{name}/LICENSE
%doc %{_datadir}/%{name}/README.md
%{_libdir}/libcltune.so.2
%{_libdir}/libcltune.so.%{version}

%files devel
%{_includedir}/cltune.h
%{_libdir}/libcltune.so
%{_libdir}/pkgconfig/cltune.pc
%{_datadir}/%{name}/samples

%changelog
* Mon Dec 5 2022 Tom Rix <trix@redhat.com> - 2.7.0-1.20221121git0bbf787
- Initial package
