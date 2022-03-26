%global debug_package %{nil}

%global __strip /bin/true

%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
%global __spec_install_post \
    /usr/lib/rpm/check-rpaths \
    /usr/lib/rpm/check-buildroot \
    /usr/lib/rpm/brp-compress

%undefine _build_create_debug
%define __arch_install_post export NO_BRP_STRIP_DEBUG=true NO_BRP_AR=true

Name: llvm-13
Epoch: 100
Version: 13.0.1
Release: 1%{?dist}
Summary: Modular compiler and toolchain technologies
License: NCSA
URL: https://github.com/llvm/llvm-project/tags
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
BuildRequires: ninja
%else
BuildRequires: ninja-build
%endif
%if 0%{?centos_version} == 700
BuildRequires: devtoolset-11-gcc
BuildRequires: devtoolset-11-gcc-c++
%else
BuildRequires: gcc
BuildRequires: gcc-c++
%endif
BuildRequires: binutils-devel
BuildRequires: cmake
BuildRequires: fdupes
BuildRequires: libffi-devel
BuildRequires: libxml2-devel
BuildRequires: ncurses-devel
BuildRequires: pkgconfig
BuildRequires: procps
BuildRequires: python-rpm-macros
BuildRequires: python3-devel
BuildRequires: zlib-devel
Provides: llvm = %{epoch}:%{version}-%{release}
Provides: llvm-13-devel = %{epoch}:%{version}-%{release}
Conflicts: llvm < %{epoch}:%{version}-%{release}

%description
LLVM is a collection of libraries and tools that make it easy to build
compilers, optimizers, just-in-time code generators, and many other
compiler-related programs.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%if 0%{?centos_version} == 700
source /opt/rh/devtoolset-11/enable && \
%endif
%cmake \
    -DBUILD_SHARED_LIBS:BOOL=OFF \
    -DCLANG_ENABLE_ARCMT:BOOL=OFF \
    -DCLANG_ENABLE_STATIC_ANALYZER:BOOL=OFF \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_libdir}/llvm-13 \
    -DCMAKE_SKIP_RPATH:BOOL=ON \
    -DCOMPILER_RT_BUILD_SANITIZERS:BOOL=OFF \
    -DCOMPILER_RT_BUILD_XRAY:BOOL=OFF \
    -DENABLE_LINKER_BUILD_ID=ON \
    -DLLVM_BUILD_DOCS:BOOL=OFF \
    -DLLVM_BUILD_EXAMPLES:BOOL=OFF \
    -DLLVM_BUILD_LLVM_DYLIB:BOOL=OFF \
    -DLLVM_BUILD_TESTS:BOOL=OFF \
    -DLLVM_BUILD_TOOLS:BOOL=OFF \
    -DLLVM_BUILD_UTILS:BOOL=OFF \
    -DLLVM_ENABLE_ASSERTIONS=OFF \
    -DLLVM_INSTALL_TOOLCHAIN_ONLY:BOOL=OFF \
    -DLLVM_LINK_LLVM_DYLIB:BOOL=OFF \
    -DLLVM_PARALLEL_COMPILE_JOBS=1 \
    -DLLVM_PARALLEL_LINK_JOBS=1 \
    -DLLVM_POLLY_BUILD:BOOL=OFF \
    -DLLVM_TARGETS_TO_BUILD=Native \
    -DLLVM_TOOL_CLANG_TOOLS_EXTRA_BUILD:BOOL=OFF \
    llvm
%cmake_build

%install
%cmake_install
ln -fs %{_libdir}/llvm-13/bin/* %{buildroot}%{_bindir}
%fdupes -s %{buildroot}

%check

%files
%license LICENSE
%dir %{_libdir}/llvm-13
%{_bindir}/*
%{_libdir}/llvm-13/*

%changelog
