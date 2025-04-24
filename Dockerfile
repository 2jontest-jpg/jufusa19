FROM odoo:15.0

USER odoo


COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
RUN rm /requirements.txt

USER odoo
