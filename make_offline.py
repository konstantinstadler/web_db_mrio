""" make_offline - modifies a Authorea github rep of online working

Notes
-----

Add standard offline header and footer including bibliography

Attributes
----------


KST 20150605 

"""

import sys
import os
import logging
import collections
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import IPython

def add_front(header = None, maketitle = True, fill_standard = True,):
    """ add front mater

    Parameters
    ----------
    header : str or list, optional
        Tex file(s) to include before the Authorea structure file (None by default)
    maketitle : boolean, optional
        If the line '\maketitle' should be included
    fill_standard : boolean, optinal
        Fill standard header if no external was given, default = True
    Returns
    -------
    list
        Lines to put at the top of the main tex file

    """
    start = []
    #IPython.embed()
    if header is not None:
        if type(header) is not list: header = [header]
        start += [r'\input{' + ff.rsplit('.tex')[0] + '}' + '\n' for ff in header]
    elif fill_standard:
        start += [
                r'\documentclass[12pt,letterpaper]{report}' + '\n',
                r'\usepackage[utf8]{inputenc}' + '\n',
                r'\usepackage{amsmath}' + '\n',
                r'\usepackage{amsfonts}' + '\n',
                r'\usepackage{amssymb}' + '\n',
                r'\usepackage{graphicx}' + '\n',
                r'\usepackage[hidelinks]{hyperref}' + '\n',
                r'\usepackage[T1]{fontenc}' + '\n',
                r'\usepackage{lmodern}' + '\n',
                '\n',
                r'\usepackage[authoryear,round,sort]{natbib}' + '\n',
                r'\bibliographystyle{plainnat}' + '\n',
                '\n',
                r'\title{\input{title.tex}}' + '\n',
                ]
    start.append('\n')
    start.append('\n')
    start.append(r'\begin{document}' + '\n')
    if maketitle:
        start.append(r'\maketitle'+ '\n')

    return start

def add_end(footer = None, fill_standard = True):
    """ add front mater

    Parameters
    ----------
    footer : str or list, optional
        Tex file(s) to include before the Authorea structure file (None by default)
    fill_standard : boolean, optinal
        Fill standard footer (just bibliography) if no external footer was given, default = True

    Returns
    -------
    list
        Lines to put at the top of the main tex file

    """
    end = []
    if footer is not None:
        if type(footer) is not list: footer = [footer]
        end += [r'\input{' + ff.rsplit('.tex')[0] + '}' + '\n' for ff in footer]
    elif fill_standard:
        end += [
                r'\bibliography{bibliography/biblio}' + '\n',
               ]
    end.append(r'\end{document}')
    return end


def convert_layout_line(line):
    """ converts a input tex line in layout.md to the write format for a main tex file

    Parameters
    ----------
    line : str
        the line to convert

    Returns
    -------
    list
        the converted line, can be more than one if it must be converted to a figure environment

    """
    if line is '\n':
        return line
    elif '.tex' in line:
        clean_line = line.rsplit('\n')[0].rsplit('.tex')[0]
        return '\input{' + clean_line + '}\n'
    else:
        figpath = os.path.split('./' + line.rsplit('\n')[0])[0]
        caption_lines = []
        for texfile in [tf for tf in os.listdir(figpath) if '.tex' in tf and tf != 'size.tex']:
            with open(os.path.join(figpath,texfile), 'r') as inpfile:
                caption_lines += inpfile.readlines()
        fig_env = [
                '\n',
                r'\begin{figure}[h!]' + '\n',
                r'\centering' + '\n',
	            r'\includegraphics[width=1.0\columnwidth]{' + line.rsplit('\n')[0] + '}\n'
                ] + caption_lines + [
                '\n',
                r'\end{figure}' + '\n',
                '\n',
                ]
        return fig_env


def main(path = None, header = None, footer = None, offline_main_file = 'main.tex', authorea_layout = 'layout.md'):
    """ Generate offline main tex file for Authorea git rep

    Note
    ----
    Any older version of offline_main_file will be overwritten

    Parameters
    ----------
    path : str, optional
        The path to the repo if not run directly there
    header : str or list, optional
        Tex file(s) to include before the Authorea structure file (None by default)
    footer : str or list, optional
        Tex file(s) to include after the Authorea structure file (None by default)
    offline_main_file : str, optional
        The top level tex filename (default: main.tex)
    authorea_layout : str, optional
        The layout file (layout.md as default)


    """
    if path:
        _old_path = os.path.abspath(os.curdir)
        os.chdir(path.rstrip('\\')[0])

    with open(authorea_layout, 'r') as inpfile:
        layout_lines = inpfile.readlines()
    
    with open(offline_main_file, 'w') as outfile: 
        for line in add_front(header = header):
            outfile.write(line)
        outfile.write('\n')
        for line in layout_lines:
            [outfile.write(ll) for ll in convert_layout_line(line)]
        outfile.write('\n')
        for line in add_end():
            outfile.write(line)

    return locals()


if __name__ == "__main__":
    locals().update(main(sys.argv[1:]))
    # or: var = main()
