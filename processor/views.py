from django.shortcuts import render
import io
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PDFData
from PyPDF2 import PdfReader
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from rest_framework.parsers import MultiPartParser

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

STOPWORDS = set(stopwords.words('english'))


def index(request):
    return render(request, 'index.html')


@api_view(['POST'])
def upload_pdf(request):
    if 'file' not in request.FILES or 'email' not in request.data:
        return Response({"error": "Please provide a file and email."}, status=status.HTTP_400_BAD_REQUEST)

    email = request.data['email']
    file = request.FILES['file']

    # Parse PDF content
    pdf_reader = PdfReader(file)
    content = ""
    for page_num in range(len(pdf_reader.pages)):
        content += pdf_reader.pages[page_num].extract_text()

    # Tokenize and identify parts of speech
    words = word_tokenize(content)
    pos_tags = pos_tag(words)

    # Filter out nouns and verbs
    nouns = [word for word, pos in pos_tags if pos.startswith('NN') and word.lower() not in STOPWORDS]
    verbs = [word for word, pos in pos_tags if pos.startswith('VB') and word.lower() not in STOPWORDS]

    # Save the data
    pdf_data, created = PDFData.objects.update_or_create(
        email=email,
        defaults={'nouns': nouns, 'verbs': verbs}
    )

    return Response({
        "email": pdf_data.email,
        "nouns": pdf_data.nouns,
        "verbs": pdf_data.verbs,
    }, status=status.HTTP_200_OK)
