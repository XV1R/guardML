FROM python:latest 
ARG VERSION=ply-3.10
ARG FILE_EXT=tar.gz 
ARG FILE_NAME=${VERSION}.${FILE_EXT}
ARG LEX_YACC_LINK=http://www.dabeaz.com/ply/${FILE_NAME} 

RUN \
	wget ${LEX_YACC_LINK} && \
	tar -xvf ${FILE_NAME} && \
	cd ${VERSION} && \ 
	python setup.py install 

CMD ["/bin/bash"] 
