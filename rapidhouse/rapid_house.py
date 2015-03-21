# -*- coding: utf-8 -*-
"""
This is a main program for RapidHouse that parse the command-line arguments, and call the sub-programs.
"""
import lib.ui as ui
import lib.rapidconfig as rapidconfig
import argparse


def main():
	parser = argparse.ArgumentParser(description='RapidHouse is a automated tuning-tool for a server application.')
	parser.add_argument('config', help='a PATH of a configuration-file for RapidHouse.')
	parser.add_argument('--version', action='version', version='v0.0.1')
	args = parser.parse_args()

	if args.config is None:
		args.config = '-'
	rc = rapidconfig.RapidConfig(args.config)
	rc.parse()

	interface = ui.Ui(rc)
	interface.manager()


if __name__ == "__main__":
	main()
