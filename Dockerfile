FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install base dependencies and python
RUN apt update && apt install -y \
  curl git unzip zip wget build-essential \
  python3 python3-pip python3-venv \
  ca-certificates gnupg lsb-release

# Install Node.js (LTS)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt install -y nodejs

# Install Go via longsleep PPA
RUN apt install -y software-properties-common && \
    add-apt-repository -y ppa:longsleep/golang-backports && \
    apt update && \
    apt install -y golang-go

# Install Deno
RUN curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh && \
    ln -s /usr/local/bin/deno /usr/bin/deno

# Install Bun
RUN curl -fsSL https://bun.sh/install | bash && \
    mv /root/.bun/bin/bun /usr/local/bin

# Install PHP + Composer
RUN apt-get install -y php php-xml php-mbstring php-curl && \
    curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Install java 25 via openjdk-r/ppa PPA
RUN add-apt-repository -y ppa:openjdk-r/ppa && \
    apt update && \
    apt install -y openjdk-25-jdk

# Install Dotnet 9.0 via dotnet/backports
RUN add-apt-repository -y ppa:dotnet/backports && \
    apt update && \
    apt-get install -y dotnet-sdk-9.0

# Install Ruby
RUN apt-get install -y ruby-full libyaml-dev
    
# Install wrk
RUN apt-get install -y wrk

# Create working directory
WORKDIR /app
COPY . .

# Pre-setup everything
RUN chmod +x *.sh */start.sh */install.sh && ./benchmark_presetup.sh

ENTRYPOINT ["./benchmark_runner.sh"]
