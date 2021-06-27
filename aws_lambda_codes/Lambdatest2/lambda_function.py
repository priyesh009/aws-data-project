import json

def lambda_handler(event, context):
    test = []
    for i in range(0,10):
        print(i)
        test.append(i)
    print(test)
    print('its working Jyotsna 2')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Jyotsna!')
    }