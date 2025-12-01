FROM odoo:19.0

USER root

COPY --chown=odoo:odoo ./requirements.txt /tmp/

RUN apt-get update \
    && apt-get install -y git gcc swig python3-m2crypto unzip curl python3-venv \
    && curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3 get-pip.py --break-system-packages --ignore-installed\
    && rm get-pip.py

RUN pip install setuptools==69.0.3 wheel --break-system-packages
RUN pip install -r /tmp/requirements.txt --break-system-packages

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]
