import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import PyPDFLoader


load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.1-70b-versatile')

# COMO O BOT IRÁ RESPONDER
def resposta_bot(mensagens, documento):
  message_system = '''Você é um assistente amigável chamado FirminoBot que utiliza as seguintes informações para formular as suas respostas: {informacoes}.
  '''
  mensagens_modelo = [('system', message_system)]
  mensagens_modelo += mensagens
  template = ChatPromptTemplate.from_messages(mensagens_modelo)
  chain = template | chat
  return chain.invoke({'informacoes': documento}).content



def carrega_site():
  url_site = input('Digite a url do site: ')
  loader = WebBaseLoader(url_site)
  documentos_site = loader.load()

  documento = ''
  for doc in documentos_site:
    documento += doc.page_content
  return documento

def carrega_pdf():
  caminho = input('Digite o caminho do pdf: ')
  loader = PyPDFLoader(caminho)
  lista_documentos = loader.load()
  documento = ''
  for doc in lista_documentos:
    documento = documento + doc.page_content
  return documento

def carrega_youtube():
  url_youtube = input('Digite a url do vídeo: ')
  loader = YoutubeLoader.from_youtube_url(url_youtube, language=['pt'])
  lista_documentos = loader.load()
  documento = ''
  for doc in lista_documentos:
    documento = documento + doc.page_content
  return documento



print('\nBem-vindo ao FirminoBot\n')

# SELEÇÃO PARA O USUÁRIO DECIDIR O QUE ELE VAI QUERER USAR
texto_selecao = '''Digite 1 se você quiser conversar com um site.
Digite 2 se você quiser conversar com um PDF.
Digite 3 se você quiser conversar com um video do Youtube.
'''

while True:

  selecao = input(texto_selecao)
  if selecao == '1':
    documento = carrega_site()
    break
  if selecao == '2':
    documento = carrega_pdf()
    break
  if selecao == '3':
    documento = carrega_youtube()
    break
  print('Digite um valor entre 1 e 3.')



mensagens = []
while True:
  pergunta = input('Usuario: ')
  if pergunta.lower() == 'x':
    break
  mensagens.append(('user', pergunta))
  resposta = resposta_bot(mensagens, documento)
  mensagens.append(('assistant', resposta))
  print(f'\nBot: {resposta}\n')

print('\nMuito obrigado por usar o FirminoBot')
