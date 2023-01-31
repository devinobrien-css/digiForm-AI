# SAM for api development
Make sure you're running Node 18 for this
Also, install the dependencies in the /image directory

## Building

First, go through all sub-directories and run `npm ci` to get all dependencies.
Afterwards, in the `./sam` directory, run `sam build` to build the functions.

## Local Development

For hot reloading you can use:
```
sam local start-api -t template.yaml --skip-pull-image
```
For warmed containers you can use:
```
sam local start-api --warm-containers EAGER
```
If your default AWS profile is not the profile used for the Secrets Manager, you can use:
```
sam local start-api --profile {profile}
```

## Deploying

Once the functions have been built, you can run `sam deploy --guided`.
Assuming you have the proper credentials, it will walk you through the deployment process.

## Deletion

If for some reason you wish to delete the project, you can simply use:
```
sam delete
```

## Patterns
Use the template.yaml in the root directory to define the resource you want to make. For apis, make a folder with a handler, install your dependencies, and your off to the races.

If you're hitting lots of chop, set a longer timeout or add a higher default memory to the template.yaml in the global section

## Some notes on Dynamo SDK v3

For getting a single item:
```
    const params = {
        TableName: 'sam-app-DallEDDBTable-1Q6B6DFWCIKTX',
        Key: {
            PK: 'CHARACTER', 
            SK:  'NAME#Bravo'
        }
    }
    ...
    const data = await ddbDocClient.send(new GetCommand(params));
    ...
```