FROM mambaorg/micromamba:latest

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /environment.yml

RUN micromamba install -y -n base -f /environment.yml && micromamba clean --all --yes

USER 0
RUN mkdir -p /src

WORKDIR /src
