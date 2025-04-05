FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    wget git cmake \
    build-essential libfreetype6-dev \
    libfontconfig1-dev \
    libspiro-dev \
    libcairo2-dev libpango1.0-dev \
    libglib2.0-dev libopenjp2-7-dev \
    default-jre-headless && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pdf2htmlEX
RUN wget https://github.com/pdf2htmlEX/pdf2htmlEX/releases/download/v0.18.8.rc1/pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-focal-x86_64.deb \
    && apt-get update \
    && apt-get install -y ./pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-focal-x86_64.deb \
    && rm ./pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-focal-x86_64.deb \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install development packages for hot reloading
RUN pip3 install --no-cache-dir watchdog flask-debugtoolbar

# Create directories for data
RUN mkdir -p /data/uploads /data/output

# Expose port
EXPOSE 9000

# Run the application in development mode with auto-reloading
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=9000", "--reload", "--debugger"]
