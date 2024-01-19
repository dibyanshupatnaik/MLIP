from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from dotenv import load_dotenv
import os
import time

load_dotenv()
endpoint = os.getenv('ENDPOINT')
key = os.getenv('KEY')

endpoint = "https://mlip-lab1-dib.cognitiveservices.azure.com/"
key = "6823a57c8ff143bb92779ad2980290c0"

credentials = CognitiveServicesCredentials(key)

client = ComputerVisionClient(
    endpoint=endpoint,
    credentials=credentials
)


def read_image(uri):
    numberOfCharsInOperationId = 36
    maxRetries = 10

    print("before sdk call")
    # SDK call
    rawHttpResponse = client.read(uri, language="en", raw=True)
    print(rawHttpResponse.headers)

    # Get ID from returned headers
    operationLocation = rawHttpResponse.headers["Operation-Location"]
    idLocation = len(operationLocation) - numberOfCharsInOperationId
    operationId = operationLocation[idLocation:]

    # SDK call
    result = client.get_read_result(operationId)

    # Try API
    retry = 0

    while retry < maxRetries:
        if result.status.lower() not in ['notstarted', 'running']:
            break
        time.sleep(1)
        result = client.get_read_result(operationId)

        retry += 1

    if retry == maxRetries:
        return "max retries reached"

    if result.status == OperationStatusCodes.succeeded:
        res_text = " ".join(
            [line.text for line in result.analyze_result.read_results[0].lines])
        return res_text
    else:
        return "error"
