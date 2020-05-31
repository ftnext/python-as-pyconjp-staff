Slack Slash Command to copy the specified file in Google Drive.  
Execute at AWS Lambda.

## Requirements

- API Gateway (POST endpoint)
- Lambda layer: installed [operate_drive](https://github.com/ftnext/diy-googledrive-operate) package
- cerdentials of Drive API
  - `my_client_secrets.json`
  - `saved_credentials.json`

### file replacement

at Lambda console (from browser)

```
.
├── lambda_function.py
├── my_client_secrets.json
├── saved_credentials.json
└── settings.yaml
```

### API Gateway configuration

Mapping template

```
{
    "method": "$context.httpMethod",
    "body" : $input.json('$'),
    "headers": {
        #foreach($param in $input.params().header.keySet())
        "$param": "$util.escapeJavaScript($input.params().header.get($param))"
        #if($foreach.hasNext),#end
        #end
    }
}
```
