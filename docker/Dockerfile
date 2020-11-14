FROM hysds/isce2:v2.3-20200617-es1
MAINTAINER edunn "Alexander.E.Dunn@jpl.nasa.gov"
LABEL description="Stack preparation for ARIARNN flood-mapping algorithm"

ARG id
ARG gid

ENV verdi_root="/home/ops/verdi/ops"
ENV pge_root="${verdi_root}/pge"
ENV slcp2cor_root="${verdi_root}/slcp2cor"

# Install pip dependencies
RUN echo "===Installing pip dependencies==="
COPY requirements.txt $pge_root/requirements.txt
RUN /opt/conda/bin/pip install -r ${pge_root}/requirements.txt

# Install slcp2cor
RUN pushd $verdi_root \
&& git clone https://github.com/alexdunncs/slcp2cor.git $slcp2cor_root \
&& cd $slcp2cor_root/src \
&& echo $(pwd) \
&& chmod +x compile.sh \
&& ./compile.sh \
&& popd

# Copy in scripts and configuration
COPY --chown=1000:1000 . $pge_root
RUN chmod a+x ${pge_root}/run_pge.py ${pge_root}/process_frames.sh
ENV PATH=${PATH}:${pge_root}

USER root
# TODO: REMOVE NEXT LINE ONCE LOCAL TESTS ARE COMPLETE
RUN mv ${pge_root}/examples/* ${pge_root}

## These lines may be run to allow local running for fast development iteration
# git clone https://github.jpl.nasa.gov/cloud/Access-Key-Generation.git && pip install bs4 && ./Access-Key-Generation/aws-login.py
# export AWS_PROFILE="saml-pub" && run_pge.py


USER ops
CMD ["run_pge.py"]