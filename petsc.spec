Name:           petsc
Version:        3.6.2
Release:        1%{?dist}
Summary:        Portable, Extensible Toolkit for Scientific Computation

License:        BSD
URL:            http://www.mcs.anl.gov/petsc/
Source0:        http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  python
BuildRequires:  gcc gcc-c++
BuildRequires:  openmpi-devel
BuildRequires:  mpich-devel
BuildRequires:  netcdf-cxx4-devel netcdf-cxx4-openmpi-devel netcdf-cxx4-mpich-devel
# -fortran-openmpi/mpich-devel
BuildRequires:  netcdf-devel netcdf-openmpi-devel netcdf-mpich-devel
BuildRequires:  hdf5-devel hdf5-openmpi-devel hdf5-mpich-devel
BuildRequires:  fftw-devel
BuildRequires:  ocl-icd-devel
BuildRequires:  papi-devel
BuildRequires:  SuperLU-devel
#BuildRequires:  ptscotch-openmpi/mpich-devel
#BuildRequires:  scalapack-openmpi/mpich-devel
#BuildRequires:  MUMPS-devel MUMPS-openmpi-devel MUMPS-mpich-devel
# -openmpi/mpich-devel
BuildRequires:  boost-devel
BuildRequires:  sundials-devel sundials-openmpi-devel
BuildRequires:  openssl-devel
BuildRequires:  cgnslib-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  valgrind-devel
BuildRequires:  libAfterImage-devel
BuildRequires:  libyaml-devel

%description
PETSc, pronounced PET-see (the S is silent), is a suite of data structures
and routines for the scalable (parallel) solution of scientific applications
modeled by partial differential equations. It supports MPI, and GPUs through
CUDA or OpenCL, as well as hybrid MPI-GPU parallelism.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -c

sed -i -e "/self.destLibDir/s/lib/%{_lib}/" %{name}-%{version}/config/install.py

%build

%define dobuild() \
cp -a %{name}-%{version} $MPI_COMPILER; \
cd $MPI_COMPILER; \
%{__python} configure \\\
  --with-cc=$CC                      \\\
  --with-cxx=$CXX                    \\\
  --with-fc=$FC                      \\\
  --CFLAGS="%{optflags}" --CXXFLAGS="%{optflags}" --FFLAGS="%{optflags} -I%{_fmoddir}" --LDFLAGS="%{__global_ldflags}" \\\
  --prefix=%{_prefix}                \\\
  %if 0%{?__isa_bits} == 64 \
    --with-64-bit-indices=0          \\\
  %endif \
  --with-threadsafety=1 --with-log=0 \\\
  --with-fortran-kernels=1           \\\
  --with-shared-libraries=1          \\\
  --with-proc-filesystem=1           \\\
  --with-large-file-io=1             \\\
  --with-mpi=$WITH_MPI               \\\
  --with-mpi-compilers=$MPI_COMPILER \\\
  --with-netcdf-cxx=$WITH_MPI        \\\
  --with-hdf5=$WITH_MPI              \\\
  --with-netcdf=$WITH_MPI            \\\
  --with-viennacl=0                  \\\
  --with-opencl=1                    \\\
  --with-papi=0                   \\\
  --with-parmetis=0                  \\\
  --with-metis=0                     \\\
  --with-tetgen=0                    \\\
  --with-trilinos=0                  \\\
  --with-superlu=0                \\\
  --with-ptscotch=0               \\\
  --with-scalapack=0              \\\
  --with-mumps=0                  \\\
  --with-boost=1                     \\\
  --with-sundials=${WITH_SUNDIALS:0} \\\
  --with-scientificpython=0       \\\
  --with-suitesparse=0               \\\
  --with-mpi4py=0                 \\\
  --with-numpy=0                  \\\
  --with-ssl=1                       \\\
  --with-cgns=0                   \\\
  --with-fiat=0                      \\\
  --with-opengles=0               \\\
  --with-ctetgen=0                \\\
  --with-pthread=1                   \\\
  --with-yaml=1                      \\\
  --with-valgrind=1                  \\\
  --with-afterimage=0             \\\
  ; \
make MAKE_NP=$RPM_BUILD_NCPUS V=1 ; \
cd ..

MPI_COMPILER=serial MPI_SUFFIX= WITH_MPI=0 CC=%__cc CXX=%__cxx FC=gfortran %dobuild

# Build OpenMPI version
#{_openmpi_load}
#WITH_MPI=1 WITH_SUNDIALS=1 CC=mpicc CXX=mpicxx FC=mpif90 #dobuild
#{_openmpi_unload}

# Build mpich version
#{_mpich_load}
#WITH_MPI=1 CC=mpicc CXX=mpicxx FC=mpif90 #dobuild
#{_mpich_unload}

%install
make install DESTDIR=%{buildroot}%{_prefix} -C serial

find %{buildroot}

mv %{buildroot}%{_prefix}/lib/* %{buildroot}%{_libdir}/

rm -f %{buildroot}%{_libdir}/%{name}/conf/*.log

%check
make test -C serial

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libidr}/lib%{name}.so.*

%files devel
%{_libidr}/lib%{name}.so

%changelog
* Sat Nov 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.6.2-1
- Initial package
