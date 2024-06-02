import boto3


def extract_query_answers(response):
    query_answers = {}
    for block in response['Blocks']:
        print(block)  # Add this line to inspect the block structure
        if block['BlockType'] == 'QUERY_RESULT':
            if 'Query' in block and 'Text' in block:
                query_text = block['Query']['Text']
                answer_text = block['Text']
                query_answers[query_text] = answer_text
            elif 'Text' in block:  # Fallback if 'Query' is not in block
                answer_text = block['Text']
                query_answers['Unknown Query'] = answer_text
    return query_answers


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
                                             {'Text': 'How much is the work experience of the candidate?'}
                                         ]})

    # Extract and print the query answers
    query_answers = extract_query_answers(response)
    for query, answer in query_answers.items():
        print(f'Query: {query}\nAnswer: {answer}')

# Exceptions handling
except Exception as e:
    print(f"Error: {e}")
