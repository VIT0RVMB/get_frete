# -*- coding:utf-8-*-
import requests
import re
from bs4 import BeautifulSoup as bs
import timeit
import json

str_request='http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?nCdEmpresa=#codigo_empresa#&sDsSenha=#senha#&nCdServico=#codigo_servico#&sCepOrigem=#cep_origem#&sCepDestino=#cep_destino#&nVlPeso=#peso#&nCdFormato=1&nVlComprimento=#comprimento#&nVlLargura=#largura#&nVlAltura=#altura#&nVlDiametro=0&sCdMaoPropria=#mao_propria#&nVlValorDeclarado=#valor_declarado#&sCdAvisoRecebimento=#aviso_recebimento#&StrRetorno=XML'



codigoEmpresa='14145790'
senha='68972741'
cepOrigem='05866000'
cepDestino='04018000'
peso='0.500'
altura='30'
largura='17'
comprimento='16'
avisoRecebimento='N'
entregaMaoPropria='N'
valorDeclarado='0'


# Código dos correios:
#PAC: 41106
#SEDEX: 40010
#Função build_str_request recebe a String com a url de requisição;
#A variavel new_str_request recebe atraves da função sub do regex os valores dos parametros
#É retornado o valor da nova String com os parametros inseridos
def build_str_request_pac(str_request):
       
       new_str_request=re.sub('#codigo_servico#','41106', str_request)
       new_str_request=re.sub('#codigo_empresa#',codigoEmpresa, new_str_request)
       new_str_request=re.sub('#senha#',senha, new_str_request)
       new_str_request = re.sub('#cep_origem#', cepOrigem, new_str_request)
       new_str_request = re.sub('#cep_destino#',cepDestino , new_str_request)
       new_str_request = re.sub('#peso#', peso, new_str_request)
       new_str_request = re.sub('#altura#', altura, new_str_request)
       new_str_request = re.sub('#largura#', largura, new_str_request)
       new_str_request = re.sub('#comprimento#', comprimento, new_str_request)
       new_str_request=re.sub('#aviso_recebimento#', avisoRecebimento, new_str_request)
       new_str_request=re.sub('#mao_propria#', entregaMaoPropria, new_str_request)
       new_str_request=re.sub('#valor_declarado#', valorDeclarado, new_str_request)

       return new_str_request

def build_str_request_sedex(str_request):
       
       new_str_request=re.sub('#codigo_servico#','40010', str_request)
       new_str_request=re.sub('#codigo_empresa#',codigoEmpresa, new_str_request)
       new_str_request=re.sub('#senha#',senha, new_str_request)
       new_str_request = re.sub('#cep_origem#', cepOrigem, new_str_request)
       new_str_request = re.sub('#cep_destino#',cepDestino , new_str_request)
       new_str_request = re.sub('#peso#', peso, new_str_request)
       new_str_request = re.sub('#altura#', altura, new_str_request)
       new_str_request = re.sub('#largura#', largura, new_str_request)
       new_str_request = re.sub('#comprimento#', comprimento, new_str_request)
       new_str_request=re.sub('#aviso_recebimento#', avisoRecebimento, new_str_request)
       new_str_request=re.sub('#mao_propria#', entregaMaoPropria, new_str_request)
       new_str_request=re.sub('#valor_declarado#', valorDeclarado, new_str_request)

       return new_str_request

def build_str_request_e_sedex(str_request):
       
       new_str_request=re.sub('#codigo_servico#','81019', str_request)
       new_str_request=re.sub('#codigo_empresa#',codigoEmpresa, new_str_request)
       new_str_request=re.sub('#senha#',senha, new_str_request)
       new_str_request = re.sub('#cep_origem#', cepOrigem, new_str_request)
       new_str_request = re.sub('#cep_destino#',cepDestino , new_str_request)
       new_str_request = re.sub('#peso#', peso, new_str_request)
       new_str_request = re.sub('#altura#', altura, new_str_request)
       new_str_request = re.sub('#largura#', largura, new_str_request)
       new_str_request = re.sub('#comprimento#', comprimento, new_str_request)
       new_str_request=re.sub('#aviso_recebimento#', avisoRecebimento, new_str_request)
       new_str_request=re.sub('#mao_propria#', entregaMaoPropria, new_str_request)
       new_str_request=re.sub('#valor_declarado#', valorDeclarado, new_str_request)

       return new_str_request



pac=build_str_request_pac(str_request)







sedex=build_str_request_sedex(str_request)

e_sedex=build_str_request_e_sedex(str_request)

response=requests.get(pac)

pac=str(response.content)
response=requests.get(sedex)
sedex=str(response.content)
response=requests.get(e_sedex)
e_sedex=str(response.content)

xml_content1=bs(pac,"xml")
valor=xml_content1.Valor
prazoEntrega=xml_content1.PrazoEntrega
msgErro=xml_content1.MsgErro


xml_content2=bs(sedex, "xml")
valor_sedex=xml_content2.Valor
prazoEntrega_sedex=xml_content2.PrazoEntrega
msgErro_sedex=xml_content2.MsgErro

xml_content3=bs(e_sedex, "xml")
valor_e_sedex=xml_content3.Valor
prazoEntrega_e_sedex=xml_content3.PrazoEntrega
msgErro_e_sedex=xml_content3.MsgErro

try:
  print 'PAC: '+valor.string+'  Prazo de Entrega: '+prazoEntrega.string+' dia(s)'
except AttributeError:
    print 'TesteS'

try:
    print 'Mensagem: '+msgErro.string
except TypeError:
    print ''     

print '\n'

try:
  print 'SEDEX: '+valor_sedex.string+'  Prazo de Entrega: '+prazoEntrega_sedex.string+' dia(s)'
except TypeError:
    print 'Erro'

try:
    print 'Mensagem: '+msgErro_sedex.string
except TypeError:
    print '' 

print '\n'

try:
  if codigoEmpresa=='':
    pass
  else:

    print "E-SEDEX: "+ valor_e_sedex.string+' Prazo de Entrega: '+prazoEntrega_e_sedex.string
except TypeError:
  print 'Erro - verifique o xml'

try:
  if codigoEmpresa=='':
    print "Sem contratos para E-sedex"
  else: 
    print "Mensagem: "+msgErro_e_sedex.string  
except TypeError:
  print '' 





print xml_content3



print e_sedex