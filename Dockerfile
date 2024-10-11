# PYTHON.
FROM python:3.12.7

# Enable Virtual Environment.
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Upgrade pip.
RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip

# Install pip dependencies.
COPY docker/pip_install.txt pip_install.txt
RUN pip install -r pip_install.txt

# Updgrade pip dependencies.
COPY docker/pip_upgrade.txt pip_upgrade.txt
RUN pip install -r pip_upgrade.txt --upgrade 

# Copy the app.
WORKDIR /code
COPY . /code