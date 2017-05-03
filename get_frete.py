# -*- coding:utf-8-*-
import requests
import re
from bs4 import BeautifulSoup as bs
import timeit
import json

class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'


class Pedido(object):

	def __init__(
			self,
	 		cep_origem,
	 		cep_destino,
	 		peso,
	 		altura,
	 		largura,
	 		comprimento
		):

		self.cep_origem  = cep_origem
		self.cep_destino = cep_destino
		self.peso        = peso
		self.altura      = altura
		self.largura     = largura
		self.comprimento = comprimento




class Cotacao_frete(object):

	def __init__(
		self                ,
		codigo_servico      ,
		codigo_empresa      ,
		senha               ,
		valor_declarado     ,
		aviso_recebimento   ,
		entrega_mao_propria ,
		pedido
	):
		self.codigo_servico      = codigo_servico
		self.codigo_empresa      = codigo_empresa
		self.senha 			     = senha
		self.valor_declarado     = valor_declarado
		self.aviso_recebimento   = aviso_recebimento
		self.entrega_mao_propria = entrega_mao_propria
		self.pedido				 = pedido 
		self.lista_retorno       = {}

	def realiza_cotacao(self):
		endpoint_url = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx'
		params = {
			"nCdEmpresa"          : self.codigo_empresa      ,
			"sDsSenha"            : self.senha               ,
			"nCdServico"          : self.codigo_servico,
			"sCepOrigem"          : self.pedido.cep_origem   ,
			"sCepDestino"         : self.pedido.cep_destino  ,
			"nVlPeso"             : self.pedido.peso         ,
			"nCdFormato"          : 1,
			"nVlComprimento"      : self.pedido.comprimento  ,
			"nVlLargura"          : self.pedido.largura      ,
			"nVlAltura"           : self.pedido.altura       ,
			"nVlDiametro"         : 0,
			"sCdMaoPropria"       : self.entrega_mao_propria ,
			"nVlValorDeclarado"   : self.valor_declarado     ,
			"sCdAvisoRecebimento" : self.aviso_recebimento   ,
			"StrRetorno"          : "XML"
		}


		response    = requests.get(endpoint_url, params = params)
		xml_content = bs(response.content, "xml")

		if  xml_content.Valor.string is None:
			self.lista_retorno['valor'] = '0.00'
		else:
			self.lista_retorno['valor'] = xml_content.Valor.string

		if xml_content.PrazoEntrega.string is None:
			self.lista_retorno['prazo_entrega'] = '0'	
		else:
			self.lista_retorno['prazo_entrega'] = xml_content.PrazoEntrega.string	

		# import ipdb; ipdb.set_trace()
		if  xml_content.MsgErro.string is None:
			self.lista_retorno['msgErro'] = '...'
		else:
			self.lista_retorno['msgErro'] = xml_content.MsgErro.string
	
			 
		return self.lista_retorno




if __name__ == "__main__":
	bcolors = bcolors()
	pedido  = Pedido(
	 		cep_origem  = '44052056' ,
	 		cep_destino = '22793104' ,
	 		peso        = '0.5'      ,
	 		altura      = '2'        ,
	 		largura     = '11'       ,
	 		comprimento = '16'       ,

		)

	pac    = Cotacao_frete(								# Código dos correios:
				codigo_servico      = '04669'    ,      # PAC   : 41106
				codigo_empresa      = '73047929' ,      # SEDEX : 40010
				senha               = '23721605' , 
				valor_declarado     = '100'        ,
				aviso_recebimento   = 'N'        ,
				entrega_mao_propria = 'N'        ,
				pedido              = pedido
			)

	sedex    = Cotacao_frete(
				codigo_servico      = '04162'    ,
				codigo_empresa      = '73047929' ,
				senha               = '23721605' , 
				valor_declarado     = '0'        ,
				aviso_recebimento   = 'N'        ,
				entrega_mao_propria = 'N'        ,
				pedido              = pedido
			)


	lista_pac = pac.realiza_cotacao()
	# import ipdb; ipdb.set_trace()

	lista_sedex = sedex.realiza_cotacao()
	

	print '====================================================================='
	print bcolors.BOLD +'PAC: ' + bcolors.ENDC + lista_pac['valor'] + '  prazo de Entrega: ' + lista_pac['prazo_entrega'] + ' dias(s)'
	print bcolors.BOLD + bcolors.WARNING + 'Mensagem: ' +bcolors.ENDC + lista_pac['msgErro'] 
	print '====================================================================='
	print bcolors.BOLD +'SEDEX: '+bcolors.ENDC + lista_sedex['valor'] + '  prazo de Entrega: ' + lista_sedex['prazo_entrega'] + ' dias(s)'
	print bcolors.BOLD + bcolors.WARNING + 'Mensagem: ' + bcolors.ENDC + lista_sedex['msgErro'] 
	print '====================================================================='



