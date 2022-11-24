#!/bin/sh

PELICAN=pelican
PELICANOPTS=

BASEDIR=$(pwd)
INPUTDIR=${BASEDIR}/content
OUTPUTDIR=${BASEDIR}/output
CONFFILE=${BASEDIR}/conf_publish.py

COMMIT_MSG="Update."

${PELICAN} "${INPUTDIR}" -o "${OUTPUTDIR}" -s "${CONFFILE}" ${PELICANOPTS} && \
    ghp-import -p -b gh-pages -m "${COMMIT_MSG}" "${OUTPUTDIR}"
