# Makefile for source rpm: vsftpd
# $Id$
NAME := vsftpd
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
