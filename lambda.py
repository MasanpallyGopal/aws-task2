import json
import boto3
import time

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Product3')


def lambda_handler(event, context):
    if event['operation'] == 'addProduct':
        return saveProduct(event)
    elif event['operation'] == 'listProduct':
        return getProducts()
    elif event['operation'] == 'updateProduct':
        return updateProduct(event)
    elif event['operation'] == 'deleteProduct':
        return deleteProduct(event)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid operation')
        }

def saveProduct(event):
    gmt_time = time.gmtime()
    now = time.strftime('%a, %d %b %Y %H:%M:%S', gmt_time)

    table.put_item(
        Item={
            'ProductCode': event['productCode'],
            'price': event['price'],
            'createdAt': now
        })

    return {
        'statusCode': 200,
        'body': json.dumps('Product with ProductCode : ' + event['productCode'] + ' created at ' + now)
    }

def getProducts():
    response = table.scan()
    items = response['Items']
    print(items)

    return {
        'statusCode': 200,
        'body': json.dumps(items),
        'headers': {
            'Content-Type': 'application/json',
        }
    }

def updateProduct(event):
    gmt_time = time.gmtime()
    now = time.strftime('%a, %d %b %Y %H:%M:%S', gmt_time)

    table.update_item(
        Key={
            'ProductCode': event['productCode']
        },
        UpdateExpression='SET price = :price, createdAt = :updatedAt',
        ExpressionAttributeValues={
            ':price': event['price'],
            ':updatedAt': now
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Product with ProductCode : ' + event['productCode'] + ' updated at ' + now)
    }

def deleteProduct(event):
    result = table.delete_item(
        Key={
            'ProductCode': event['productCode']
        }
    )
    
    print(result)

    return {
        'statusCode': 200,
        'body': json.dumps('Product with ProductCode : ' + event['productCode'] + ' deleted')
    }
