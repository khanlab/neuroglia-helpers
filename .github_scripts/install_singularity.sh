export SINGULARITY_VERSION=3.5.2 GO_VERSION=1.13 OS=linux ARCH=amd64

# install development tools and libraries
sudo apt-get update && sudo apt-get install -y \
build-essential \
libssl-dev \
uuid-dev \
libgpgme11-dev \
squashfs-tools \
libseccomp-dev \
wget \
curl \
pkg-config \
git \
cryptsetup

# install go
curl -O -L --retry 5 https://dl.google.com/go/go$GO_VERSION.$OS-$ARCH.tar.gz && \
sudo tar -C /usr/local -xzvf go$GO_VERSION.$OS-$ARCH.tar.gz && \
rm go$GO_VERSION.$OS-$ARCH.tar.gz

echo 'export PATH=/usr/local/go/bin:$PATH' >> ~/.bashrc && \
source ~/.bashrc

# install singularity
curl -O -L --retry 5 https://github.com/sylabs/singularity/releases/download/v${SINGULARITY_VERSION}/singularity-${SINGULARITY_VERSION}.tar.gz && \
tar -xzf singularity-${SINGULARITY_VERSION}.tar.gz && \
cd singularity

./mconfig && \
make -C builddir && \
sudo make -C builddir install

