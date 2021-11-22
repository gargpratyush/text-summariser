from flask import Flask, render_template, request, redirect
import sumy
from sumy.summarizers.kl import KLSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer as Luhn
app = Flask(__name__)
app.debug = True



def luhn_summarizer(text, num):
    tokenizer = sumy.nlp.tokenizers.Tokenizer
    parser = sumy.parsers.plaintext.PlaintextParser.from_string(text, tokenizer('english'))

    summarizer = Luhn()
    summary = summarizer(parser.document, sentences_count = num)
    text = ''
    for sent in summary:
        text += str(sent)
    
    return text

def textrank_summarizer(text, num):
    parser = PlaintextParser.from_string(text,Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary =summarizer(parser.document,num)
    text_summary=""
    for sentence in summary:
        text_summary+=str(sentence)

    return text_summary

def klsum_summarizer(text, num):
    
    parser = PlaintextParser.from_string(text,Tokenizer("english"))
    summarizer_kl = KLSummarizer()
    summary =summarizer_kl(parser.document, num)
    kl_summary=""
    for sentence in summary:
        kl_summary+=str(sentence)  
    return kl_summary

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/form", methods=["POST"])
def form():
    text = request.form.get("input_text")
    method = request.form.get("methods")
    num = request.form.get("num")
    summary = ''
    if method == 'luhn':
        summary = luhn_summarizer(text, num)
        method = 'Luhn Summarizer'
    if method == 'textrank':
        summary = textrank_summarizer(text, num)
        method = 'TextRank Summarizer'
    if method == 'klsum':
        summary = klsum_summarizer(text, num)
        method = 'KL-Sum Summarizer'

    return render_template('summary.html', summary = summary, method = method)
    