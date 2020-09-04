#!/usr/bin/env bash
set -eu

usage() {
  echo "Usage: $0 -p <python_package> -l <layer_zip_file_name>" 1>&2
  echo "" 1>&2
  echo "Create a zip file for Lambda layers in _build_ dir from the specified package." 1>&2
  echo "" 1>&2
  echo "-p: Specify Python package in PyPI or open git repository. Required" 1>&2
  echo "-l: Specify created zip file name. Required" 1>&2
  echo "-x: Be verbose." 1>&2
  echo "-h: Show this help message." 1>&2
  exit 1
}

if [ "$1" = '--help' -o "$1" = '-help' ]; then
  usage
fi

LAYER_FACTORY_DOCKER_IMAGE="aws-lambda-python38:1.0"
CONTAINER_NAME="layer_factory"

DEST_DIR="build"

while getopts l:p:xh OPT
do
  case $OPT in
    "l" ) LAYER_ZIP_FILE=$OPTARG
      ;;
    "p" ) PACKAGE=$OPTARG
      ;;
    "x" ) set -x
      ;;
    "h" ) usage
      ;;
    *   ) usage
      ;; 
  esac
done

shift `expr $OPTIND - 1`

if [ "${LAYER_ZIP_FILE}" = "" -o "${PACKAGE}" = "" ]; then
  usage
fi

mkdir -p ${DEST_DIR}

docker run --name ${CONTAINER_NAME} ${LAYER_FACTORY_DOCKER_IMAGE} ${PACKAGE} 
docker cp ${CONTAINER_NAME}:/var/task/python_layer.zip ${DEST_DIR}/${LAYER_ZIP_FILE}
docker rm ${CONTAINER_NAME}
