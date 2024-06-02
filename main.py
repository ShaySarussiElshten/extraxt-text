import boto3


def extract_text_from_block(response):
    text = []
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':  # You can also use 'WORD' here
            if 'Text' in block:
                text.append(block['Text'])
    return text


try:
    # Configure AWS credentials
    access_key_id = ''
    secret_access_key = ''
    session = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )

    region = 'eu-west-1'

    # Configure the Amazon Textract client
    textract = session.client('textract', region_name=region)

    # Configure the Amazon S3 client
    s3 = session.client('s3', region_name=region)

    # Specify the S3 object location of the document to extract text from
    bucket_name = 's3-with-textract'
    document_key = 'resume.png'

    s3_object = s3.get_object(Bucket=bucket_name, Key=document_key)
    document_location = {'S3Object': {'Bucket': bucket_name, 'Name': document_key}}

    # Use Amazon Textract to extract text from the document
    response = textract.analyze_document(Document=document_location,
                                         FeatureTypes=['TABLES', 'FORMS', 'SIGNATURES', 'QUERIES'],
                                         QueriesConfig={'Queries': [
                                             {'Text': '{}'.format('How much is the work experience of the candidate?')}
                                         ]})

    # Extract and print the text
    text = extract_text_from_block(response)

    # Call the function which prints the response
    print('Extracted Text:', ' '.join(text))

# Exceptions handling
except Exception as e:
    print(f"Error: {e}")
