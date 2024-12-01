import boto3
import argparse
import os
import sys

# Argument parser
parser = argparse.ArgumentParser(description="Translate HTML documents using AWS Translate.")
parser.add_argument("SourceLanguageCode", help="Language code of the source document (e.g., 'en').")
parser.add_argument("TargetLanguageCode", help="Language code for the target translation (e.g., 'es').")
parser.add_argument("SourceFile", help="Path to the source file to be translated.")
args = parser.parse_args()

# Initialize AWS Translate client
translate = boto3.client('translate')

try:
    # Validate the source file
    if not os.path.exists(args.SourceFile):
        print(f"Error: File {args.SourceFile} not found.")
        sys.exit(1)

    # Read the source file
    with open(args.SourceFile, "rb") as file:
        data = file.read()

    # Call AWS Translate API
    result = translate.translate_document(
        Document={
                "Content": data,
                "ContentType": "text/html"
            },
        SourceLanguageCode=args.SourceLanguageCode,
        TargetLanguageCode=args.TargetLanguageCode
    )

    # Save the translated document
    if "TranslatedDocument" in result:
        fileName = os.path.basename(args.SourceFile)
        translated_file = f"{args.TargetLanguageCode}-{fileName}"
        with open(translated_file, 'w', encoding='utf-8') as f:
            f.write(result["TranslatedDocument"]["Content"].decode('utf-8'))

        print(f"Translated document saved as {translated_file}")
    else:
        print("Translation result did not contain a document.")

except boto3.exceptions.Boto3Error as e:
    print(f"AWS Boto3 Error: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
