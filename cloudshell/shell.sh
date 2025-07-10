## INSIDE A CLOUD SHELL OR AWS CLI

# pull requests and schema dependencies from github

curl -LO https://github.com/mnowrouz/Conjur_IAM_Demo/releases/download/v1.0.1/lambda_layer_request.zip

# load the dependencies as a lambda layer

aws lambda publish-layer-version \
  --layer-name requests-schema-layer \
  --zip-file fileb://lambda_layer_request.zip \
  --compatible-runtimes python3.9 &&


# then go to your lambda function and attach the layer to the function (in the UI)




