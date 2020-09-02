#!/usr/bin/env bash

set -e

SCRIPT_DIR=$(cd $(dirname $0); pwd)

usage() {
  echo "Usage: $0 -n <lambda_function_name> -r <role_arn> -l <layer_arn> [-l <layer_arn>] -e <env_var_pair> [-e <env_var_pair>] [-- --profile foo]" 1>&2
  echo "" 1>&2
  echo "Deploy AWS Lambda function which can read/write Google spreadsheet and post to Slack." 1>&2
  echo "" 1>&2
  echo "-n: Specify name of the Lambda function. Required" 1>&2
  echo "-r: Specify ARN of role for the Lambda function. Required" 1>&2
  echo "-l: Specify ARN of layer for the Lambda function. Required at least one" 1>&2
  echo "-e: Specify environment variable as key=value format. Required at least one" 1>&2
  echo "-x: Be verbose." 1>&2
  echo "-h: Show this help message." 1>&2
  echo "" 1>&2
  echo "Use -- to pass other parameters (profile, region, ...) to aws-cli." 1>&2
  exit 1
}

if [ "$1" = "--help" -o "$1" = "-help" ]; then
  usage
fi

LAYER_ARNS=()
ENVIRONMENT_VARIABLES=()

while getopts n:r:l:e:xh OPT
do
  case $OPT in
    "n" ) FUNCTION_NAME=$OPTARG
      ;;
    "r" ) ROLE_ARN=$OPTARG
      ;;
    "l" ) LAYER_ARNS+=($OPTARG)
      ;;
    "e" ) ENVIRONMENT_VARIABLES+=($OPTARG)
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

if [ "${FUNCTION_NAME}" = "" -o "${ROLE_ARN}" = "" ]; then
  usage
fi

if [ ${#LAYER_ARNS[@]} -eq 0 -o ${#ENVIRONMENT_VARIABLES[@]} -eq 0 ]; then
  usage
fi

ENVIRONMENT_VARIABLES_STRING=""
for env_var in ${ENVIRONMENT_VARIABLES[@]}
do
  ENVIRONMENT_VARIABLES_STRING="${env_var},${ENVIRONMENT_VARIABLES_STRING}"
done
# remove trailing comma
ENVIRONMENT_VARIABLES_STRING=$(echo ${ENVIRONMENT_VARIABLES_STRING} | sed -E 's/,$//')

# zipにフルパス分のディレクトリができないようにcdすることにした
cd ${SCRIPT_DIR}

# zipはアーカイブに追加する挙動なので、アップロードするコードが増えないように前回デプロイしたファイルを消す
rm function.zip
zip function.zip lambda_function.py

aws lambda create-function \
  --function-name ${FUNCTION_NAME} \
  --runtime python3.8 \
  --role ${ROLE_ARN} \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --timeout 10 \
  --environment Variables="{${ENVIRONMENT_VARIABLES_STRING}}" \
  --layers ${LAYER_ARNS[@]} \
  $@
