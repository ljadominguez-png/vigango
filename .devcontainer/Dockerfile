FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install core tools & Java 17
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    git \
    unzip \
    xz-utils \
    zip \
    libglu1-mesa \
    openjdk-17-jdk \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
ENV ANDROID_HOME="/opt/android-sdk"
ENV ANDROID_CMDLINE_TOOLS="${ANDROID_HOME}/cmdline-tools/latest"
ENV FLUTTER_HOME="/usr/local/flutter"
ENV PATH="${PATH}:${JAVA_HOME}/bin:${ANDROID_CMDLINE_TOOLS}/bin:${ANDROID_HOME}/platform-tools:${FLUTTER_HOME}/bin"

# Install Android SDK CLI & API tools
ARG CMDLINE_VERSION="11076708_latest"
RUN mkdir -p ${ANDROID_CMDLINE_TOOLS} && \
    curl -fsSL https://dl.google.com/android/repository/commandlinetools-linux-${CMDLINE_VERSION}.zip -o /tmp/cmdline.zip && \
    unzip -q /tmp/cmdline.zip -d /tmp/cmdline && \
    mv /tmp/cmdline/cmdline-tools/* ${ANDROID_CMDLINE_TOOLS}/ && \
    rm -rf /tmp/cmdline /tmp/cmdline.zip

RUN yes | sdkmanager --licenses && \
    sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

# Install Flutter SDK (3.27.1 stable)
ARG FLUTTER_VERSION="3.27.1"
RUN git clone -b ${FLUTTER_VERSION} https://github.com/flutter/flutter.git ${FLUTTER_HOME} && \
    git config --global --add safe.directory ${FLUTTER_HOME}

# Configure Flutter & accept Android licenses
RUN flutter config --no-analytics && \
    flutter config --android-sdk ${ANDROID_HOME} && \
    yes | flutter doctor --android-licenses && \
    flutter doctor

WORKDIR /workspace